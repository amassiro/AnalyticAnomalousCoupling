from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class AnaliticAnomalousCouplingEFTNegative(PhysicsModel):

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
        self.numOperators = 82
        self.alternative = False

        # NB: alphabetically sorted, do not reshuffle
        self.Operators = [
             #'cDim8_k1',
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
             'cuu1'
             ]

        self.numOperators = len(self.Operators)

        print " Operators = ", self.Operators


    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.mHRange = po.replace("higgsMassRange=","").split(",")
                if len(self.mHRange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema"
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"

            if po.startswith("eftOperators="):
                self.Operators = po.replace("eftOperators=","").split(",")
                print " Operators = ", self.Operators
                self.numOperators = len(self.Operators)

            if po.startswith("eftAlternative"):
                self.alternative = True

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
        # model: SM + k*linear + k**2 * quadratic
        #
        #   SM        = Asm**2
        #   linear    = Asm*Absm
        #   quadratic = Absm**2
        #
        #  ... and extended to more operators
        #
        #
        # model: SM + k*linear + k**2 * quadratic
        #
        #   SM        = Asm**2
        #   linear_1        = Asm*Abs_1
        #   linear_2        = Asm*Absm_2
        #   linear_3        = Absm_1*Absm_2
        #   quadratic_1 = Absm_1**2
        #   quadratic_2 = Absm_2**2
        #
        #
        #  Combine limitation/assumption: all histograms are defined positive
        #      See http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/physicsmodels/#interference
        #  There will be some algebra here below to deal with it, but it will be transparent for the user
        #  as if it was ...
        #
        #
        # e.g. expr::func_sm("@0*(1-(@1+@2+@3-@1*@2-@1*@3-@2*@1-@2*@3-@3*@1-@3*@2))",r,k_cG,k_cGtil, k_cG,k_cH, k_cGtil,k_cG, k_cGtil,k_cH, k_cH,k_cG, k_cH,k_cGtil)
        #

        #
        # sm
        #
        print " Test = "

        if not self.alternative :
          if self.numOperators != 1:
              print "expr::func_sm(\"@0*(1-(" +                                                                                                                                                                  \
                             "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +                                                                                                               \
                             "-@" + "-@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if j!=i ]) +                                                     \
                             "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
          else:
            print "expr::func_sm(\"@0*(1-(" +                                                                     \
                    "@1" +                                                                                          \
                    "))\",r," + "k_" + str(self.Operators[0]) + ")"
          if self.numOperators != 1:
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +
                                          "-@" + "-@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if j!=i ]) +
                                          "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
                 )
          else :
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@1" +
                                          "))\",r," + "k_" + str(self.Operators[0]) + ")"
                 )
        else :

          print "expr::func_sm(\"@0*(1-(" +                                                                                                                                                               \
                         "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +                                                                                                               \
                         "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"

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
        # sm + linear + quadratic
        #

        if not self.alternative :
          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              #
              # sm + linear + quadratic
              #
              #print " Test = "
              print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                                           \
                                 "(\"@0*(" +                                                                                      \
                                 "@1 * (1-2*(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +      \
                                 ")\",r,k_" + str(self.Operators[operator]) +                                                     \
                                 ", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +            \
                                 ")"
              #
              #
              # expr::func_sm_linear_quadratic_cG("@0*(@1 * (1-2*(@2+@3) ))",r,k_cG, k_cGtil, k_cH)
              #
              #
              self.modelBuilder.factory_(
                      "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                 "(\"@0*(" +
                                 "@1 * (1-2*(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +
                                 ")\",r,k_" + str(self.Operators[operator]) +
                                 ", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +
                                 ")"
                      )
          else :
            print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                   \
                      "(\"@0*(" +                                                                      \
                      "@1" +                                                                           \
                      ")\",r,k_" + str(self.Operators[0]) +                                           \
                      ")"
  
            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                               "(\"@0*(" +
                               "@1" +
                               ")\",r,k_" + str(self.Operators[0]) +
                               ")"
                    )

        else :
          for operator in range(0, self.numOperators):
            print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                   \
                      "(\"@0*(" +                                                                      \
                      "@1" +                                                                           \
                      ")\",r,k_" + str(self.Operators[operator]) +                                           \
                      ")"

            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                "(\"@0*(" +
                                "@1" +
                                ")\",r,k_" + str(self.Operators[operator]) +
                                ")"
                    )
          
          
        #
        # quadratic term in each Wilson coefficient
        #
        #
        # e.g. expr::func_sm_linear_quadratic_cH("@0*(@1 * (1-2*(@2+@3) ))",r,k_cH, k_cG, k_cGtil)
        #

        for operator in range(0, self.numOperators):

          if not self.alternative :

            print "expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r,k_" + str(self.Operators[operator]) + ")"

            self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r,k_" + str(self.Operators[operator]) + ")")


          else :

            if self.numOperators != 1:
              #for operator_sub in range(operator+1, self.numOperators):

              print "expr::func_quadratic_"+ str(self.Operators[operator]) +                                                                                              \
                                        "(\"@0*(@1*@1-@1-2*(" +                                                                                                          \
                                        "@" + "+@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if j!=i ]) +   \
                                        "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +
                                        "(\"@0*(@1*@1-@1-2*(" +
                                        "@" + "+@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if j!=i ]) +
                                        "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
                                        )
            else:

              print "expr::func_quadratic_"+ str(self.Operators[0]) +                                                                                              \
                                        "(\"@0*(@1*@1-@1" +   \
                                        ")\",r,k_" + str(self.Operators[0]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +                                                                                              \
                                        "(\"@0*(@1*@1-@1" +   \
                                        ")\",r,k_" + str(self.Operators[0]) + ")"
                                        )



        #
        # interference between pairs of Wilson coefficients + SM + linear + quadratic
        #
        if self.numOperators != 1:
          for operator in range(0, self.numOperators):
            for operator_sub in range(operator+1, self.numOperators):

              #
              # Since I have only Mij (and I do not define the sample Mji)
              #
              print "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
               "(\"@0*@1*@2*2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +                      \
               ")"

              self.modelBuilder.factory_(
                       "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                       "(\"@0*@1*@2*2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +
                       ")")


        if self.numOperators != 1 and self.alternative:
          for operator in range(0, self.numOperators):
            for operator_sub in range(operator+1, self.numOperators):

              #
              # Since I have only Mij (and I do not define the sample Mji)
              #
              print "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
               "(\"@0*@1*@2*2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +                      \
               ")"

              self.modelBuilder.factory_(
                       "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                       "(\"@0*@1*@2*2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +
                       ")")








        print " parameters of interest = ", self.poiNames
        print " self.numOperators = ", self.numOperators
        
        self.modelBuilder.doSet("POI",self.poiNames)





#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        print "process = " , process

        if   process == "sm":          return "func_sm"

        for operator in range(0, self.numOperators):
          if process == "sm_lin_quad_"+ str(self.Operators[operator]) :    return "func_sm_linear_quadratic_"+ str(self.Operators[operator])
          if process == "quad_"+ str(self.Operators[operator]) :              return "func_quadratic_"+ str(self.Operators[operator])
          for operator_sub in range(operator+1, self.numOperators):
            if not self.alternative :
              if process == "sm_lin_quad_mixed_"+ str(self.Operators[operator]) + "_"+ str(self.Operators[operator_sub]) :    return "func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
              if process == "sm_lin_quad_mixed_"+ str(self.Operators[operator_sub]) + "_"+ str(self.Operators[operator]) :    return "func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
            else :
              if process == "quad_mixed_"+ str(self.Operators[operator]) + "_"+ str(self.Operators[operator_sub]) :    return "func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
              if process == "quad_mixed_"+ str(self.Operators[operator_sub]) + "_"+ str(self.Operators[operator]) :    return "func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])



        return 1



analiticAnomalousCouplingEFTNegative = AnaliticAnomalousCouplingEFTNegative()
