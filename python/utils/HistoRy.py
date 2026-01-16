import ROOT
from copy import deepcopy
from itertools import combinations
import numpy as np
from HiggsAnalysis.AnalyticAnomalousCoupling.utils.scan import scanEFT
import sys 

class HistoBuilder:
    
    def __init__(self):
        self.pois = []
        self.ppois = []
        self.has_r_SignalStrength = False
        self.shapes = {}
        self.rateParam = {}
        
        self.minimPoisValue = {}
        self.historyHistos = {}
         
        self.historySingleHistos = {}
        self.historyDoubleHistos = {}

        self.interest_poi_value = []
        
        self.prefix = "histo_"

        self.scanUtil = scanEFT()
        
        # EFTNeg model shapes
        self.shNames = ["sm", "sm_lin_quad", "sm_lin_quad_mixed", "quad"]

    @staticmethod
    def parsePOIs(pois):
        if type(pois) == str:
            return pois
        elif type(pois) == list and len(pois) == 1:
            return pois[0]
        elif type(pois) == list and len(pois) > 1:
            return pois
        else:
            print("POIs not recognized")
            return None
            
    def setPrefix(self, prefix):
        self.prefix = prefix
        # if you do this after loading shapes we can check 
        if self.shapes:
            if self.prefix + "sm" not in self.shapes.keys():
                # need to fix this  
                for key in list(self.shapes.keys()):
                    if key.startswith(self.prefix) and key.endswith("_sm"):
                        self.prefix = key.split("sm")[0]
                        print("[WARNNG] REDEFINED PREFIX TO {}".format(self.prefix))
                        break 
        
    def getExpectedSigNames(self):
        
        l = [self.prefix + "sm"]
        for poi in self.pois:
            l.append(self.prefix + "sm_lin_quad_" + poi.strip("k_"))
            l.append(self.prefix + "quad_" + poi.strip("k_"))

        for ppair in self.ppois:
            l.append(self.prefix + "sm_lin_quad_mixed_" + ppair[0].strip("k_") + "_" + ppair[1].strip("k_"))
            l.append(self.prefix + "sm_lin_quad_mixed_" + ppair[1].strip("k_") + "_" + ppair[0].strip("k_"))

        return l
    
    def setInterestPOI(self, interestPOI):
        self.interestPOI = interestPOI
        self.scanUtil.setPOI(HistoBuilder.parsePOIs(interestPOI))

    def setRateParam(self, rpn):
        for i in rpn: self.rateParam[i] = []

    def setPoi(self,  pois):
        self.pois = pois
        self.ppois = list(combinations(pois, 2))
        self.interestPOI = pois
        self.scanUtil.setPOI(HistoBuilder.parsePOIs(pois))
        
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
        self.scanUtil.setPOI(HistoBuilder.parsePOIs(self.pois))

        # if also "r" was let free to float, also add it to the list of pois
        if "r" in [ i.GetName() for i in t.GetListOfBranches() ]: self.has_r_SignalStrength = True


        #c = dict.fromkeys(self.pois)
        #self.pois = c.keys()

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
        sm_bench = deepcopy(self.shapes[self.prefix + "sm"])

        fact = 1
        poi_sum = 0
        poiPair_sum = 0
        for poi in self.pois:
            poi_sum +=  self.minimPoisValue[poi]

        fact -= poi_sum

        for pois in self.ppois:
            poiPair_sum += self.minimPoisValue[pois[0]]*self.minimPoisValue[pois[1]]

        fact += poiPair_sum
        fact *= self.minimPoisValue["r"]

        sm_bench.Scale(fact)
        
        self.historySingleHistos[poiVal]["SM"] = sm_bench
        
        #sm + li + qu
        for poi in self.pois:
            h = deepcopy(self.shapes[self.prefix + "sm_lin_quad_" + poi.strip("k_")])
            poiVal = self.minimPoisValue[poi]
            fact = poiVal
            for  j in self.pois:
                if j != poi:
                    fact -= poiVal * self.minimPoisValue[j]

            fact *= self.minimPoisValue["r"]

            h.Scale(fact)
            self.historySingleHistos[poiVal]["sm_lin_quad_"+ poi.strip("k_")] = h
            

        #qu
        for poi in self.pois:
            h = deepcopy(self.shapes[self.prefix + "quad_" + poi.strip("k_")])
            h.Scale( self.minimPoisValue["r"]*(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi]) )
            self.historySingleHistos[poiVal]["quad_"+ poi.strip("k_")] = h            
        
        
    def compute(self, poiInterest):
        
        print("#####################")
        print(poiInterest)
        print("#####################")
        print(self.minimPoisValue)
        print("#####################")
        
        if isinstance(poiInterest, dict):
            poiInterest = "_".join([f"{i}_{j}".replace(".","p").replace("-","m") for i,j in poiInterest.items()])
            
        self.historySingleHistos[poiInterest] = {}
        #sm 
        bench = deepcopy(self.shapes[self.prefix + "sm"])

        fact = 1
        poi_sum = 0
        poiPair_sum = 0
        for poi in self.pois:
            poi_sum +=  self.minimPoisValue[poi]

        fact -= poi_sum

        for pois in self.ppois:
            poiPair_sum += self.minimPoisValue[pois[0]]*self.minimPoisValue[pois[1]]

        fact += poiPair_sum
        fact *= self.minimPoisValue["r"]

        print("--> SM fact " + str(fact))

        bench.Scale(fact)
        self.historySingleHistos[poiInterest]["SM"] = deepcopy(bench)


        #sm + li + qu
        for poi in self.pois:
            h = deepcopy(self.shapes[self.prefix + "sm_lin_quad_" + poi.strip("k_")])
            poiVal = self.minimPoisValue[poi]
            fact = poiVal
            for  j in self.pois:
                if j != poi:
                    fact -= poiVal * self.minimPoisValue[j]

            fact*=self.minimPoisValue["r"]

            print("--> Sm li qu {} fact ".format(poi) + str(fact))

            h.Scale(fact)
            self.historySingleHistos[poiInterest]["sm_lin_quad_"+ poi.strip("k_")] = h
            bench.Add(h)

        #qu
        for poi in self.pois:
            h = deepcopy(self.shapes[self.prefix + "quad_" + poi.strip("k_")])
            print("--> qu {} fact ".format(poi) + str(self.minimPoisValue["r"]*(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi])))
            h.Scale( self.minimPoisValue["r"]*(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi]) )
            self.historySingleHistos[poiInterest]["quad_"+ poi.strip("k_")] = h
            
            bench.Add(h)
        
        #mixed
        for ppair in self.ppois:

            name = self.prefix + "sm_lin_quad_mixed_" + ppair[0].strip("k_") + "_" + ppair[1].strip("k_")

            if name not in  self.shapes.keys():
                name = self.prefix + "sm_lin_quad_mixed_" + ppair[1].strip("k_") + "_" + ppair[0].strip("k_")

                if name not in  self.shapes.keys():
                    print ("No shape for {} {}".format(ppair[0], ppair[1]))
                    continue

            h = deepcopy(self.shapes[name])
            fact = self.minimPoisValue["r"] * self.minimPoisValue[ppair[0]] * self.minimPoisValue[ppair[1]]

            print("--> mixed {} {} fact ".format(ppair[0], ppair[1]) + str(fact))

            h.Scale(fact)
            self.historySingleHistos[poiInterest][name.split(self.prefix + "")[1]] = h

            bench.Add(h)


        #print(bench.Integral(), self.shapes[self.prefix + "sm"].Integral())
        if bench.GetMinimum() < 0:
            print ("foundBin < 0" + str(bench.GetMinimum()) )
            
        return bench

        

    def runHistoryEFTNeg(self):
        
        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)
            
        for event in t:
            
            for poi in self.pois:
                self.minimPoisValue[poi] = getattr(event, poi)
            for key in self.rateParam.keys():
                self.rateParam[key].append(getattr(event, key))

            self.minimPoisValue["r"] = 1 if not self.has_r_SignalStrength else getattr(event, "r")
            
            if len(self.pois) == 1:
                poiVal = getattr(event, self.pois[0])
                
                self.interest_poi_value.append(poiVal)
                histo = self.compute(poiVal)
                
                self.historyHistos[poiVal] = histo
                
            else:
                print("SONO QUI")
                poiVal = {i: getattr(event, i) for i in self.pois}
                name = "_".join([f"{i}_{j}".replace(".","p").replace("-","m") for i,j in poiVal.items()])
                
                self.interest_poi_value.append(poiVal)
                histo = self.compute(poiVal)
                
                self.historyHistos[name] = histo
                
    
    def returnInterestPOIValues(self):
        return self.interest_poi_value

    def returnHistory(self):
        self.historyHistos["sm"] = self.shapes[self.prefix + "sm"]
        return self.historyHistos
    
    def returnComponentHistory(self):
        self.historySingleHistos["sm"] = self.shapes[self.prefix + "sm"]
        return self.historySingleHistos

    def returnRateParams(self):
        return self.rateParam
