#!/usr/bin/env python3

from HiggsAnalysis.AnalyticAnomalousCoupling.utils.functions import *
import ROOT
import json 
import numpy as np
ROOT.gStyle.SetLineScalePS(1)
from array import array
import argparse
ROOT.gROOT.SetBatch(0)

poi_to_label = {}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ciaone')
    parser.add_argument("-cfg", "--config", dest="config", help="The configuration file with the analysis", required=True)
    parser.add_argument("-s", "--scale", dest="scale", help="Scale these op by a factor. Comma separated list as cW:10,cHW:2,...", required=False, default = "")
    parser.add_argument("-k", "--keepan", dest="keepan", help="Keep only these AN, comma separated list", required=False, default = None)
    parser.add_argument("-c", "--common", dest="common", help="Keep only operators shared by more than one analysis. Default is false", required=False, default = False, action="store_true")
    parser.add_argument("-f", "--filter", dest="filter", help="Filter results for this analysis. Keep other analyses only if they share ops with this one", required=False, default = "")
    parser.add_argument("-o", "--output", dest="output", help="Plot output name without extension. Default is summary", required=False, default = "summary")
    args, _ = parser.parse_known_args()

    # loading the analysis dictionary
    an = {}
    lumi = "138"
    exec(open(args.config,"r").read())

    # keep an if specified
    if args.filter: filter_for_analysis_(an, args.filter)
    if args.keepan: keep_analyses(an, args.keepan.split(","))
    if args.common: filter_common_ops_(an)


    # revert the plot dictionary so that keys are the operators
    plot = revert_dictionary(an)

    # scale operators
    scale = [i.split(":") for i in args.scale.split(",") if i != ""]
    for sf in scale:
        print("--> Will scale {} by {}".format(sf[0], sf[1]))
        scale_operator(plot, sf[0], float(sf[1]))

    c = ROOT.TCanvas("c", "c", 2000, 1500)

    canvas_limits = [-10.0, 10.0]

    ROOT.gStyle.SetOptStat(0)

    margins = 0.11
    pad2 = ROOT.TPad("pad2", "20", 0.0, 0.0,1.0, 0.68)
    pad3 = ROOT.TPad("pad3", "20", 0.0, 0.68,1.0, 1.0)

    #pad3.SetLeftMargin(0.09)
    #pad3.SetTopMargin(0.18)
    pad2.SetLeftMargin(0.1)
    pad2.SetBottomMargin(0.2)
    pad3.SetBottomMargin(0.03)
    pad2.SetTopMargin(0.02)
    pad3.SetBottomMargin(0.01)

    pad2.SetFrameLineWidth(4)
    pad3.SetFrameLineWidth(4)



    #pad1.Draw()
    pad2.Draw()
    pad3.Draw()

    pad2.cd()

    import math as mt
    step = 0.5
    edges = [-1]
    for key in plot.keys():
        current = edges[-1]
        edges.append(mt.ceil(len(plot[key]["interval"])*0.3) + current)

    edges = array("f", edges)
            
            

    # h = ROOT.TH1F("labels", "labels", len(plot.keys()), -1, len(plot.keys()))
    h = ROOT.TH1F("labels", "labels", len(edges)-1, edges)
    for idx, i in enumerate(plot.keys()):
        label = i
        if i in poi_to_label.keys(): label = poi_to_label[i]
        h.GetXaxis().SetBinLabel(idx+1, label) 

    h.SetTitle("")
    h.SetMaximum(canvas_limits[1])
    h.SetMinimum(canvas_limits[0])
    h.SetLineColor(0)

    h.GetYaxis().SetTitle("Parameter value")
    h.GetYaxis().SetTitleFont(43)
    h.GetYaxis().SetTitleSize(50)
    h.GetYaxis().SetTitleOffset(0.9)
    h.GetXaxis().SetLabelFont(43)
    h.GetXaxis().SetLabelSize(30)
    h.GetYaxis().SetLabelFont(43)
    h.GetYaxis().SetLabelSize(40)

    h.GetXaxis().LabelsOption("v"); 
    h.GetYaxis().LabelsOption("v"); 


    # h.GetXaxis().SetLabelSize(0);
    h.GetXaxis().SetTickLength(0);
    h.GetYaxis().SetTickLength(0.01);

    # redraw the grid by hand as we have custom bin width 

    xmin, xmax = min(edges), max(edges)
    ymin, ymax = canvas_limits[0], canvas_limits[1]

    grid = []

    for i_ in edges:
        grid_line = ROOT.TLine(i_,ymin,i_,ymax)
        grid_line.SetLineWidth(1)
        grid_line.SetLineColor(ROOT.kGray+1)
        grid_line.SetLineStyle(2)
        grid.append(grid_line)

    lines, graphs, arrows, legend, legend_graphs, tex_names = convert_dict_to_objects(plot, h)

    l_ = ROOT.TLine(-1,0, edges[-1],0)
    l_.SetLineColor(ROOT.kGray)
    l_.SetLineWidth(3)


    h.Draw("Y+")
    l_.Draw()

    for gr in grid: gr.Draw("L same")
        
    for line in lines: line.Draw()
    for g in graphs: g.Draw("P same")
    for arr in arrows: arr.Draw()


    # draw ancillary

    tex = ROOT.TLatex(0.07, 0.2, "CMS")
    tex.SetTextFont(62)
    tex.SetTextSize(0.06)
    tex.SetLineWidth(2)
    tex.SetTextAngle(90)
    tex.SetNDC()
    tex.Draw()

    tex1 = ROOT.TLatex(0.07, 0.35,"Preliminary")
    tex1.SetTextFont(52)
    tex1.SetTextSize(0.06)
    tex1.SetLineWidth(2)
    tex1.SetTextAngle(90)
    tex1.SetNDC()
    tex1.Draw()

    tex3 = ROOT.TLatex(0.09, 0.2, "#sqrt{s} = 13 TeV, " + f"{lumi}" + " fb^{-1}, #Lambda = 1 TeV")
    tex3.SetTextFont(52)
    tex3.SetTextSize(0.04)
    tex3.SetLineWidth(2)
    tex3.SetTextAngle(90)
    tex3.SetNDC()
    tex3.Draw()


    # pad2.SetTicks()
    # pad2.SetGridx()

    #pad2.RedrawAxis()

    pad3.cd()


    # h2 = ROOT.TH1F("labels", "labels", len(plot.keys()), -1, len(plot.keys()))

    h2 = ROOT.TH1F("labels1", "labels1", len(edges)-1, edges)
    # for idx, i in enumerate(plot.keys()):
    #     h.GetXaxis().SetBinLabel(idx+1, poi_to_label[i]) 

    h2.SetTitle("")
    h2.GetYaxis().SetLabelSize(0)
    h2.GetXaxis().SetTickSize(0)
    h2.GetYaxis().SetTickSize(0)
    h2.GetXaxis().SetLabelSize(0)
    h2.SetMaximum(canvas_limits[1])
    h2.SetMinimum(canvas_limits[0])
    h2.SetLineColor(0)

    h2.Draw()

    for g1 in legend_graphs: g1.Draw("P same")
    for t in tex_names: t.Draw()



    # legend.Draw()

    c.Update()
    c.Draw()

    c.Print(f"{args.output}.png")
    c.Print(f"{args.output}.pdf")
