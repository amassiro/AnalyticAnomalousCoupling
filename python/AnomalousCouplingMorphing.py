from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

#
# See derivation and explanation, validation, tests in AN-20-204
#


class AnaliticAnomalousCouplingMorphing(PhysicsModel):

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
        self.numOperators = 82
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
        print (" Operators = ", self.Operators)


    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            
            if po.startswith("eftOperators="):
                self.Operators = po.replace("eftOperators=","").split(",")
                self.numOperators = len(self.Operators)
                print (" Operators = ", self.Operators)
                if self.numOperators > 1:
                  raise ValueError(f"for now only works with one operator, you specified {self.numOperators}")
                

            if po.startswith("addDim8"):
                self.Operators.extend ( self.OperatorsDim8 )
                self.addDim8 = True

            #
            # this is needed in the case the complete list of operators is not the one provided above,
            # but for some reason, like a new model or a new basis, different or more operators are added.
            # There could be also the possibility that one operator is removed from the complete list of operators,
            # who knows why ... by it might happen, thus the method to remove it is given hereafter
            #
            if po.startswith("defineCompleteOperators="):
                self.CompleteOperators = po.replace("defineCompleteOperators=","").split(",")
                print (" CompleteOperators = ", self.CompleteOperators)

            if po.startswith("addToCompleteOperators="):
                toAddOperators = po.replace("addToCompleteOperators=","").split(",")
                self.CompleteOperators.extend ( toAddOperators )
                print (" CompleteOperators = ", self.CompleteOperators)

            if po.startswith("removeFromCompleteOperators="):
                toRemoveOperators = po.replace("removeFromCompleteOperators=","").split(",")
                newlist = [i for i in self.CompleteOperators if i not in toRemoveOperators]
                self.CompleteOperators = newlist
                print (" CompleteOperators = ", self.CompleteOperators)


    # Define parameters of interest
    #

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # mu overall scaling of all signals
        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"


        # EFT scaling is implemented as follows:

        # expected input template for w(0), w(1), w(-1)

        # SM = w(0)
        # SM + Li + Qi = w(1)
        # SM - Li + Qi = w(-1)

        # N(k) = SM + kLi + kkQi
        #      = (1-kk)w(0) + 0.5*k(1+k)w(1) + 0.5k*(k-1)w(-1)


        # for now only one op
        for operator in range(0, self.numOperators):
          self.modelBuilder.doVar("k_" + str(self.Operators[operator]) + "[0,-200,200]")
          self.poiNames += ",k_" + str(self.Operators[operator])

          # Sm scaling w(0)
          if self.numOperators != 1:
            # for now we do not enter here
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +
                                          "-@" + "-@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if i<j ]) +
                                          "))\",r," + "k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
                 )
          else :
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@1*@1" +
                                          "))\",r," + "k_" + str(self.Operators[0]) + ")"
                 )


        #
        # this is the coefficient of "SM + Lin_i + Quad_i"
        #

        if self.numOperators != 1:
          # for now we do not enter here FIX ME
          for operator in range(0, self.numOperators):
            #print " Test = "
            #print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                                           \
                                #"(\"@0*(" +                                                                                      \
                                #"@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +      \
                                #")\",r,k_" + str(self.Operators[operator]) +                                                     \
                                #", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +            \
                                #")"
            #
            #
            # expr::func_sm_linear_quadratic_cG("@0*(@1 * (1-2*(@2+@3) ))",r,k_cG, k_cGtil, k_cH)
            #
            #
            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                "(\"@0*(" +
                                "@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +
                                ")\",r,k_" + str(self.Operators[operator]) +
                                ", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +
                                ")"
                    )
        else :
          print ("expr::func_sm_linear_quadratic_" + str(self.Operators[0]) +
                              "(\"@0*(" +
                              "0.5*@1*(1+@1)" +
                              ")\",r,k_" + str(self.Operators[0]) +
                              ")")
                              
          self.modelBuilder.factory_(
                  "expr::func_sm_linear_quadratic_" + str(self.Operators[0]) +
                              "(\"@0*(" +
                              "0.5*@1*(1+@1)" +
                              ")\",r,k_" + str(self.Operators[0]) +
                              ")"
                  )



                #
        # this is the coefficient of "SM - Lin_i + Quad_i"
        #

        if self.numOperators != 1:
          # for now we do not enter here FIX ME
          for operator in range(0, self.numOperators):
            #print " Test = "
            #print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                                           \
                                #"(\"@0*(" +                                                                                      \
                                #"@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +      \
                                #")\",r,k_" + str(self.Operators[operator]) +                                                     \
                                #", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +            \
                                #")"
            #
            #
            # expr::func_sm_linear_quadratic_cG("@0*(@1 * (1-2*(@2+@3) ))",r,k_cG, k_cGtil, k_cH)
            #
            #
            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                "(\"@0*(" +
                                "@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +
                                ")\",r,k_" + str(self.Operators[operator]) +
                                ", k_" + ", k_".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +
                                ")"
                    )
        else :
          print ("expr::func_sm_minuslinear_quadratic_" + str(self.Operators[0]) +
                              "(\"@0*(" +
                              "0.5*@1*(@1-1)" +
                              ")\",r,k_" + str(self.Operators[0]) +
                              ")")
                              
          self.modelBuilder.factory_(
                  "expr::func_sm_minuslinear_quadratic_" + str(self.Operators[0]) +
                              "(\"@0*(" +
                              "0.5*@1*(@1-1)" +
                              ")\",r,k_" + str(self.Operators[0]) +
                              ")"
                  )

        # This is the old code for Quadratic Qi and mixed interferences
        # We leave it here commented so that we can recycle in future
        # for the time being we assume only one operator
        """
        for operator in range(0, self.numOperators):

          #
          # this is the coefficient of "Quad_i"
          #
          
          if not self.alternative :

            #print "expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r,k_" + str(self.Operators[operator]) + ")"

            self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r,k_" + str(self.Operators[operator]) + ")")


          else :

            if self.numOperators != 1:

              #print "expr::func_quadratic_"+ str(self.Operators[operator]) +    \
                                        #"(\"@0*(@1*@1-@1-@1*(" + "@" + "+@".join([str(j+1) for j in range(len(self.Operators)) if j != 0 ]) +   \
                                        #"))\",r," + "k_" +  str(self.Operators[operator]) + ", k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators)) if i != operator ]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +      \
                                        "(\"@0*(@1*@1-@1-@1*(" + "@" + "+@".join([str(j+1) for j in range(len(self.Operators)) if j != 0 ]) +   \
                                        "))\",r," + "k_" +  str(self.Operators[operator]) + ", k_" + ", k_".join([str(self.Operators[i]) for i in range(len(self.Operators)) if i != operator ]) + ")"
                                        )
                                                                                                                                                                                

            else:

              #print "expr::func_quadratic_"+ str(self.Operators[0]) + \
                                        #"(\"@0*(@1*@1-@1" +   \
                                        #")\",r,k_" + str(self.Operators[0]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +  \
                                        "(\"@0*(@1*@1-@1" +   \
                                        ")\",r,k_" + str(self.Operators[0]) + ")"
                                        )



        #
        # (SM + linear) + quadratic + interference between pairs of Wilson coefficients
        #
        
        if not self.alternative :
          
          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              for operator_sub in range(operator+1, self.numOperators):

                #
                # this is the coefficient of "SM + Lin_i + Lin_j + Quad_i + Quad_j + 2 * M_ij"
                #
                #print "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
                #"(\"@0*@1*@2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +                      \
                #")"

                self.modelBuilder.factory_(
                        "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                        "(\"@0*@1*@2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +
                        ")")

        else:

          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              for operator_sub in range(operator+1, self.numOperators):

                #
                # this is the coefficient of "Quad_i + Quad_j + 2 * M_ij"
                #
                #print "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
                #"(\"@0*@1*@2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +                      \
                #")"

                self.modelBuilder.factory_(
                        "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                        "(\"@0*@1*@2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) +
                        ")")


        """

        print (" parameters of interest = ", self.poiNames)
        print (" self.numOperators = ", self.numOperators)
        
        self.modelBuilder.doSet("POI",self.poiNames)





#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        #print "process = " , process

        if   process == "sm" or "_sm" in process:
          print(f"scaling {process} with func_sm")          
          return "func_sm"

        for operator in range(0, self.numOperators):

          # Sm + Li + Qi coefficient
          if process == "w1_" + str(self.Operators[operator]) or "_w1_" + str(self.Operators[operator]) in process :
            print(f"scaling {process} with func_sm_linear_quadratic_{self.Operators[operator]}")
            return "func_sm_linear_quadratic_"+ str(self.Operators[operator])

          # Sm - Li + Qi coefficient
          if process == "wm1_" + str(self.Operators[operator]) or "_wm1_" + str(self.Operators[operator]) in process :
            print(f"scaling {process} with func_sm_minuslinear_quadratic_{self.Operators[operator]}")
            return "func_sm_minuslinear_quadratic_"+ str(self.Operators[operator])
          

        """
        for operator in range(0, self.numOperators):
          if process == "sm_lin_quad_"+ str(self.Operators[operator]) or "_sm_lin_quad_"+ str(self.Operators[operator]) in process : 
            return "func_sm_linear_quadratic_"+ str(self.Operators[operator])
          if process == "quad_"+ str(self.Operators[operator]) :              return "func_quadratic_"+ str(self.Operators[operator])
          for operator_sub in range(operator+1, self.numOperators):
            if not self.alternative :
              if process == "sm_lin_quad_mixed_"+ str(self.Operators[operator]) + "_"+ str(self.Operators[operator_sub]) or "_sm_lin_quad_mixed_"+ str(self.Operators[operator]) + "_"+ str(self.Operators[operator_sub]) in process :   
                return "func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
              if process == "sm_lin_quad_mixed_"+ str(self.Operators[operator_sub]) + "_"+ str(self.Operators[operator]) or "_sm_lin_quad_mixed_"+ str(self.Operators[operator_sub]) + "_"+ str(self.Operators[operator]) in process :  
                return "func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
            else :
              if process == "quad_mixed_"+ str(self.Operators[operator]) + "_"+ str(self.Operators[operator_sub]) : 
                return "func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
              if process == "quad_mixed_"+ str(self.Operators[operator_sub]) + "_"+ str(self.Operators[operator]) :  
                return "func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])
        """
        
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

        print(f"scaling {process} with 1")
        return 1


#
#  Standard inputs:
# 
#     S
#     S + Li + Qi
#     S - Li + Qi
#    
#



analiticAnomalousCouplingMorphing = AnaliticAnomalousCouplingMorphing()
