import ROOT
from copy import deepcopy
from itertools import combinations
import numpy as np
from scan import scanEFT

class HistoBuilder:
    
    def __init__(self):
        self.pois = []
        self.ppois = []
        self.shapes = {}
        self.rateParam = {}
        
        self.minimPoisValue = {}
        self.historyHistos = {}
         
        self.historySingleHistos = {}
        self.historyDoubleHistos = {}

        self.interest_poi_value = []

        self.scanUtil = scanEFT()
        
        # EFTNeg model shapes
        self.shNames = ["sm", "sm_lin_quad", "sm_lin_quad_mixed", "quad"]


    def getExpectedSigNames(self):

        l = ["sm"]
        for poi in self.pois:
            l.append("sm_lin_quad_" + poi.strip("k_"))
            l.append("quad_" + poi.strip("k_"))

        for ppair in self.ppois:
            l.append("sm_lin_quad_mixed_" + ppair[0].strip("k_") + "_" + ppair[1].strip("k_"))
            l.append("sm_lin_quad_mixed_" + ppair[1].strip("k_") + "_" + ppair[0].strip("k_"))

        return l
    
    def setInterestPOI(self, interestPOI):
        self.interestPOI = interestPOI
        self.scanUtil.setPOI(interestPOI)

    def setRateParam(self, rpn):
        for i in rpn: self.rateParam[i] = []

    def setPoi(self,  pois, interestPOI):
        self.pois = pois
        self.ppois = list(combinations(pois, 2))
        self.interestPOI = interestPOI
        self.scanUtil.setPOI(interestPOI)
        
    def setShapes(self, file):

        f = ROOT.TFile(file)
        for i in f.GetListOfKeys():
            name = i.GetName()
            self.shapes[name] = deepcopy(f.Get(name))
        
        f.Close()
        
        print("Initialized shapes in memory")
        
    def setScan(self, file, tree):
        self.file = file
        self.tree = tree

        self.scanUtil.setFile(file)
        self.scanUtil.setTree(tree)

        # Now load all the EFT parameters

        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)

        self.pois = [ i.GetName() for i in t.GetListOfBranches() if i.GetName().startswith("k_") ]
        #if hasattr(self, "interestPOI"):
        #    self.pois = [i for i in self.pois if i != self.interestPOI]

        c = dict.fromkeys(self.pois)
        self.pois = c.keys()

        self.ppois = list(combinations(self.pois, 2))

        f.Close()

        print("Initialized LL scan in memory")

    def setScanMaxNLL(self, max=5):
        self.scanUtil.setupperNLLimit(max)
        
    def returnShapes(self):
        return self.shapes
    
    def getScan(self):
        
        gs = self.scanUtil.getScan()

        return gs
        
    def computeSingles(self, poiVal):
        
        self.historySingleHistos[poiVal] = {}
        
        #sm 
        sm_bench = deepcopy(self.shapes["histo_sm"])

        fact = 1
        poi_sum = 0
        poiPair_sum = 0
        for poi in self.pois:
            poi_sum +=  self.minimPoisValue[poi]

        fact -= poi_sum

        for pois in self.ppois:
            poiPair_sum += self.minimPoisValue[pois[0]]*self.minimPoisValue[pois[1]]

        fact += poiPair_sum

        sm_bench.Scale(fact)
        
        self.historySingleHistos[poiVal]["SM"] = sm_bench
        
        #sm + li + qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_sm_lin_quad_" + poi.strip("k_")])
            poiVal = self.minimPoisValue[poi]
            fact = poiVal
            for  j in self.pois:
                if j != poi:
                    fact -= poiVal * self.minimPoisValue[j]

            h.Scale(fact)
            self.historySingleHistos[poiVal]["sm_lin_quad_"+ poi.strip("k_")] = h
            

        #qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_quad_" + poi.strip("k_")])
            h.Scale(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi])
            self.historySingleHistos[poiVal]["quad_"+ poi.strip("k_")] = h            
        
        
    def compute(self, poiInterest):
        
        self.historySingleHistos[poiInterest] = {}
        #sm 
        bench = deepcopy(self.shapes["histo_sm"])

        fact = 1
        poi_sum = 0
        poiPair_sum = 0
        for poi in self.pois:
            poi_sum +=  self.minimPoisValue[poi]

        fact -= poi_sum

        for pois in self.ppois:
            poiPair_sum += self.minimPoisValue[pois[0]]*self.minimPoisValue[pois[1]]

        fact += poiPair_sum

        bench.Scale(fact)
        self.historySingleHistos[poiInterest]["SM"] = deepcopy(bench)


        #sm + li + qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_sm_lin_quad_" + poi.strip("k_")])
            poiVal = self.minimPoisValue[poi]
            fact = poiVal
            for  j in self.pois:
                if j != poi:
                    fact -= poiVal * self.minimPoisValue[j]

            h.Scale(fact)
            self.historySingleHistos[poiInterest]["sm_lin_quad_"+ poi.strip("k_")] = h
            bench.Add(h)

        #qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_quad_" + poi.strip("k_")])
            h.Scale(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi])
            self.historySingleHistos[poiInterest]["quad_"+ poi.strip("k_")] = h
            
            bench.Add(h)
        
        #mixed
        for ppair in self.ppois:

            name = "histo_sm_lin_quad_mixed_" + ppair[0].strip("k_") + "_" + ppair[1].strip("k_")

            if name not in  self.shapes.keys():
                name = "histo_sm_lin_quad_mixed_" + ppair[1].strip("k_") + "_" + ppair[0].strip("k_")

                if name not in  self.shapes.keys():
                    print ("No shape for {} {}".format(ppair[0], ppair[1]))
                    continue

            h = deepcopy(self.shapes[name])
            fact = self.minimPoisValue[ppair[0]] * self.minimPoisValue[ppair[1]]
            h.Scale(fact)
            self.historySingleHistos[poiInterest][name.split("histo_")[1]] = h

            bench.Add(h)


        #print(bench.Integral(), self.shapes["histo_sm"].Integral())
        if bench.GetMinimum() < 0:
            print ("foundBin < 0" + str(bench.GetMinimum()) )
            
        return bench

        

    def runHistoryEFTNeg(self):
        
        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)
        
        print([i.GetName() for i in t.GetListOfBranches()])
        print(t.GetEntries())
        
        for event in t:
            for poi in self.pois:
                self.minimPoisValue[poi] = getattr(event, poi)
            for key in self.rateParam.keys():
                self.rateParam[key].append(getattr(event, key))
            
            poiVal = getattr(event, self.interestPOI)
            self.interest_poi_value.append(poiVal)
            histo = self.compute(poiVal)
            
            self.historyHistos[poiVal] = histo
                
    
    def returnInterestPOIValues(self):
        return self.interest_poi_value

    def returnHistory(self):
        self.historyHistos["sm"] = self.shapes["histo_sm"]
        return self.historyHistos
    
    def returnComponentHistory(self):
        self.historySingleHistos["sm"] = self.shapes["histo_sm"]
        return self.historySingleHistos

    def returnRateParams(self):
        return self.rateParam