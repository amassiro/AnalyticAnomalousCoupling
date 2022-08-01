#!/usr/bin/env python

import ROOT 
from copy import deepcopy
import CombineHarvester.CombineTools.ch as ch
import os
import math as mt
import argparse
from HistoRy import HistoBuilder

def getCanvas(n, reg):
    if n == 1:
        c = ROOT.TCanvas("c_" + reg, "c", 1000, 1000)
    if n == 2:
        c = ROOT.TCanvas("c_" + reg, "c", 2000, 1000)
        c.Divide(2,1)
    if n == 3:
        c = ROOT.TCanvas("c_" + reg, "c", 3000, 1000)
        c.Divide(3,1)
    if n == 4:
        c = ROOT.TCanvas("c_" + reg, "c", 2000, 2000)
        c.Divide(2,2)

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
    parser.add_argument('-rp', '--rateparams',     dest='rateparams',     help='Map for rateparameters to background in the form name:param name:param (where name should match the name in the datacard', required = False, nargs="+")
    parser.add_argument('-t', '--type',     dest='type',     help='Gifs to be plotted, can choose between scan, overall, signal, templates. You can add more of them separated by a space', required = False, nargs="+", default=["scan", "overall", "signal", "templates"])
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


    args = parser.parse_args()

    ROOT.gROOT.SetBatch(1)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetPalette(ROOT.kOcean)

    datacard_name = args.datacard.split("/")[-1] 
    datacard_folder = args.datacard.split(datacard_name)[0] 

    plot_name = "_".join(i for i in args.type)

    margins = 0.11


    # create output dir
    try:
        os.mkdir(args.outfolder)
    except:
        pass
    
    map = {i.split(":")[0]:i.split(":")[1] for i in args.rateparams }  # background : rateparam
    vars = {i.split(":")[0]:i.split(":")[1] for i in args.variables }  # region : variable

    cwd = os.getcwd()

    os.chdir(datacard_folder)
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
        
        scan = hh.getScan()

        histos = hh.returnHistory()
        values = hh.returnInterestPOIValues()

        rateParams = hh.returnRateParams()

        signals = hh.getExpectedSigNames()
        bkg = [i for i in processes if i not in signals]

        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kCyan, ROOT.kViolet, ROOT.kGray, ROOT.kMagenta, ROOT.kSpring, ROOT.kGreen, ROOT.kTeal, ROOT.kOrange, ROOT.kYellow, ROOT.kAzure, ROOT.kCyan+2, ROOT.kCyan+5]
        
        histos["sm"].SetFillColor(ROOT.kGray)
        histos["sm"].SetLineWidth(0)
        histos["sm"].SetMarkerSize(0)

        c = getCanvas(len(args.type), reg)


        ROOT.gStyle.SetOptStat(0000)

        for idx, j in enumerate(sorted(values)):

            # draw this point only if frequency is preserved
            if idx % args.frequency == 0:


                print(idx)
                
                # If the likelihood scan at this point is greater than the required maximum then skip
                # this point and don't plot it
                y = scan.Eval(j)
                if y > args.maxNLL: continue

                for type_index, t_ in enumerate(args.type):
                    
                    c.cd(type_index + 1)
                    ROOT.gPad.SetFrameLineWidth(3)
                    ROOT.gPad.SetRightMargin(margins)
                    ROOT.gPad.SetLeftMargin(margins)

                    if t_ == "scan":

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


                    if t_ == "overall":

                        leg = ROOT.TLegend(0.15, 0.89, 0.89, 0.7)
                        leg.SetNColumns(3)
                        leg.SetBorderSize(0)
                        leg.SetTextSize(0.025)

                        bkgs = {}

                        v_ = ""
                        if reg in vars.keys():
                            v_ = vars[reg]
            
                        bkg_shapes =ROOT.THStack("hs",";{};{}".format(v_, "Events"))

                        f = ROOT.TFile(file_)
                        for idx_, b in enumerate(bkg):
                            h = f.Get("histo_"+b)
                            h.SetLineWidth(0)
                            h.SetMarkerSize(0)
                            h.SetFillColor(colors[idx_])
                            leg.AddEntry(h, b, "F")
                            if b in map.keys():
                                h.Scale(rateParams[map[b]][idx])
                            bkgs[b] = deepcopy(h)
                            bkg_shapes.Add(h)

                        bkg_shapes.Add(histos["sm"])
                        leg.AddEntry(histos["sm"], "SM", "F")

                        bkg_shapes.SetMinimum(1e-1)
                        max = bkg_shapes.GetStack().Last().GetMaximum()

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

                        leg.AddEntry(fullBSM, "SM+EFT {}={:.3f}".format(args.operators[0], j), "F")

                        if args.logy: ROOT.gPad.SetLogy()

                        leg.Draw()

                        if args.lumi:
                            tex2 = getLumi(args.lumi, args.energy)
                            tex2.Draw()

                        if args.cms:
                            tex_cms2 = getCMS()
                            tex_cms2.Draw()

                        if args.preliminary:
                            tex_p2 = getPreliminary()
                            tex_p2.Draw()

                    if t_ == "signal":

                        leg2 = ROOT.TLegend(0.45, 0.89, 0.89, 0.65)
                        leg2.SetNColumns(1)
                        leg2.SetBorderSize(0)
                        leg2.SetTextSize(0.025)

                        sm = deepcopy(histos["sm"])

                        v_ = ""
                        if reg in vars.keys():
                            v_ = vars[reg]
                        
                        max_ = sm.GetMaximum()
                        #sm.SetMinimum(1e-1)

                        if args.logy:
                            sm.SetMaximum(100*max_)
                        else:
                            sm.SetMaximum(max_ + 0.3*max_)
                        
                        sm.SetTitle("")
                        sm.GetXaxis().SetTitle(v_)
                        sm.GetYaxis().SetTitle("Events")
                        sm.GetYaxis().SetMaxDigits(2)


                        sm.Draw("hist")

                        histos[j].SetLineColor(ROOT.kRed)
                        histos[j].SetLineWidth(2)

                        histos[j].Draw("hist same")

                        h_err = deepcopy(sm)
                        h_err.SetMarkerSize(0)
                        h_err.SetFillColor(ROOT.kBlack)
                        h_err.SetFillStyle(3005)

                        h_err.Draw("E2 same")

                        leg2.AddEntry(sm, "SM", "F")
                        leg2.AddEntry(histos[j], "SM+EFT {}".format("{} = {:.3f}".format(args.operators[0], j)), "F")
                        leg2.AddEntry(h_err, "Stat. Unc.", "F")

                        leg2.Draw()

                        if args.logy: ROOT.gPad.SetLogy()

                        if args.lumi:
                            tex3 = getLumi(args.lumi, args.energy)
                            tex3.Draw()

                        if args.cms:
                            tex_cms3 = getCMS()
                            tex_cms3.Draw()

                        if args.preliminary:
                            tex_p3 = getPreliminary()
                            tex_p3.Draw()

                    if t_ == "templates":

                        leg3 = ROOT.TLegend(0.45, 0.89, 0.89, 0.7)
                        leg3.SetNColumns(1)
                        leg3.SetBorderSize(0)
                        leg3.SetTextSize(0.025)

                        sm2 = histos["sm"].Clone("sm_")


                        v_ = ""
                        if reg in vars.keys():
                            v_ = vars[reg]

                        
                        sm2.SetMaximum(sm2.GetMaximum() + 0.5*sm2.GetMaximum())
                        sm2.SetMinimum(-sm2.GetMaximum())
                        sm2.SetTitle("")
                        sm2.GetXaxis().SetTitle(v_)
                        sm2.GetYaxis().SetTitle("Events")
                        sm2.GetYaxis().SetMaxDigits(2)


                        sm2.Draw("hist")

                        js = deepcopy(histos[j])
                        js.SetLineColor(ROOT.kRed)
                        js.SetLineWidth(2)
                        js.Draw("hist same")

                        h_err2 = deepcopy(sm2)
                        h_err2.SetMarkerSize(0)
                        h_err2.SetFillColor(ROOT.kBlack)
                        h_err2.SetFillStyle(3005)

                        h_err2.Draw("E2 same")


                        for template in hh.historySingleHistos[j].keys():
                            
                            hh.historySingleHistos[j][template].SetLineColorAlpha(ROOT.kAzure+1, 0.3)
                            hh.historySingleHistos[j][template].SetFillColor(0)
                            hh.historySingleHistos[j][template].SetMarkerSize(0)

                            hh.historySingleHistos[j][template].Draw("hist same")

                            

                        leg3.AddEntry(sm2, "SM", "F")
                        leg3.AddEntry(js, "SM+EFT {}".format("{} = {:.3f}".format(args.operators[0], j)), "F")
                        leg3.AddEntry(h_err2, "Stat. Unc.", "F")

                        leg3.AddEntry(hh.historySingleHistos[j][template], "Templates", "F")

                        leg3.Draw()

                        if args.lumi:
                            tex4 = getLumi(args.lumi, args.energy)
                            tex4.Draw()

                        if args.cms:
                            tex_cms4 = getCMS()
                            tex_cms4.Draw()

                        if args.preliminary:
                            tex_p4 = getPreliminary()
                            tex_p4.Draw()


                c.cd()
            
                c.Draw()
                c.Print(os.path.join(args.outfolder, "{}_{}.gif+20".format(reg, plot_name)))
