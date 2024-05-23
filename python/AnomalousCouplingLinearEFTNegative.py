from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

#
# See derivation and explanation, validation, tests in AN-20-204
#

#
# Consider only linear component:
# beware that the model now is not by construction non-negative defined, since SM+lin is not given to be non-negative
# thus analyser should make sure that at coupling set to 1 the SM+Lin is not negative.
# alternatively the analyser should give as input SM+l*Lin, with "l" chosen such that it is not-negative the sum
# for every bin. It's up to the analyser then scale accordingly the likelihood scan
#

class AnaliticAnomalousCouplingLinearEFTNegative(PhysicsModel):

    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
        self.numOperators = 82
        self.reuseCompleteDatacards = False
        self.addDim8 = False
        self.OperatorsDim8 = [
             # dimension 8
             'cS0',
             'cS1',
             'cM0',
             'cM1',
             'cM2',
             'cM3',
             'cM4',
             'cM6',
             'cM7',
             'cT0',
             'cT1',
             'cT2',
             'cT3',
             'cT4',
             'cT6',
             'cT7',
             'cT8',
             'cT9',             
        ]
        
        # NB: alphabetically sorted, do not reshuffle
        self.Operators = [
             # dimension 6
             'cG',
             'cGtil',
             'cH',
             'cHB',
             'cHBtil',
             'cHDD',
             'cHG',
             'cHGtil',
             'cHW',
             'cHWB',
             'cHWBtil',
             'cHWtil',
             'cHbox',
             'cHd',
             'cHe',
             'cHl1',
             'cHl3',
             'cHq1',
             'cHq3',
             'cHu',
             'cHudAbs',
             'cHudPh',
             'cW',
             'cWtil',
             'cdBAbs',
             'cdBPh',
             'cdGAbs',
             'cdGPh',
             'cdHAbs',
             'cdHPh',
             'cdWAbs',
             'cdWPh',
             'cdd',
             'cdd1',
             'ceBAbs',
             'ceBPh',
             'ceHAbs',
             'ceHPh',
             'ceWAbs',
             'ceWPh',
             'ced',
             'cee',
             'ceu',
             'cld',
             'cle',
             'cledqAbs',
             'cledqPh',
             'clequ1Abs',
             'clequ1Ph',
             'clequ3Abs',
             'clequ3Ph',
             'cll',
             'cll1',
             'clq1',
             'clq3',
             'clu',
             'cqd1',
             'cqd8',
             'cqe',
             'cqq1',
             'cqq11',
             'cqq3',
             'cqq31',
             'cqu1',
             'cqu8',
             'cquqd1Abs',
             'cquqd1Ph',
             'cquqd8Abs',
             'cquqd8Ph',
             'cuBAbs',
             'cuBPh',
             'cuGAbs',
             'cuGPh',
             'cuHAbs',
             'cuHPh',
             'cuWAbs',
             'cuWPh',
             'cud1',
             'cud8',
             'cuu',
             'cuu1',
             'cjj11',
             'cjj18',
             'cjj31',
             'cjj38',
             'cHj1',
             'cHQ1'
             ]


        self.CompleteOperators = self.Operators + self.OperatorsDim8

        self.numOperators = len(self.Operators)

        print(" Operators = ", self.Operators)

        
        

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.mHRange = po.replace("higgsMassRange=","").split(",")
                if len(self.mHRange) != 2:
                    raise RuntimeError("Higgs mass range definition requires two extrema")
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError("Extrema for Higgs mass range defined with inverterd order. Second must be larger the first")

            if po.startswith("eftOperators="):
                self.Operators = po.replace("eftOperators=","").split(",")
                print(" Operators = ", self.Operators)
                self.numOperators = len(self.Operators)

            if po.startswith("addDim8"):
                self.Operators.extend ( self.OperatorsDim8 )
                self.addDim8 = True

            if po.startswith("reuseCompleteDatacards"):
                self.reuseCompleteDatacards = True
                print(" reuseCompleteDatacards = ", self.reuseCompleteDatacards)
                

#
# standard, not touched (end)
#


#
# Define parameters of interest
#

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # trilinear Higgs couplings modified
        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"


        for operator in range(0, self.numOperators):
          self.modelBuilder.doVar("k_" + str(self.Operators[operator]) + "[0,-200,200]")
          self.poiNames += ",k_" + str(self.Operators[operator])

        #
        # model: SM + k*linear
        #
        #   SM        = Asm**2
        #   linear    = Asm*Absm
        #   quadratic = Absm**2
        #
        #  ... and extended to more operators
        #
        #
        # model: SM + k*linear
        #
        #   SM        = Asm**2
        #   linear_1        = Asm*Abs_1
        #   linear_2        = Asm*Absm_2
        #
        #
        #  Combine limitation/assumption: all histograms are defined positive
        #      See http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/physicsmodels/#interference
        #  Workaround (but it's not 100% robust since the model, neglecting the quadratic term 
        #  is by construction NOT non-negative safe:
        #
        #   sm + lin
        #   sm
        #
        #     sm + k*lin
        #   = sm + k * (sm+lin-sm) 
        #   = sm *(1-k) + k*(sm+lin) 


        #
        # this is the coefficient of "SM"
        #


        if self.numOperators != 1:
          self.modelBuilder.factory_(
               "expr::func_sm(\"@0*(1-(" +
                                        "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +
                                        "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
               )
        else :
          self.modelBuilder.factory_(
               "expr::func_sm(\"@0*(1-(" +
                                        "@1" +
                                        "))\",r," + "k_" + str(self.Operators[0]) + ")"
               )


        #
        # A check to reuse complete datacards
        #
        if not self.reuseCompleteDatacards : 
          #
          # this is the coefficient of "SM + Lin_i"
          #
          
          for operator in range(0, self.numOperators):
            #
            self.modelBuilder.factory_(
                 "expr::func_sm_linear_"+ str(self.Operators[operator]) + 
                       "(\"@0*@1\",r," + "k_" + str(self.Operators[operator]) + ")"
                 )
        
        else :
          #
          # a bit of waste of resources and add/subtract components ... but it can help in reusing complete datacards  
          #
          #  sm+lin = sm+lin+quad - quad
          #
          #
          for operator in range(0, self.numOperators):
            #
            self.modelBuilder.factory_(
                 "expr::func_sm_linear_quadratic_"+ str(self.Operators[operator]) + 
                       "(\"@0*@1\",r," + "k_" + str(self.Operators[operator]) + ")"
                 )

          for operator in range(0, self.numOperators):
            #
            self.modelBuilder.factory_(
                 "expr::func_quadratic_"+ str(self.Operators[operator]) + 
                       "(\"-@0*@1\",r," + "k_" + str(self.Operators[operator]) + ")"
                 )
          
        print(" parameters of interest = ", self.poiNames)
        print(" self.numOperators = ", self.numOperators)
        
        self.modelBuilder.doSet("POI",self.poiNames)


#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        #print "process = " , process

        if   process == "sm" or "_sm" in process:          return "func_sm"

        for operator in range(0, self.numOperators):
          if process == "sm_lin_"+ str(self.Operators[operator]) or "_sm_lin_"+ str(self.Operators[operator]) in process:
            return "func_sm_linear_"+ str(self.Operators[operator])
          

        #
        # This will allow the usage of a datacard with quadratic and mixed component
        # with this simplified model:
        # all contributions are set to 0      ;)
        #
        # However, in the datacard we MUST have sm_lin_OPERATOR, that is not there in the complete model (the one with quadratic)!
        #
        #
        if "sm_lin_quad_mixed_" in process or "_sm_lin_quad_mixed_" in process: 
          return 0
        if not self.reuseCompleteDatacards : 
          if "sm_lin_quad_" in process or "_sm_lin_quad_" in process: 
            return 0
          if "quad_" in process: 
            return 0
        else :
          for operator in range(0, self.numOperators):
            if process == "sm_lin_quad_"+ str(self.Operators[operator]) or "_sm_lin_quad_"+ str(self.Operators[operator]) in process :
              return "func_sm_linear_quadratic_"+ str(self.Operators[operator])
            if process == "quad_"+ str(self.Operators[operator]) :           return "func_quadratic_"+ str(self.Operators[operator])
          
          
        #
        # sometimes we have complete datacards, with many operators, but we want to test 
        # a model just with few operators, 
        # for example if we need to combine a datacard with dependency only on 2 operators
        # with another that depends on 3 (thus having many more components).
        # If this is the case, compare the complete list of operators
        # and if any of them appear in the "process" then this process is scaled to 0
        # since it is NOT used by the model, and otherwise it would be treated as
        # a background, thus being a mistake!
        #
        for complete_list_of_operators in self.CompleteOperators:
          if complete_list_of_operators in process:
            return 0
            #
            # No need to remove the list in "Operators"
            # since if it was to be used there, the "return" would 
            # have been already called.
            # This option will be triggered only if no return was already called
            # and if not "return 0" we would have "return 1" underneath,
            # thus considering this as background
            # NB: the names in "CompleteOperators" are wild cards
            # and should not be used by other samples (real background!)
            # but, com'on, a bit of rules!
            #

        return 1


#
#  Inputs:
# 
#     S
#     S + Li
#  


analiticAnomalousCouplingLinearEFTNegative = AnaliticAnomalousCouplingLinearEFTNegative()
