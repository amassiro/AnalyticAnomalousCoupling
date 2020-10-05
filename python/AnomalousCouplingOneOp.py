from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class AnaliticAnomalousCouplingOneOp(PhysicsModel):

#
# standard, not touched
#

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.mHRange = po.replace("higgsMassRange=","").split(",")
                if len(self.mHRange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema"
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"

#
# standard, not touched (end)
#


#
# Define parameters of interest
#

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        
        # trilinear Higgs couplings modified 
        self.modelBuilder.doVar("k_my[1,-200,200]")
        self.poiNames = "k_my"

        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames += ",r"

        #
        # model: SM + k*linear + k**2 * quadratic
        #
        #   SM        = Asm**2
        #   linear    = Asm*Absm
        #   quadratic = Absm**2
        
        self.modelBuilder.factory_("expr::sm_func(\"@0\",r)")
        self.modelBuilder.factory_("expr::linear_func(\"@0*@1\",r,k_my)")
        self.modelBuilder.factory_("expr::quadratic_func(\"@0*@1*@1\",r,k_my)")

        print self.poiNames
        self.modelBuilder.doSet("POI",self.poiNames)


#
# Define how the yields change
#


    def getYieldScale(self,bin,process):


        if process == "sm":          return "sm_func"
        elif process == "linear":    return "linear_func"
        elif process == "quadratic": return "quadratic_func"
        else:
          return 1



analiticAnomalousCouplingOneOp = AnaliticAnomalousCouplingOneOp()


