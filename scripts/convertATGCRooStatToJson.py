import json 
from glob import glob
import os, sys
import ROOT 
from concurrent.futures import ProcessPoolExecutor as Pool
import argparse 

def usage_msg(name=None):
    return """
              Command line parser to convert aTGCRooStat signal yields into 
              a json input compliant with AnalyticAnomalousCoupling. 
              This script makes some assumptions: You should already have aTGCRooStat datacards
              and all root files should be available, those containing the EFT parametrization as TF(1,2,3)
              and those of the backgrounds.
              This scripts reads the parametrization files and converts it into a json file that can be read
              by AnalyticAnomalousCoupling EFT model.

              The EFT parametrization file names should follow this convention:
                    <whatever>_<name>.root
              Where <name> is the one appearing in the datacard except for an arbitrary prefix that can be added 
              to all samples by specifying the c.l.a. -pp (or --processprefix) so that the datacard name reads as
                    <processprefix>_<name>
              
              The parametrization should be know and should be the same for all the root input files. For example 
              the files could contain a TF3 function with following content
                    [0]+[1]*x+[2]*y+[3]*z+[4]*x*y+[5]*x*z+[6]*y*z+[7]*x*x+[8]*y*y+[9]*z*z
              We do not know what the 'x' coeff., [1] stands for so it should be provided as an input to this script.

              For example, we have multiple files containing the parametrization for each bin as:
                    signal_proc_ZVBF_ptZ_mu_3D_binx0.root, signal_proc_ZVBF_ptZ_mu_3D_binx1.root
                    signal_proc_ZVBF_ptZ_mu_3D_binx2.root, signal_proc_ZVBF_ptZ_mu_3D_binx3.root, ...

              And atGCRooStat compliant datacards with process names:
                    anoCoupl_process_ZVBF_ptZ_mu_3D_binx0, anoCoupl_process_ZVBF_ptZ_mu_3D_binx1
                    anoCoupl_process_ZVBF_ptZ_mu_3D_binx2, anoCoupl_process_ZVBF_ptZ_mu_3D_binx3, ...
            
              The EFT parametrization in the 'signal_proc_*' files reads as:
                    sm + x*lin_cx + y*lin_cw + z*lin_cb + x*y*mix_cx_cw + x*z*mix_cx_cb + y*z*mix_cw_cb + 
                    + x*x*quad_cx + y*y*quad_cw + z*z*quad_cb

              Therefore this script can be called as:

                    python convertToJson.py -fg signal_proc_*.root -pp anoCoupl_process -fp signal_proc
                                            -c sm:0,lin_cx:1,lin_cw:2,lin_cb:3,mix_cx_cw:4,mix_cx_cb:5,mix_cw_cb:6,quad_cx:7,quad_cw:8,quad_cb:9
                                            -mp 8 -o converted_aTGC_EFT2Obs.json

           """

def readBinParab(arg):
    # map with coefficients to TF3 params count from 0 (SM) to 9
    paramMap = arg["map"]

    f = ROOT.TFile(arg["file"])
    funcname = [i.GetName() for i in f.GetListOfKeys()][0]
    func = f.Get(funcname)

    coeff_dict = {arg["sample"]: {k: func.GetParameter(paramMap[k]) for k in list(paramMap.keys())}}

    # normalize by sm weight so that the algebra 
    # reads as EFT2Obs: 1 + Ax + Bxx + Cy + Dyy + Exy + ...
    sm = coeff_dict[arg["sample"]]["sm"]

    for coef in list(coeff_dict[arg["sample"]].keys()):
        coeff_dict[arg["sample"]][coef] /= sm

    print(("--> Parametrization for file {}".format(arg["file"])))
    print(coeff_dict)

    return coeff_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert aTGC to AnaliticAnomalousCoupling', usage=usage_msg())
    parser.add_argument('-fl',  '--filelist',   dest='filelist',     help='Comma separated list of file name containing TF or TH for the signal bin EFT parametrization')
    parser.add_argument('-fg',  '--fileglob',   dest='fileglob',     help='String glob-compliant to retrieve all files at once instead of filelist')
    parser.add_argument('-c',  '--coefficients',   dest='coefficients',     help='Map of the signal TF parameters to coefficients of the EFT \
                                                                                  expansion with following syntax (numbers are examples): \
                                                                                  sm:0,lin_cx:1,quad_cx:7,lin_cw:2,quad_cw:8,mix_cx_cw:4...', required=True)
    parser.add_argument('-o',  '--output',   dest='output',     help='Name of the output .json file, needs to terminate with .json. By default: converted_aTGC_EFT2Obs.json', \
                        required=False, default="converted_aTGC_EFT2Obs.json")
    parser.add_argument('-mp',  '--multiproc',   dest='multiprocess',     help='Number of cores used to read signal files, by default single core', required=False, type=int, default=1)
    parser.add_argument('-pp',  '--processprefix',   dest='processprefix',     help='Process prefix as seen from the datacard, to be appended', required=False, type=str, default="")
    parser.add_argument('-fp',  '--fileprefix',   dest='fileprefix',     help='EFT parametrization files prefix to be stripped to retreive the process name', required=False, type=str, default="")
    args = parser.parse_args()

    # build the hard coded coeffiient map:
    # function content [0]+[1]*x+[2]*y+[3]*z+[4]*x*y+[5]*x*z+[6]*y*z+[7]*x*x+[8]*y*y+[9]*z*z
    # from sapta codes
    # param_sm = func.GetParameter(0)
    # param_int_cx = func.GetParameter(1)
    # param_bsm_cx = func.GetParameter(7)
    # param_int_cw = func.GetParameter(2)
    # param_bsm_cw = func.GetParameter(8)
    # param_int_cb = func.GetParameter(3)
    # param_bsm_cb = func.GetParameter(9)

    # --> SM = [0]
    # --> lin_cx = [1]
    # --> quad_cx = [7]
    # --> lin_cw = [2]
    # --> quad_cw = [8]
    # --> lin_cb = [3]
    # --> quad_cb = [9]
    # --> mix_cx_cw = [4]
    # --> mix_cx_cb = [5]
    # --> mix_cw_cb = [6]

    # ops = ["cw", "cx", "cb"]
    # coeff_dict = {
    #     "sm": 0,
    #     "lin_cx": 1,
    #     "lin_cw": 2,
    #     "lin_cb": 3,
    #     "quad_cx": 7,
    #     "quad_cw": 8,
    #     "quad_cb": 9,
    #     "mix_cx_cw": 4,
    #     "mix_cx_cb": 5,
    #     "mix_cw_cb": 6
    # }

    if args.filelist is None and args.fileglob is None:
        print("[ERROR] You need to provide either a comma separated list of files with \
               -fl (or --filelist) such as: -fl file1.root,file2.root or alternatively a glob string to retrieve all    \
               files matching a pattern with -fg (or --fileglob) such as: -fg file*.root")
        sys.exit(0)

    if args.filelist is not None:
        files = args.filelist.split(",")
    elif args.fileglob is not None and ".root" in args.fileglob:
        files = glob(args.fileglob)

    # check that all files are root files 
    if not all(i.endswith(".root") for i in files):
        print("[ERROR] the file list retreived does contain non-root files, is that correct?")
        print("The file list: ")
        print(files)
        sys.exit(0)

    if args.fileprefix != "":
        if not args.fileprefix.endswith("_"): args.fileprefix+="_"
    if args.processprefix != "":
        if not args.processprefix.endswith("_"): args.processprefix+="_"

    coeff_dict = {k: i for k,i in [it_.split(":") for it_ in args.coefficients.split(",")]}
    # need to retrieve the ops:
    ops = [i.strip("quad_") for i in list(coeff_dict.keys()) if i.startswith("quad_")]

    print(("--> Detected {} operators: {}".format(len(ops), ops)))

    # name of the signal processes per bin: anoCoupl_process_ZVBF_ptZ_mu_3D_bin2
    # name of the parabola files : signal_proc_ZVBF_ptZ_el_3D_bin2.root

    arguments = []
    for f_ in files:
        
        sample_name = args.processprefix + f_.split(".root")[0].split(args.fileprefix)[1]
        arg_dict = {}
        arg_dict["file"] = f_ 
        arg_dict["map"] = coeff_dict
        arg_dict["sample"] = sample_name

        arguments.append(arg_dict)

    print("---> Starting to build the EFT parametrization")
    with Pool(args.multiprocess) as p:
        coeffs = list(p.map(readBinParab, arguments))
    print("---> Done")

    # create a fake EFT2Obs dictionary
    # bin_labels are the bins of the processes as written in the datacard
    # edges are the distribution bin edges but are not used in the t2w
    # parameters: list of parameters of interest
    # bins: list of lists containing the EFT parametrization -> 3 entries = lin, 4 entries = quad only first value of list is the actual coef
    # aread: Do not know and do not care

    keys = ['bin_labels', 'edges', 'parameters', 'bins', 'areas']
    toWrite = {k: [] for k in keys}
    toWrite["parameters"] = ops
    # the only key in the list of coeffs is the bin name as writtten in datacard
    toWrite["bin_labels"] = [list(i.keys())[0] for i in coeffs]

    # now contruct the parametrization in a compatible way
    bins = []
    for c in coeffs:
        ov = []
        sample = list(c.keys())[0]
        coeff = c[sample]

        for cv in list(coeff.keys()):
            if cv.startswith("lin"):
                ov.append([coeff[cv], coeff[cv], cv.strip("lin_")])
            elif cv.startswith("quad"):
                ov.append([coeff[cv], coeff[cv], cv.strip("quad_"), cv.strip("quad_")])
            elif cv.startswith("mix"):
                op1, op2 = cv.strip("mix_").split("_")
                ov.append([coeff[cv], coeff[cv], op1, op2])

        bins.append(ov)

    toWrite["bins"] = bins    
    
    outfname = args.output

    print("---> Dumping into json")

    d_ = json.dumps(toWrite, indent = 4)
    with open(outfname, "w") as f: 
        f.write(d_)
    f.close()

    print("---> Done")