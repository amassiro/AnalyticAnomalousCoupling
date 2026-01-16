#!/usr/bin/env python3

import ROOT 
from copy import deepcopy
import CombineHarvester.CombineTools.ch as ch
from HiggsAnalysis.CombinedLimit.DatacardParser import *
import os
import math as mt
import argparse
from HiggsAnalysis.AnalyticAnomalousCoupling.utils.HistoRy import HistoBuilder
import sys
from optparse import OptionParser



def loadDatacard(dcpath: str, parser=None) -> Datacard:
    if parser == None:
        # create an empty parser
        parser = OptionParser()

    # add specific options that may not be present in the
    # command line and are specific for the parsing of
    # datacard

    addDatacardParserOptions(parser)

    # parse argument (and command line options)
    # if parser was created then we cannot parse
    # command line options

    if parser == None:
        (options, args) = parser.parse_args(args=[])
    else:
        (options, args) = parser.parse_args(args=[])

    # allow no signals
    options.allowNoSignal = True

    # read original datacard
    file = open(dcpath, "r")
    DC = parseCard(file, options)
    DC.path = "/".join(dcpath.split("/")[:-1]) + "/"
    if DC.path == "/":
        DC.path = "./"
    if not DC.hasShapes:
        DC.hasShapes = True

    return DC

def getCanvas(n, reg):

    divs = ()
    list_divs = [(2,1), (3,1), (2,2), (3,2), (3,2), (4,2), (4,2), (3,3), (5,2), (4,3), (4,3), (5,3), (5,3), (5,3)]

    # only LS
    if n ==0 : divs = (1,1)
    elif n < len(list_divs): divs = list_divs[n-1]
    else:
        if n % 2 != 0: n+=1
        divs = (int(n/2), 2) 
    
    print(divs)
    c = ROOT.TCanvas("c_" + reg, "c", 1000*divs[0], 1000*divs[1])
    c.Divide(divs[0],divs[1])
    
    for i in range(1, divs[0]*divs[1]+1):
        pad = c.cd(i)
        pad.SetTopMargin(0.1)
        pad.SetBottomMargin(0.1)
        pad.SetLeftMargin(0.1)
        pad.SetRightMargin(0.1)

    return c


def getLumi(lumi, energy):

    tex = ROOT.TLatex(0.88,.92,"{} ".format(lumi) +  "fb^{-1}" +  " ({} TeV)".format(energy))
    tex.SetNDC()
    tex.SetTextAlign(31)
    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.SetLineWidth(2)

    return tex

def getCMS():

    tex = ROOT.TLatex(0.22,.92,"CMS")
    tex.SetNDC()
    tex.SetTextFont(61)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.SetTextAlign(31)

    return tex

def getPreliminary():

    tex = ROOT.TLatex  (0.42, .92, "Preliminary")
    tex.SetNDC()
    tex.SetTextSize(0.76 * 0.05)
    tex.SetTextFont(52)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextAlign(31)

    return tex

                        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script allows to draw different gif plots for profiled EFT Fits using AnalyticalAnomalousCoupling')

    # Important infos
    parser.add_argument('-d', '--datacard',     dest='datacard',     help='Path to the datacard you used in the fit', required = True)
    parser.add_argument('-s', '--scan',     dest='scan',     help='Path to the combine output of the profiled fit using the -d --datacaard argument datacard', required = True)
    parser.add_argument('-op', '--operators',     dest='operators',     help='Operators of interest separated by a white space e.g. k_cqq3 k_cqq31 ...', required = True, nargs="+")
    parser.add_argument('-rp', '--rateparams',     dest='rateparams',     help='Do you want to retrieve rate param values from the fit? Default is False', required = False, default=False, action="store_true")
    parser.add_argument('-o', '--outfolder',   dest='outfolder',     help='output folder where plots will be saved', required = False, default = "plots")
    
    # Fancy plotting infos
    parser.add_argument('-variables', '--variables',     dest='variables',     help='Map for variables to regions in the form region:var region:var, will be used just to label x axis', required = False, nargs="+", default=[])
    parser.add_argument('-frequency', '--frequency',   dest='frequency',     help='Frequency of gif point (plot 1 over N points), default is to plot all', required = False, default = 1, type=int)
    parser.add_argument('-maxNLL', '--maxNLL',   dest='maxNLL',     help='Set the maximum of the NLL to be plotted, default is 5 (-2deltaNLL=10)', required = False, default = 5, type=float)
    parser.add_argument('-regions', '--regions',   dest='regions',     help='Draw gifs only for these regions separated by a white space, default is all', required = False, default = ["all"], nargs="+")
    parser.add_argument('-logy', '--logy',   dest='logy',     help='Set LogY on overall and signal panels, default is false', required = False, default = False, action="store_true")
    parser.add_argument('-drawSigma', '--drawSigma',   dest='drawSigma',     help='Draw one and two sigma levels in the scan panel, default is false', required = False, default = False, action="store_true")
    parser.add_argument('-lumi', '--lumi',   dest='lumi',     help='Draw this luminosity on the pad', required = False, default = "", type=str)
    parser.add_argument('-energy', '--energy',   dest='energy',     help='Draw this energy on the pad, default 13 TeV', required = False, default = 13, type=float)
    parser.add_argument('-cms', '--cms',   dest='cms',     help='Add cms label on top left', required = False, default = False, action="store_true")
    parser.add_argument('-preliminary', '--preliminary',   dest='preliminary',     help='Add preliminary label on top left', required = False, default = False, action="store_true")
    parser.add_argument('-blind', '--blind-regions',   dest='blindregions',     help='Blind these regions, by typing all, blind all regions nargs=+', required = False, default = [], nargs="+")

    args = parser.parse_args()

    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0000)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetPalette(ROOT.kOcean)
    cols = list(ROOT.TColor.GetPalette())
    print(cols)
    ncols = len(cols)

    datacard_name = args.datacard.split("/")[-1]
    datacard_folder = args.datacard.split(datacard_name)[0] 
    plot_name = "_".join(i for i in args.operators)

    margins = 0.11


    # create output dir
    try:
        os.mkdir(args.outfolder)
    except:
        pass
    
    map = {}
    if args.rateparams:
        dfile = open(args.datacard, "r")
        cont = dfile.readlines()

        # search for the rate params:
        for line in cont:
            if "rateParam" not in line: continue
            cleanline = a = [i for i in line.split(" ") if i]
            map[cleanline[3]] = cleanline[0]



    #map = {i.split(":")[0]:i.split(":")[1] for i in args.rateparams }  # background : rateparam
    vars = {i.split(":")[0]:i.split(":")[1] for i in args.variables }  # region : variable

    cwd = os.getcwd()
    if datacard_folder != '': os.chdir(datacard_folder)
    #dr = ch.CombineHarvester()
    #dr.ParseDatacard(datacard_name)
    
    #regions = dr.bin_set()
    #processes = dr.process_set()
    
    dc = loadDatacard(datacard_name)
    regions = [i for i in args.regions if i in dc.bins] if args.regions != ["all"] else dc.bins
    if args.blindregions == ["all"]: args.blindregions = dc.bins
    processes = dc.processes
    shapes_files = {k: {} for k in regions}
    
    for reg__ in dc.shapeMap.keys():
        if reg__ in shapes_files.keys():
            for entry in dc.shapeMap[reg__]:
                # should be one
                shapes_files[reg__]["file"] = dc.shapeMap[reg__][entry][0]
                # get prefix 
                for i in dc.shapeMap[reg__][entry][1:]:
                    if "$PROCESS" in i:
                        shapes_files[reg__]["prefix"] = i.split("$PROCESS")[0]
                        break

    os.chdir(cwd)
    
    
    # cycle on each regions found in the datacard
    # for each region a gif will be plotted

    builders = {}
    for reg in regions:
        file_ = shapes_files[reg]["file"]
        prefix_ = shapes_files[reg]["prefix"]
        hh = HistoBuilder()
        #hh.setInterestPOI(args.operators[0])
        hh.setShapes(file_)
        hh.setPrefix(prefix_)
        hh.setScan(args.scan, "limit")
        hh.setScanMaxNLL(args.maxNLL)
        print(map)
        hh.setRateParam(map.values())
        hh.runHistoryEFTNeg()

        builders[reg] = hh


    scan = builders[reg].getScan()
    values = builders[reg].returnInterestPOIValues()
    
    if isinstance(values[0], dict) and len(hh.pois) == 2 :
        # in this case the keys of the histos are integers (index in the tree)
        values = sorted(values, key=lambda x: (x[hh.pois[0]], x[hh.pois[1]]))
    else:
        values = sorted(values)

    c = getCanvas(len(regions), "__CANV")



    tex_saver = []
    histo_saver = []
    legends = []

    print(values)
    for idx, j in enumerate(values):
        canv_idx = 1
        # draw this point only if frequency is preserved
        if idx % args.frequency == 0:
            
            if isinstance(values[0], dict) and len(hh.pois) == 2 :
                # NEED TO PLOT IN 2D SCAN
                pass
            else:
                
                # If the likelihood scan at this point is greater than the required maximum then skip
                # this point and don't plot it
                try:
                    y = scan.Eval(j)
                    if y > args.maxNLL: continue
                except: 
                    # may fall here if the graph has no points
                    y = None

                
                if y is not None:
                    # Draw scan 
                    c.cd(canv_idx)

                    ROOT.gPad.SetFrameLineWidth(3)
                    ROOT.gPad.SetRightMargin(margins)
                    ROOT.gPad.SetLeftMargin(margins)

                    scan.Draw("AL")
                    scan.SetLineColor(ROOT.kBlack)
                    y = scan.Eval(j)

                    m = ROOT.TMarker(j, y, 20)
                    m.SetMarkerSize(2)
                    m.SetMarkerColor(ROOT.kBlack)

                    m.Draw("P same")

                    if args.drawSigma:

                        min_x, max_x = scan.GetXaxis().GetXmin(), scan.GetXaxis().GetXmax() 

                        x_frac = min_x + abs(0.05*(max_x-min_x))

                        o_sigma = ROOT.TLine(min_x, 1, max_x, 1)
                        o_sigma.SetLineStyle(2)
                        o_sigma.SetLineWidth(2)
                        o_sigma.SetLineColor(ROOT.kGray+2)
                        t_sigma = ROOT.TLine(min_x, 3.84, max_x, 3.84)
                        t_sigma.SetLineStyle(2)
                        t_sigma.SetLineWidth(2)
                        t_sigma.SetLineColor(ROOT.kGray+2)

                        o_sigma.Draw("L same")
                        t_sigma.Draw("L same")

                        ois = ROOT.TLatex()
                        ois.SetTextFont(42)
                        ois.SetTextSize(0.03)
                        ois.DrawLatex( x_frac, 1.05, '68%' )
                        tis = ROOT.TLatex()
                        tis.SetTextFont(42)
                        tis.SetTextSize(0.03)
                        tis.DrawLatex( x_frac, 3.89, '95%' )

                    if args.lumi:
                        tex1 = getLumi(args.lumi, args.energy)
                        tex1.Draw()
                        tex_saver.append(tex1)

                    if args.cms:
                        tex_cms1 = getCMS()
                        tex_cms1.Draw()
                        tex_saver.append(tex_cms1)

                    if args.preliminary:
                        tex_p1 = getPreliminary()
                        tex_p1.Draw()
                        tex_saver.append(tex_p1)

                    canv_idx+=1

            for reg in regions:

                c.cd(canv_idx)

                ROOT.gPad.SetFrameLineWidth(3)
                ROOT.gPad.SetRightMargin(margins)
                ROOT.gPad.SetLeftMargin(margins)


                # retrieve the builder
                hh = builders[reg]
                
                histos = hh.returnHistory()

                rateParams = hh.returnRateParams()

                signals = hh.getExpectedSigNames()
                # need to remove the prefix
                signals = [i.replace(shapes_files[reg]["prefix"], "") for i in signals]
                
                bkg = [i for i in processes if i not in signals and "_quad_" not in i]
                
        
                histos["sm"].SetFillColor(ROOT.kGray)
                histos["sm"].SetLineWidth(0)
                histos["sm"].SetMarkerSize(0)


                data = shapes_files[reg]["prefix"] + "data_obs" 
 
                leg = ROOT.TLegend(0.15, 0.89, 0.87, 0.7)
                leg.SetNColumns(3)
                leg.SetBorderSize(0)
                leg.SetTextSize(0.025)

                bkgs = {}

                v_ = ""
                if reg in vars.keys():
                    v_ = vars[reg]
    
                bkg_shapes = ROOT.THStack("hs_{}",";{};{}".format(reg, v_, "Events"))
                
                print(reg, shapes_files.keys(), reg in shapes_files.keys(), shapes_files[reg])
                f = ROOT.TFile(shapes_files[reg]["file"])
                for idx_, b in enumerate(bkg):
                    h = f.Get(shapes_files[reg]["prefix"]+b)
                    h.SetDirectory(0)
                    h.SetLineWidth(0)
                    h.SetMarkerSize(0)
                    col_idx = int(float(ncols) / len(bkg) * idx_)
                    h.SetFillColor(cols[col_idx])
                    leg.AddEntry(h, b, "F")
                    if b in map.keys():
                        h.Scale(rateParams[map[b]][idx])
                    bkgs[b] = deepcopy(h)
                    bkg_shapes.Add(h)

                h_data = f.Get(data)
                h_data.SetLineColor(ROOT.kBlack)
                h_data.SetMarkerColor(ROOT.kBlack)
                h_data.SetMarkerStyle(8)

                bkg_shapes.Add(histos["sm"])
                leg.AddEntry(histos["sm"], "SM", "F")

                bkg_shapes.SetMinimum(1e-1)
                # max = bkg_shapes.GetStack().Last().GetMaximum()
                max = h_data.GetMaximum()

                if args.logy:
                    bkg_shapes.SetMaximum(100*max)
                else:
                    bkg_shapes.SetMaximum(max + 0.3*max)

            
                bkg_shapes.GetStack().Last().GetYaxis().SetMaxDigits(2)
                bkg_shapes.Draw("hist")


                if isinstance(j, dict):
                    l_ = "_".join([f"{k}_{m}".replace(".","p").replace("-","m") for k,m in j.items()])
                    fullBSM = deepcopy(histos[l_])
                else:
                    fullBSM = deepcopy(histos[j])
                
                for key in bkgs.keys():
                    fullBSM.Add(bkgs[key])

                    
                fullBSM.SetFillColor(0)
                fullBSM.SetLineWidth(2)
                fullBSM.SetLineColor(ROOT.kRed)

                fullBSM.Draw("hist same")

                # keep legend steady in the gif
                if not isinstance(j, dict):
                    if j < 0: leg.AddEntry(fullBSM, "EFT {}={:.2f}".format(args.operators[0], j), "F")
                    else: leg.AddEntry(fullBSM, "EFT {}={:.3f}".format(args.operators[0], j), "F")
                else:
                    lab_ = ", ".join( [ "{}={:.3f}".format(k,m) if m>0 else  "{}={:.2f}".format(k,m) for k,m in j.items() ] )
                    leg.AddEntry(fullBSM, "EFT {}".format(lab_), "F")

                

                histo_saver += [fullBSM, bkg_shapes]

                if reg not in args.blindregions:
                    h_data.Draw("PE same")
                    leg.AddEntry(h_data, "Data", "PE")
                    histo_saver += [h_data]
                

                if args.logy: ROOT.gPad.SetLogy()

                leg.Draw()
                legends.append(leg)

                if args.lumi:
                    tex2 = getLumi(args.lumi, args.energy)
                    tex2.Draw()
                    tex_saver.append(tex2)

                if args.cms:
                    tex_cms2 = getCMS()
                    tex_cms2.Draw()
                    tex_saver.append(tex_cms2)

                if args.preliminary:
                    tex_p2 = getPreliminary()
                    tex_p2.Draw()
                    tex_saver.append(tex_p2)


                ROOT.gPad.RedrawAxis()

                canv_idx += 1

                #c.cd()    
                #ROOT.gPad.Update()

            c.cd()
            c.Print(os.path.join(args.outfolder, "{}.gif+20".format(plot_name)))