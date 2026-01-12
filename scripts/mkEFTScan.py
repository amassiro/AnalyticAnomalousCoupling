#!/usr/bin/env python3
import argparse
import ROOT
import os
import sys
from HiggsAnalysis.AnalyticAnomalousCoupling.utils.scan import scanEFT

def getBestFit(graphScan):
    xings = []
    n = graphScan.GetN ()
    x = list(graphScan.GetX ())
    y = list(graphScan.GetY ())
    x, y = zip(*sorted(zip(x, y)))
    found = False

    # get best fit --> min value on y -2DeltaNLL
    y_b, x_b = zip(*sorted(zip(y, x)))

    x_b = x_b[0]

    return x_b 

def getLSintersections (graphScan, val):

    xings = []
    n = graphScan.GetN ()
    x = list(graphScan.GetX ())
    y = list(graphScan.GetY ())
    x, y = zip(*sorted(zip(x, y)))
    found = False

    for i in range(n):
        if (y[i] == val):
            xings.append(x[i])
            continue
        if i > 0:
            if ((y[i] - val) * (y[i-1] - val) < 0):
                xings.append(x[i-1] +  abs ((y[i-1] - val) * (x[i] - x[i-1]) / (y[i] - y[i-1])) )

    if len(xings) == 0:
        print("@ @ @ WARNING @ @ @: returning graph x-axis range limits")
        xings.append(graphScan.GetXaxis ().GetXmin ())
        xings.append(graphScan.GetXaxis ().GetXmax ())

    elif len(xings) == 1:
        if (xings[0] < 0):
            print("@ @ @ WARNING @ @ @: returning graph x-axis higher limit")
            xings.append(graphScan.GetXaxis().GetXmax ())
        else :
            print("@ @ @ WARNING @ @ @: returning graph x-axis lower limit")
            xings.append (xings[0])
            xings[0] = graphScan.GetXaxis ().GetXmin ()

    if len(xings) > 2:
        print("@ @ @ WARNING @ @ @: more than two intersections found, returning the first two")
        xings = xings[:2]

    return xings

def getLabel():

    tex = ROOT.TLatex(0.55, .92, "AnalyticAnomalousCoupling")
    tex.SetNDC()
    tex.SetTextSize(0.76 * 0.05)
    tex.SetTextFont(52)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextAlign(31)

    return tex


def getLumi(lumi, energy=13):

    tex = ROOT.TLatex(0.88, .92, "{} ".format(lumi) +
                      "fb^{-1}" + " ({} TeV)".format(energy))
    tex.SetNDC()
    tex.SetTextAlign(31)
    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.SetLineWidth(2)

    return tex


def getCMS():

    tex = ROOT.TLatex(0.22, .92, "CMS")
    tex.SetNDC()
    tex.SetTextFont(61)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.SetTextAlign(31)

    return tex


def getPreliminary():

    tex = ROOT.TLatex(0.42, .92, "Preliminary")
    tex.SetNDC()
    tex.SetTextSize(0.76 * 0.05)
    tex.SetTextFont(52)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextAlign(31)

    return tex


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='This script allows to draw different gif plots for profiled EFT Fits using AnalyticalAnomalousCoupling')

    parser.add_argument('-p', '--POI',   dest='POI',     help='POIs to be plotted, default is \"r\"',
                        required=False, default="r", type=str, nargs="+")
    parser.add_argument('-maxNLL', '--maxNLL',   dest='maxNLL',
                        help='Set the maximum of the NLL to be plotted, default is 5 (-2deltaNLL=10)', required=False, default=5, type=float)
    parser.add_argument('-o', '--output',   dest='output',
                        help='Path + filename + filetype for output. Default is scan.pdf', required=False, default="scan.pdf", type=str)
    parser.add_argument('-lumi', '--lumi',   dest='lumi',
                        help='Draw this luminosity on the pad', required=False, default="", type=str)
    parser.add_argument('-xlabel', '--xlabel',   dest='xlabel',
                        help='Fancy xlabel for the scan', required=False, default="", type=str)
    parser.add_argument('-ylabel', '--ylabel',   dest='ylabel',
                        help='Fancy ylabel for the scan', required=False, default="", type=str)
    parser.add_argument('-energy', '--energy',   dest='energy',
                        help='Draw this energy on the pad, default 13 TeV', required=False, default=13, type=float)
    parser.add_argument('-cms', '--cms',   dest='cms',     help='Add cms label on top left',
                        required=False, default=False, action="store_true")
    parser.add_argument('-preliminary', '--preliminary',   dest='preliminary',
                        help='Add preliminary label on top left', required=False, default=False, action="store_true")
    parser.add_argument('-isNuis', '--isNuis',   dest='isNuis',
                        help='Option for a 3d draw with 2 POI on x-y and -2DeltaNLL on z. Useful if x is POI and y is a nuisance', required=False, default=False, action="store_true")
    parser.add_argument('-others', '--others',   dest='others',
                        help='Other scans on the same POI with <file>:<color int>:<linestyle int>:<label>', required=False, default=[], nargs="+")
    parser.add_argument('-ml', '--main-label',   dest='main_label',
                        help='Main label for the plot. If not given no legend included', required=False, type=str)
    parser.add_argument('-ff', '--fileFormat',   dest='fileFormat',
                        help='The format for the output default is png and pdf', required=False, default=["png", "pdf"], nargs="+")
    parser.add_argument('-lh', '--hidelegend',   dest='hidelegend',
                        help='Do not plot the legend on the canvas', required=False, default=False, action="store_true")
    args, _ = parser.parse_known_args()

    if len(sys.argv) < 2:
        print("[ERROR] Usage python mkEFTScan.py <path_to_scan> -maxNLL (5) -lumi (\"\") -energy (13) -cms (False) -preliminary (False)")
        sys.exit(0)

    if len(args.POI) > 2:
        print("[ERROR] Specified {} operators to be plotted but only 2 are supported for plotting purposes".format(
            len(args.POI)))

    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0000)

    scan = sys.argv[1]

    if len(args.POI) == 1:
        pois = args.POI[0]
    else:
        pois = args.POI

    # 2d fits line styles for 68 and 95
    linestyle = [1, 7]

    scanUtil = scanEFT()
    scanUtil.setFile(scan)
    scanUtil.setTree("limit")
    scanUtil.setPOI(pois)
    scanUtil.setupperNLLimit(args.maxNLL)
    scanUtil.setNuisanceStyle(args.isNuis)

    gs = scanUtil.getScan()
    x_b = getBestFit(gs)
    xings1s = getLSintersections(gs, 1.0)
    xings2s = getLSintersections(gs, 1.0)
    print(f"Main scan 68.27% C.L (1 s.d.)  {pois}<1: {xings1s} --> {x_b:.3f}+{abs(xings1s[1]-x_b):.3f}-{abs(x_b-xings1s[0]):.3f}")
    print(f"Main scan 95.45% C.L (2 s.d.)  {pois}<4: {xings2s} --> {x_b:.3f}+{abs(xings2s[1]-x_b):.3f}-{abs(x_b-xings2s[0]):.3f}")
    others = []
    labels = []
    if len(args.others) != 0:

        for file_, color_, line_, label_ in [i.split(":") for i in args.others]:
            scanUtil_ = scanEFT()
            scanUtil_.setFile(file_)
            scanUtil_.setTree("limit")
            scanUtil_.setPOI(pois)
            scanUtil_.setupperNLLimit(args.maxNLL)
            scanUtil_.setNuisanceStyle(args.isNuis)
            gs_ = scanUtil_.getScan()
            x_b_ = getBestFit(gs_)
            xings1s_ = getLSintersections(gs_, 1.0)
            xings2s_ = getLSintersections(gs_, 1.0)
            print(f"{label_} scan 68.27% C.L (1 s.d.)  {pois}<1: {xings1s_} --> {x_b_:.3f}+{abs(xings1s_[1]-x_b_):.3f}-{abs(x_b_-xings1s_[0]):.3f}")
            print(f"{label_} scan 95.45% C.L (2 s.d.)  {pois}<4: {xings2s_} --> {x_b_:.3f}+{abs(xings2s_[1]-x_b_):.3f}-{abs(x_b_-xings2s_[0]):.3f}")
            gs_.SetLineWidth(4)
            gs_.SetLineColor(int(color_))
            gs_.SetLineStyle(int(line_))
            if isinstance(pois, str):
                others.append(gs_)
                labels.append(label_)
            else:
                for levelIdx, _ in enumerate([68, 95]):
                    # if scan is not close then we will have different graphs
                    for graphIdx in range(len(scanUtil_.contours[levelIdx])):
                        scanUtil_.contours[levelIdx][graphIdx].SetLineStyle(
                            linestyle[levelIdx])
                        scanUtil_.contours[levelIdx][graphIdx].SetLineColor(
                            int(color_))
                        scanUtil_.contours[levelIdx][graphIdx].SetLineWidth(3)
                others.append(scanUtil_.contours)
                labels.append(label_)

            # gs.Draw("L same")

    margins = 0.13
    if args.xlabel:
        gs.GetXaxis().SetTitle(args.xlabel)
    if args.ylabel:
        gs.GetYaxis().SetTitle(args.ylabel)

    c = ROOT.TCanvas("c", "c", 1000, 1000)

    leg = ROOT.TLegend(0.85, 0.85, 0.6, 0.7)
    leg.SetBorderSize(0)

    ROOT.gPad.SetFrameLineWidth(3)

    if len(args.POI) == 1:
        ROOT.gPad.SetRightMargin(margins)
    elif len(args.POI) == 2:
        ROOT.gPad.SetRightMargin(0.15)

    ROOT.gPad.SetBottomMargin(margins)
    ROOT.gPad.SetLeftMargin(margins)

    ROOT.gPad.SetTicks()

    if len(args.POI) == 1:

        gs.SetLineWidth(4)
        gs.SetLineColor(ROOT.kBlack)

        if args.xlabel:
            gs.GetXaxis().SetTitle(args.xlabel)
        gs.GetXaxis().SetTitleSize(0.05)
        gs.GetYaxis().SetTitleSize(0.05)
        gs.GetXaxis().SetTitleOffset(1.1)

        gs.Draw("AL")

        if args.main_label:
            leg.AddEntry(gs, args.main_label, "L")

        for g, l in zip(others, labels):
            g.Draw("L same")
            leg.AddEntry(g, l, "L")

        min_x, max_x = gs.GetXaxis().GetXmin(), gs.GetXaxis().GetXmax()

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
        ois.DrawLatex(x_frac, 1.05, '68%')
        tis = ROOT.TLatex()
        tis.SetTextFont(42)
        tis.SetTextSize(0.03)
        tis.DrawLatex(x_frac, 3.89, '95%')

        if args.main_label and not args.hidelegend:
            leg.Draw()

    elif len(args.POI) == 2:

        exp = ROOT.TGraph()
        exp.SetPoint(0, 0, 0)
        exp.SetMarkerStyle(34)
        exp.SetMarkerSize(2)
        exp.SetMarkerColor(ROOT.kRed)

        xl = pois[0]
        yl = pois[1]
        if args.xlabel:
            xl = args.xlabel
        if args.ylabel:
            yl = args.ylabel

        # gs.GetZaxis().SetTitle("-2 #Delta LL")
        # gs.GetZaxis().SetTitleOffset(0.8)
        gs.GetHistogram().GetZaxis().SetTitle("-2 #Delta lnL")
        gs.GetHistogram().GetZaxis().SetTitleOffset(1)
        gs.GetHistogram().GetZaxis().SetTitleSize(0.04)

        gs.GetHistogram().GetXaxis().SetTitle(xl)
        gs.GetHistogram().GetXaxis().SetTitleOffset(1)
        gs.GetHistogram().GetXaxis().SetTitleSize(0.045)

        gs.GetHistogram().GetYaxis().SetTitle(yl)
        gs.GetHistogram().GetYaxis().SetTitleOffset(1)
        gs.GetHistogram().GetYaxis().SetTitleSize(0.045)

        gs.GetHistogram().GetXaxis().SetLabelSize(0.041)
        gs.GetHistogram().GetYaxis().SetLabelSize(0.041)

        leg = ROOT.TLegend(0.82, 0.85, 0.67, 0.7)
        leg.AddEntry(exp, "Expected", "P")
        leg.SetBorderSize(0)

        if args.isNuis:
            gs.SetNpx(200)
            gs.SetNpy(200)

            hist = gs.GetHistogram().Clone("arb_hist")

            for i in range(hist.GetSize()):
                hist.SetBinContent(i+1, 0)

            for i in range(gs.GetN()):
                hist.Fill(gs.GetX()[i],  gs.GetY()[i],  gs.GetZ()[i] + 0.001)

            hist.GetXaxis().SetTitle(xl)
            hist.GetYaxis().SetTitle(yl)
            # hist.GetZaxis().SetTitle("-2 #Delta LL")

            hist.GetYaxis().SetTitleOffset(1.7)
            hist.GetXaxis().SetTitleOffset(1.4)
            # hist.GetZaxis().SetTitleOffset(0.8)

            hist.GetXaxis().SetTitleSize(0.04)
            hist.GetYaxis().SetTitleSize(0.04)

            hist.GetZaxis().SetRangeUser(0, float(args.maxNLL))

            hist.SetTitle("")
            hist.Draw("colz")

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

        elif len(args.others) > 0:

            # first of all, set the main 2d plot to white
            # all bin contents to 0
            for i in range(gs.GetHistogram().GetSize()):
                gs.GetHistogram().SetBinContent(i+1, 0)

            gs.GetXaxis().SetTitle(xl)
            gs.GetYaxis().SetTitle(yl)

            gs.GetYaxis().SetTitleOffset(1.4)
            gs.GetXaxis().SetTitleOffset(1.1)

            gs.GetHistogram().SetTitle("")

            # plot axes only
            gs.Draw("hist")

            # there are two levels 68 and 95 %
            # same color will be applied but
            # different linestyle

            # first draw the main
            for idx, _ in enumerate([68, 95]):
                levelContours = scanUtil.contours[idx]
                # if scan is not close then we will have different graphs
                for graph in levelContours:
                    graph.SetLineStyle(linestyle[idx])
                    graph.SetLineColor(ROOT.kBlack)
                    graph.SetLineWidth(3)

                    graph.Draw("L same")

            if args.main_label:
                # always present
                leg.AddEntry(scanUtil.contours[0][0], args.main_label, "L")

            for other, label in zip(others, labels):
                for idx, _ in enumerate([68, 95]):
                    levelContours = other[idx]
                    # if scan is not close then we will have different graphs
                    for graph in levelContours:
                        graph.Draw("L same")
                leg.AddEntry(other[0][0], label, "L")

            exp.Draw("P same")
            if not args.hidelegend:
                leg.Draw()

        else:

            for i in range(gs.GetHistogram().GetSize()):
                if (gs.GetHistogram().GetBinContent(i+1) == 0):
                    gs.GetHistogram().SetBinContent(i+1, 100)

            gs.GetXaxis().SetTitle(xl)
            gs.GetYaxis().SetTitle(yl)

            gs.GetYaxis().SetTitleOffset(1.4)
            gs.GetXaxis().SetTitleOffset(1.1)

            gs.GetZaxis().SetRangeUser(0, float(args.maxNLL))
            gs.GetHistogram().GetZaxis().SetRangeUser(0, float(args.maxNLL))

            gs.GetHistogram().SetTitle("")
            gs.GetHistogram().Draw("colz")

            # conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
            # cont_graphs = [conts.At(i) for i in range(len(conts))]

            colors = [ROOT.kRed, ROOT.kRed]

            for i, item_ in enumerate(scanUtil.contours):
                # item_ here is a TList
                l = list(item_)
                for item in l:
                    try:
                        item.SetLineColor(colors[i])
                        item.SetLineStyle(linestyle[i])
                        item.SetLineWidth(2)
                        item.Draw("L same")
                    except:
                        continue
                # only add one legend entry, arbitrary
                if len(l) > 0:
                    leg.AddEntry(l[0], "#pm {} s.d.".format(i+1), "L")

            exp.Draw("P same")
            if not args.hidelegend:
                leg.Draw()

        c.Modified()
        c.Update()

    if not args.cms:
        tex = getLabel()
        tex.Draw()
    else:
        tex = getCMS()
        tex.Draw()
        if args.preliminary:
            tex2 = getPreliminary()
            tex2.Draw()

    if args.lumi:
        tex3 = getLumi(args.lumi)
        tex3.Draw()

    c.Draw()
    for ff_ in args.fileFormat:
        if ff_ == "root": continue
        c.Print(args.output + "." + ff_)

    if "root" in args.fileFormat:
        f = ROOT.TFile(args.output + ".root", "RECREATE")

        name = "Main" if not args.main_label else args.main_label
        gs.Write(name)

        for g, l in zip(others, labels):
            g.Write(l)

        if len(args.POI) == 2:

            # first draw the main
            for idx, level in enumerate([68, 95]):
                levelContours = scanUtil.contours[idx]
                # if scan is not close then we will have different graphs
                for graph in levelContours:
                    graph.Write(name + "_" + str(level))

            for other, label in zip(others, labels):
                for idx, level in enumerate([68, 95]):
                    levelContours = other[idx]
                    # if scan is not close then we will have different graphs
                    for graph in levelContours:
                        graph.Write(label + "_" + str(level))        
