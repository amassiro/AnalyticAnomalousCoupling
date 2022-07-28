import ROOT 
import numpy as np
from array import array
from copy import deepcopy

class scanEFT:

    def __init__(self):

        self.tree = "limit"
        self.upper = 5
        self.lower = -30

    def setFile(self, file):
        self.file = file 

    def setTree(self, tree):
        self.tree = tree 

    def setPOI(self, pois):
        self.poi = pois

    def setNLLimits(self, upper, lower):
        self.upper = upper 
        self.lower = lower

    def setupperNLLimit(self, upper):
        self.upper = upper 

    def setlowerNLLimit(self, lower):
        self.lower = lower 

    def getScan(self):
        
        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)
        
        if isinstance(self.poi, str):

            to_draw = ROOT.TString("2*deltaNLL:{}".format(self.poi))
            n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(self.upper,self.lower), "l")

            if n <= 1: 
                print("[ATTENTION] no likelihood for {}".format(self.poi))
                return


            x = np.ndarray((n), 'd', t.GetV2())[1:] #removing first element (0,0)
            y_ = np.ndarray((n), 'd', t.GetV1())[1:] #removing first element (0,0)

            x, ind = np.unique(x, return_index = True)
            y_ = y_[ind]
            y = np.array([i-min(y_) for i in y_]) #shifting likelihood toward 0

            graphScan = ROOT.TGraph(x.size,x,y)
            graphScan.GetXaxis().SetTitle(self.poi)
            graphScan.GetYaxis().SetTitle("-2#DeltaLL")
            graphScan.SetTitle("")
            graphScan.SetLineColor(ROOT.kRed)
            graphScan.SetLineWidth(2)
            
            f.Close()


            self.scan = graphScan

            return self.scan

        elif isinstance(self.poi, list):

            one_s_frac = 2.3 / self.upper
            two_s_frac = 5.99 / self.upper

            __stops = array('d', [0.00, one_s_frac, two_s_frac, 1])
            __red = array('d', [1.0, 1.0, 0.145, 0.0])
            __green  = array('d', [1.0, 0.549, 0.459, 0.0])
            __blue  = array('d', [1.0, 0.0, 1.0, 1.0])


            #ROOT.TColor.CreateGradientColorTable(3, __stops, __red, __green, __blue, 255)
            ROOT.TColor.CreateGradientColorTable(4, __stops,__red, __green, __blue, 50, 0.8)
            ROOT.gStyle.SetNumberContours(200)

            to_draw = ROOT.TString("{}:{}:2*deltaNLL".format(self.poi[0], self.poi[1]))
            n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(self.upper,self.lower), "l")

            if n <= 1: 
                print("[ATTENTION] no likelihood for {}".format(self.poi))
                return

            x = np.ndarray((n), 'd', t.GetV1())
            y = np.ndarray((n), 'd', t.GetV2())
            z_ = np.ndarray((n), 'd', t.GetV3())

            z = np.array([i-min(z_) for i in z_]) #shifting likelihood toward 0
            graphScan = ROOT.TGraph2D(n,x,y,z)

            graphScan.GetZaxis().SetTitle("-2 #Delta LL")
            graphScan.GetXaxis().SetTitle(self.poi[0])
            graphScan.GetYaxis().SetTitle(self.poi[1])
            graphScan.SetLineColor(ROOT.kRed)
            graphScan.SetLineWidth(2)

            graphScan.GetZaxis().SetRangeUser(0, self.upper)
            graphScan.GetHistogram().GetZaxis().SetRangeUser(0, self.upper)

            for i in range(graphScan.GetHistogram().GetSize()):
                if (graphScan.GetHistogram().GetBinContent(i+1) == 0):
                    graphScan.GetHistogram().SetBinContent(i+1, 100)

            hist = graphScan.GetHistogram().Clone("arb_hist")
            hist.SetContour(2, np.array([2.30, 5.99]))
            hist.Draw("CONT Z LIST")
            ROOT.gPad.Update()

            self.contours = deepcopy(hist) 
            self.scan = deepcopy(graphScan)

            f.Close()

            return self.scan


