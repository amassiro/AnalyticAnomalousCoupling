#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json 
import ROOT
from glob import glob
import sys
import numpy as np
from itertools import combinations
import argparse

def usage_msg(name=None):
    return """

           convertAACtoIM.py -i <INPUT_DATACARD>
                             -o <OUTPUT_DATACARD>
                             -op <op1 op2 op3 op4 ...>
                             -sf <OUTPUT_JSON_FILE>
                             --noDumping -> Optional: do not dump the datacard
                             --noScaling -> Optional: do not dump the EFT scaling

           This script converts a datacard + shapes compatible with the AnaliticAnomalousCouplingEFTNegative model
           into a datacard + json file for usage with the new InterferenceModel for EFT 
           https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/main/python/InterferenceModels.py

           You should specify the input datacard you want to convert with c.l.a. -i (--input).
           The output datacard, created at path specified by -o (--ouput), will present only one process named "sm". All EFT components such as quad_op,
           sm_lin_quad_op and so on will be dropped along with their nuisances.

           The EFT scaling will be implemented in a JSON file saved in the file specified by -sf (--scalefile) for each region, and bin of the input distributions.
           You can specify the operators you want to extract the EFT scaling with the c.l.a. -op (--operators).

           The scaling will contain a quadratic form for each bin as a lower triangular matrix of the EFT scaling as:

           1/SM * (SM + kLin + k**2Quad + mLin + m**2Quad + kmMix + ...) = 1 + kA + k**2B + mC + m**2D + kmE + ...

           Where Lin = 2*Re(A_{SM}*A_{op}) and Quad = |A_{op}|^{2}

           If one switches to the matrix version of the quadratic form above:

           [ [ |A_{1}|2,         Re(A_{SM}*A_{1}|),  Re(A_{1}*A_{2})   ],  [op_1,
             [ Re(A_{SM}*A_{1}|),   |A_{2}|^2,       Re(A_{SM}*A_{2}|) ],   op_2, 
             [ Re(A_{1}*A_{2}),  Re(A_{SM}*A_{2}|),        1           ]]   1]

           Which can be generalized for arbitrary number of operators. In the JSON file the constant term will read as BScaling[1]

           Two additional c.l.a. can be specified to avoid to dump the datacard or to avoid to dump the EFT scaling respectively:
             --noDumping
             --noScaling 
           """

def amplitude_squared_for(ops, icoef, jcoef):
   # pure quadratics
   if icoef == jcoef:
     if icoef == len(ops): return "sm"
     else: return "quad_" + str(ops[icoef])

   # linears and mixed quadratics
   else:
      if icoef == len(ops):
         return "lin_" + str(ops[jcoef])
      elif jcoef == len(ops)-1:
         return "lin_" + str(ops[icoef])
      else: return "mix_" + str(ops[icoef]) + "_" + str(ops[jcoef])
       

def filterLine(line, start, keep, nuis=False):
   bl = [i for i in line.split(start)[1].split(" ") if i != "" and i != "\n"] 
   if not nuis:
      blol = [bl[i] for i in keep]
      oline = start + "       " + "         ".join(i for i in blol) +  "\n" 

   else:
      type_ = bl.pop(0)
      blol = [bl[i] for i in keep]
      oline = start + "       " + type_ + "       " + "         ".join(i for i in blol) +  "\n"
   return oline

def dumpEFT(card, out):

    f = open(card, "r")
    lines = f.readlines()

    drop_keyswords = ["quad_", "lin_", "sm_lin_quad_"]
    # processes
    for line in lines:
       if line.startswith("process"):
          procs = [i for i in line.split("process")[1].split(" ") if i != "" and i != "\n"]
          break

    f.close()
    # find index to drop
    drop_idx = []
    for idx, proc in enumerate(procs):
       for dk in drop_keyswords:
          if proc.startswith(dk) and idx not in drop_idx: drop_idx.append(idx)

    keep_idx = [i for i in range(len(procs)) if i not in drop_idx]
    keep_procs = np.unique([procs[i] for i in keep_idx])
    # jmax
    nprocs = len(keep_procs)-1
 
    f = open(card, "r")
    fout = open(out, "w")

    lines = f.readlines()
    pidx = 0 
    bin = 0
    rate = 0

    for line in lines:

       if not line.strip():
          fout.write(line)
          continue
       if line.startswith("jmax"):
          fout.write("jmax " + str(nprocs) + " number of processes minus 1\n")
          continue
       if line.startswith("-"):
          fout.write(line)
          continue
       if line.startswith("bin"):
          if bin == 0: 
             fout.write(line)
             bin += 1
             continue
          else:
             fout.write(filterLine(line, "bin", keep_idx))
             bin += 1
             continue
       if line.startswith("process"):
          fout.write(filterLine(line, "process", keep_idx))
          pidx += 1
          continue
       if line.startswith("rate"):
          fout.write(filterLine(line, "rate", keep_idx))
          rate += 1
          continue
       # is this a nuisance
       if rate == 1 and pidx == 2 and bin == 2:
          fl = [i for i in line.split(" ") if i != "" and i != "\n"]
          nuisname = fl[0]
          nuis_type = fl[1]
          if fl[1] in ["autoMCStats", "rateParam"]:
             fout.write(line)
             continue
          else:
             fout.write(filterLine(line, nuisname, keep_idx, nuis=True))
             continue 

       fout.write(line)      


if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Command line parser to extract EFT parametrization as JSON from an AnalyticAnomalousCoupling (EFTNegative) datacard', usage=usage_msg())
   parser.add_argument('-op',  '--operators',   dest='operators',     help='Operators for which you want to extract the parametrization -op (--operators) cW cW cHB ...', required = True, nargs="+")
   parser.add_argument('-i',  '--input',   dest='input',     help='Path to the input datacard', required = True, type=str)
   parser.add_argument('-o',  '--output',   dest='output',     help='Path to the ouput datacard that will be created, default is dumped.txt', required = False, type=str, default="dumped.txt")
   parser.add_argument('-sf',  '--scalefile',   dest='scalefile',     help='Path to the ouput json file with the EFT scaling, default is scaling.json', required = False, type=str, default="scaling.json")
   parser.add_argument('--noScaling',   dest='noscaling',     help='Do not create EFT scaling', required = False, default=False, action="store_true" )
   parser.add_argument('--noDumping',   dest='nodumping',     help='Do not dump datacard', required = False, default=False, action="store_true")

   args = parser.parse_args()

   ops = args.operators

   if not args.nodumping:
      print("Removing all EFT templates from original datacard and dumping in {}".format(sys.argv[3]))
      dumpEFT(args.input, args.output)

   if not args.noscaling: 

      print("Running the scaling for {}".format(" ".join(ops)))
      shapefiles = {}
      f = open(args.input, "r")
      lines = f.readlines()

      for l in lines:
         if l.startswith("shapes *"):
            # region, shape_file_path, nominal_wildcard, varied_wildcard
            filterline = [i for i in l.split("shapes *")[1].split(" ") if i != ""]
            region = filterline[0]
            path = filterline[1]
            nominal = filterline[2]
            if "$PROCESS" in nominal: nominal = nominal.replace("$PROCESS", "")
            shapefiles[region] = {"path": path, "nominal": nominal}


      scaling = []
      for channel in shapefiles.keys():
         sd = {}
         sd["process"] = "sm"
         sd["channel"] = channel
         sd["parameters"] = ["k_" + i for i in ops] + ["Bscaling[1]"]
         
         sd["scaling"] = []

         combo = list(combinations(ops, 2))
         matrix = {}

         f = ROOT.TFile(shapefiles[channel]["path"])
         # get SM first as needed for normalization
         matrix["sm"] = f.Get(shapefiles[channel]["nominal"] + "sm")

         for op in ops:
            for comp in ["quad_", "sm_lin_quad_"]:
               matrix[comp + op] = f.Get(shapefiles[channel]["nominal"] + comp + op)

         for c in combo:
            if shapefiles[channel]["nominal"] + "sm_lin_quad_mixed_" + c[0] + "_" + c[1] in [i.GetName() for i in f.GetListOfKeys()]: 
               matrix["sm_lin_quad_mixed_" + c[0] + "_" + c[1]] = f.Get(shapefiles[channel]["nominal"] + "sm_lin_quad_mixed_" + c[0] + "_" + c[1])
            elif shapefiles[channel]["nominal"] + "sm_lin_quad_mixed_" + c[1] + "_" + c[0] in [i.GetName() for i in f.GetListOfKeys()]:
               matrix["sm_lin_quad_mixed_" + c[1] + "_" + c[0]] = f.Get(shapefiles[channel]["nominal"] + "sm_lin_quad_mixed_" + c[1] + "_" + c[0])
            else:
               print("Error {} {}".format(shapefiles[channel]["path"], "sm_lin_quad_mixed_" + c[1] + "_" + c[0]))

         # add lin and mixed after we filled the matrix
         for op in ops:  
            matrix["lin_" + op] = matrix["sm_lin_quad_" + op].Clone("lin_" + op)
            matrix["lin_" + op].Add(matrix["sm"], -1)
            matrix["lin_" + op].Add(matrix["quad_" + op], -1)

            # divide by 2 linears
            matrix["lin_" + op].Scale(1./2)

         for c in combo:

            if "sm_lin_quad_mixed_" + c[1] + "_" + c[0] in matrix.keys():
               name = "mix_" + c[0] + "_" + c[1]
               matrix[name] = matrix["sm_lin_quad_mixed_" + c[1] + "_" + c[0]].Clone(name)
               matrix[name].Add(matrix["sm"])
               matrix[name].Add(matrix["sm_lin_quad_" + c[0]], -1)
               matrix[name].Add(matrix["sm_lin_quad_" + c[1]], -1)
               # divide by 2 linears
               matrix[name].Scale(1./2)
            elif "sm_lin_quad_mixed_" + c[0] + "_" + c[1] in matrix.keys():
               name = "mix_" + c[1] + "_" + c[0]
               matrix[name] = matrix["sm_lin_quad_mixed_" + c[0] + "_" + c[1]].Clone(name)
               matrix[name].Add(matrix["sm"])
               matrix[name].Add(matrix["sm_lin_quad_" + c[0]], -1)
               matrix[name].Add(matrix["sm_lin_quad_" + c[1]], -1) 
               # divide by 2 linears
               matrix[name].Scale(1./2)
            else:
               print("Error")
            
                           
         # for each bin derive the triangular
         # parametrization         
         for ibin in range(matrix["sm"].GetNbinsX()):
            scale_bin = []
            # denominator 
            fact = matrix["sm"].GetBinContent(ibin+1)

            # get matrix eleements
            for i in range(len(ops)+1):
               for j in range(i + 1 ):
                  if fact == 0:
                     print("[WARNING] sm bin count for bin {} in region {} is ZERO. Will set all EFT to ZERO".format(ibin+1, channel)) 
		     scale_bin.append(0)
                     continue
                  try:
                     scale_bin.append(matrix[amplitude_squared_for(ops, i, j)].GetBinContent(ibin+1) / fact)
                  except:
                     op1, op2 = amplitude_squared_for(ops, i, j).split("_")[1], amplitude_squared_for(ops, i, j).split("_")[2]
                     name = "mix_" + op2 + "_" + op1
                     scale_bin.append(matrix[name].GetBinContent(ibin+1) / fact)

            sd["scaling"].append(scale_bin) 

         scaling.append(sd)
         f.Close()

      dump = json.dumps(scaling, indent=4)
      with open(args.scalefile, 'w') as f:
         f.write(dump)
         
