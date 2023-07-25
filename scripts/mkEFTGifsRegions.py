#!/usr/bin/env python

import ROOT 
from copy import deepcopy
import CombineHarvester.CombineTools.ch as ch
import os
import math as mt
import argparse
from HistoRy import HistoBuilder
import sys

def getCanvas(n, reg):

    divs = ()
    list_divs = [(2,1), (3,1), (2,2), (3,2), (3,2), (4,2), (4,2), (3,3), (5,2), (4,3), (4,3), (5,3), (5,3), (5,3)]

    if n < len(list_divs): divs = list_divs[n-1]
    else:
        if n % 2 != 0: n+=1
        divs = (n/2, 2) 

    c = ROOT.TCanvas("c_" + reg, "c", 1000*divs[0], 1000*divs[1])
    c.Divide(divs[0],divs[1])

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
    parser.add_argument('-rp', '--rateparams',     dest='rateparams',     help='Do you want to retrieve rate param values from the fit? Default is False', required = False, default=True, action="store_true")
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
    parser.add_argument('-blind', '--blind-regions',   dest='blindregions',     help='Blind these regions, nargs=+', required = False, default = [], nargs="+")

    args = parser.parse_args()

    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0000)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetPalette(ROOT.kOcean)
    cols = ROOT.TColor.GetPalette()
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
    dr = ch.CombineHarvester()
    dr.ParseDatacard(datacard_name)
    
    regions = dr.bin_set()
    processes = dr.process_set()

    shapes_files = {k: "" for k in regions}
    f = open(datacard_name, "r")
    contents = f.readlines()

    i = 0
    while any(shapes_files[k] == "" for k in regions):

        line = contents[i]
        for j in regions:
            if j in line:
                for entry in line.split(" "):
                    if os.path.isfile(entry):
                        shapes_files[j] = entry
                        i+= 1
                        continue
        i += 1

    os.chdir(cwd)
    
    
    # cycle on each regions found in the datacard
    # for each region a gif will be plotted

    builders = {}
    for reg in regions:

        if reg not in args.regions and "all" not in args.regions: continue 
        file_ = shapes_files[reg]
        hh = HistoBuilder()
        hh.setInterestPOI(args.operators[0])
        hh.setShapes(file_)
        hh.setScan(args.scan, "limit")
        hh.setScanMaxNLL(args.maxNLL)
        hh.setRateParam(map.values())
        hh.runHistoryEFTNeg()

        builders[reg] = hh


    scan = builders[reg].getScan()
    values = builders[reg].returnInterestPOIValues()

    c = getCanvas(len(regions)+1, "__CANV")



    tex_saver = []
    histo_saver = []
    legends = []

    for idx, j in enumerate(sorted(values)):
        canv_idx = 1
        # draw this point only if frequency is preserved
        if idx % args.frequency == 0:

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

                if args.cms:
                    tex_cms1 = getCMS()
                    tex_cms1.Draw()

                if args.preliminary:
                    tex_p1 = getPreliminary()
                    tex_p1.Draw()

                tex_saver += [tex1, tex_cms1, tex_p1]

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
                bkg = [i for i in processes if i not in signals]
        
                histos["sm"].SetFillColor(ROOT.kGray)
                histos["sm"].SetLineWidth(0)
                histos["sm"].SetMarkerSize(0)


                data = "histo_Data" 
 
                leg = ROOT.TLegend(0.15, 0.89, 0.87, 0.7)
                leg.SetNColumns(3)
                leg.SetBorderSize(0)
                leg.SetTextSize(0.025)

                bkgs = {}

                v_ = ""
                if reg in vars.keys():
                    v_ = vars[reg]
    
                bkg_shapes = ROOT.THStack("hs_{}",";{};{}".format(reg, v_, "Events"))

                f = ROOT.TFile(shapes_files[reg])
                for idx_, b in enumerate(bkg):
                    h = f.Get("histo_"+b)
                    h.SetDirectory(0)
                    h.SetLineWidth(0)
                    h.SetMarkerSize(0)
                    col_idx = int(float(ncols) / len(bkg) * idx_)
                    # h.SetFillColor(colors[idx_])
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



                fullBSM = deepcopy(histos[j])
                
                for key in bkgs.keys():
                    fullBSM.Add(bkgs[key])

                    
                fullBSM.SetFillColor(0)
                fullBSM.SetLineWidth(2)
                fullBSM.SetLineColor(ROOT.kRed)

                fullBSM.Draw("hist same")

                # keep legend steady in the gif
                if j < 0: leg.AddEntry(fullBSM, "EFT {}={:.2f}".format(args.operators[0], j), "F")
                else: leg.AddEntry(fullBSM, "EFT {}={:.3f}".format(args.operators[0], j), "F")

                

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

                if args.cms:
                    tex_cms2 = getCMS()
                    tex_cms2.Draw()

                if args.preliminary:
                    tex_p2 = getPreliminary()
                    tex_p2.Draw()

                tex_saver += [tex2, tex_cms2, tex_p2]

                ROOT.gPad.RedrawAxis()

                canv_idx += 1

                #c.cd()    
                #ROOT.gPad.Update()

            c.cd()
            c.Print(os.path.join(args.outfolder, "{}.gif+20".format(plot_name)))