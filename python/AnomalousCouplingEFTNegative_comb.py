import fnmatch
import json
import sys
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

#
# See derivation and explanation, validation, tests in AN-20-204
#


class AnaliticAnomalousCouplingEFTNegative_comb(PhysicsModel):
    "Float independently cross sections and branching ratios"

    def __init__(self):
        PhysicsModel.__init__(
            self
        )  # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
        self.numOperators = 82
        self.alternative = False
        self.addDim8 = False
        self.OperatorsDim8 = [
            # dimension 8
            "cS0",
            "cS1",
            "cM0",
            "cM1",
            "cM2",
            "cM3",
            "cM4",
            "cM6",
            "cM7",
            "cT0",
            "cT1",
            "cT2",
            "cT3",
            "cT4",
            "cT6",
            "cT7",
            "cT8",
            "cT9",
        ]

        # NB: alphabetically sorted, do not reshuffle
        self.Operators = [
            # dimension 6
            "cG",
            "cGtil",
            "cH",
            "cHB",
            "cHBtil",
            "cHDD",
            "cHG",
            "cHGtil",
            "cHW",
            "cHWB",
            "cHWBtil",
            "cHWtil",
            "cHbox",
            "cHd",
            "cHe",
            "cHl1",
            "cHl3",
            "cHq1",
            "cHq3",
            "cHu",
            "cHudAbs",
            "cHudPh",
            "cW",
            "cWtil",
            "cdBAbs",
            "cdBPh",
            "cdGAbs",
            "cdGPh",
            "cdHAbs",
            "cdHPh",
            "cdWAbs",
            "cdWPh",
            "cdd",
            "cdd1",
            "ceBAbs",
            "ceBPh",
            "ceHAbs",
            "ceHPh",
            "ceWAbs",
            "ceWPh",
            "ced",
            "cee",
            "ceu",
            "cld",
            "cle",
            "cledqAbs",
            "cledqPh",
            "clequ1Abs",
            "clequ1Ph",
            "clequ3Abs",
            "clequ3Ph",
            "cll",
            "cll1",
            "clq1",
            "clq3",
            "clu",
            "cqd1",
            "cqd8",
            "cqe",
            "cqq1",
            "cqq11",
            "cqq3",
            "cqq31",
            "cqu1",
            "cqu8",
            "cquqd1Abs",
            "cquqd1Ph",
            "cquqd8Abs",
            "cquqd8Ph",
            "cuBAbs",
            "cuBPh",
            "cuGAbs",
            "cuGPh",
            "cuHAbs",
            "cuHPh",
            "cuWAbs",
            "cuWPh",
            "cud1",
            "cud8",
            "cuu",
            "cuu1",
            "cjj11",
            "cjj18",
            "cjj31",
            "cjj38",
            "cHj1",
            "cHQ1",
        ]

        self.CompleteOperators = self.Operators + self.OperatorsDim8

        self.numOperators = len(self.Operators)
        print(" Operators = ", self.Operators)
        self.verbose = True

    def setPhysicsOptions(self, physOptions):
        print(physOptions)
        for po in physOptions:
            # if po.startswith("higgsMassRange="):
            # self.mHRange = po.replace("higgsMassRange=","").split(",")
            # if len(self.mHRange) != 2:
            # raise RuntimeError, "Higgs mass range definition requires two extrema"
            # elif float(self.mHRange[0]) >= float(self.mHRange[1]):
            # raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"

            if po.startswith("fileCombination="):
                print("Doing filecombination")
                fileCombination = po.replace("fileCombination=", "")
                with open(fileCombination) as f:
                    self.bin_ops_map = json.load(f)

            if po.startswith("eftOperators="):
                self.Operators = po.replace("eftOperators=", "").split(",")
                print(" Operators = ", self.Operators)
                self.numOperators = len(self.Operators)

            if po.startswith("eftAlternative"):
                self.alternative = True

            if po.startswith("addDim8"):
                self.Operators.extend(self.OperatorsDim8)
                self.addDim8 = True

            if po.startswith("verbose="):
                self.verbose = eval(po.replace("verbose=", ""))

            #
            # this is needed in the case the complete list of operators is not the one provided above,
            # but for some reason, like a new model or a new basis, different or more operators are added.
            # There could be also the possibility that one operator is removed from the complete list of operators,
            # who knows why ... by it might happen, thus the method to remove it is given hereafter
            #
            if po.startswith("defineCompleteOperators="):
                self.CompleteOperators = po.replace(
                    "defineCompleteOperators=", ""
                ).split(",")
                print(" CompleteOperators = ", self.CompleteOperators)

            if po.startswith("addToCompleteOperators="):
                toAddOperators = po.replace("addToCompleteOperators=", "").split(",")
                self.CompleteOperators.extend(toAddOperators)
                print(" CompleteOperators = ", self.CompleteOperators)

            if po.startswith("removeFromCompleteOperators="):
                toRemoveOperators = po.replace(
                    "removeFromCompleteOperators=", ""
                ).split(",")
                newlist = [
                    i for i in self.CompleteOperators if i not in toRemoveOperators
                ]
                self.CompleteOperators = newlist
                print(" CompleteOperators = ", self.CompleteOperators)

        if not hasattr(self, "bin_ops_map"):
            self.bin_ops_map = {"*": self.Operators}
        else:
            for ibin in self.bin_ops_map:
                self.bin_ops_map[ibin] = [
                    i for i in self.bin_ops_map[ibin] if i in self.Operators
                ]

    #
    # standard, not touched (end)
    #

    #
    # Define parameters of interest
    #
    def private_factory(self, func):
        if self.verbose:
            print(func)
        self.modelBuilder.factory_(func)

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"

        for operator in range(0, self.numOperators):
            self.modelBuilder.doVar(
                "k_" + str(self.Operators[operator]) + "[0,-200,200]"
            )
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

        #
        # this is the coefficient of "SM"
        #

        for _bin_name in self.bin_ops_map:
            bin_name = _bin_name.replace("*", "WildCard")
            active_ops = self.bin_ops_map[bin_name]
            self.numOperators = len(active_ops)
            if self.verbose:
                print(f"Active ops for {bin_name}", active_ops)

            sm_func_name = f"expr::func_sm_{bin_name}"

            if self.numOperators == 0:
                self.private_factory(f'{sm_func_name}("@0",r)')
            elif self.numOperators == 1:
                self.private_factory(
                    f'{sm_func_name}("@0*(1-('
                    + "@1"
                    + '))",r,'
                    + "k_"
                    + str(active_ops[0])
                    + ")"
                )
            else:
                self.private_factory(
                    f'{sm_func_name}("@0*(1-('
                    + "@"
                    + "+@".join([str(i + 1) for i in range(len(active_ops))])
                    + "-@"
                    + "-@".join(
                        [
                            str(i + 1) + "*@" + str(j + 1)
                            for i in range(len(active_ops))
                            for j in range(len(active_ops))
                            if i < j
                        ]
                    )
                    + '))",r,'
                    + "k_"
                    + ", k_".join([str(active_ops[i]) for i in range(len(active_ops))])
                    + ")"
                )
            #
            # Linear term e.g. expr::func_sm_linear_quadratic_cG("@0*(@1 * (1 - (@2+@3)))",r,k_cG, k_cGtil, k_cH)
            #

            if self.numOperators == 1:
                self.private_factory(
                    f"expr::func_sm_linear_quadratic_{bin_name}_"
                    + str(active_ops[0])
                    + '("@0*('
                    + "@1"
                    + ')",r,k_'
                    + str(active_ops[0])
                    + ")"
                )
            elif self.numOperators > 1:
                for operator in range(0, self.numOperators):
                    self.private_factory(
                        f"expr::func_sm_linear_quadratic_{bin_name}_"
                        + str(active_ops[operator])
                        + '("@0*('
                        + "@1 * (1-("
                        + "@"
                        + "+@".join([str(j + 2) for j in range(len(active_ops) - 1)])
                        + ") )"
                        + ')",r,k_'
                        + str(active_ops[operator])
                        + ", k_"
                        + ", k_".join(
                            [
                                str(active_ops[j])
                                for j in range(len(active_ops))
                                if operator != j
                            ]
                        )
                        + ")"
                    )

            #
            # quadratic term in each Wilson coefficient
            #

            for operator in range(0, self.numOperators):
                #
                # this is the coefficient of "Quad_i"
                #

                self.private_factory(
                    f"expr::func_quadratic_{bin_name}_"
                    + str(active_ops[operator])
                    + '("@0*(@1*@1-@1)",r,k_'
                    + str(active_ops[operator])
                    + ")"
                )

            #
            # (SM + linear) + quadratic + interference between pairs of Wilson coefficients
            #

            if self.numOperators > 1:
                for operator in range(0, self.numOperators):
                    for operator_sub in range(operator + 1, self.numOperators):
                        #
                        # this is the coefficient of "SM + Lin_i + Lin_j + Quad_i + Quad_j + 2 * M_ij"
                        #

                        self.private_factory(
                            f"expr::func_sm_linear_quadratic_mixed_{bin_name}_"
                            + str(active_ops[operator_sub])
                            + "_"
                            + str(active_ops[operator])
                            + '("@0*@1*@2",r,k_'
                            + str(active_ops[operator])
                            + ",k_"
                            + str(active_ops[operator_sub])
                            + ")"
                        )

        if self.verbose:
            print(" parameters of interest = ", self.poiNames)
            print(" self.numOperators = ", self.numOperators)

        self.modelBuilder.doSet("POI", self.poiNames)

    #
    # Define how the yields change
    #

    def getYieldScale(self, bin, process):
        func = self.getYieldScale_(bin, process)
        if self.verbose:
            print(f"Will scale {process} in bin {bin} with {func}")
        return func

    def getYieldScale_(self, bin, process):
        bin_name = None
        for _bin_name in self.bin_ops_map:
            if fnmatch.fnmatch(bin, _bin_name):
                bin_name = _bin_name
                break
        if bin_name is None:
            bin_name = bin

        bin_name = bin_name.replace("*", "WildCard")

        active_ops = self.bin_ops_map[bin_name]
        self.numOperators = len(active_ops)


        active_ops = self.bin_ops_map[bin]
        self.numOperators = len(active_ops)

        if process == "sm" or process.endswith("sm"):
            return f"func_sm_{bin_name}"

        for operator in range(0, self.numOperators):
            if (
                process == "sm_lin_quad_" + str(active_ops[operator])
                or "_sm_lin_quad_" + str(active_ops[operator]) in process
            ):
                return f"func_sm_linear_quadratic_{bin_name}_" + str(
                    active_ops[operator]
                )
            if (
                process == "quad_" + str(active_ops[operator])
                or "_quad_" + str(active_ops[operator]) in process
            ):
                return f"func_quadratic_{bin_name}_" + str(active_ops[operator])
            for operator_sub in range(operator + 1, self.numOperators):
                if not self.alternative:
                    if (
                        process
                        == "sm_lin_quad_mixed_"
                        + str(active_ops[operator])
                        + "_"
                        + str(active_ops[operator_sub])
                        or "_sm_lin_quad_mixed_"
                        + str(active_ops[operator])
                        + "_"
                        + str(active_ops[operator_sub])
                        in process
                    ):
                        return (
                            f"func_sm_linear_quadratic_mixed_{bin_name}_"
                            + str(active_ops[operator_sub])
                            + "_"
                            + str(active_ops[operator])
                        )
                    if (
                        process
                        == "sm_lin_quad_mixed_"
                        + str(active_ops[operator_sub])
                        + "_"
                        + str(active_ops[operator])
                        or "_sm_lin_quad_mixed_"
                        + str(active_ops[operator_sub])
                        + "_"
                        + str(active_ops[operator])
                        in process
                    ):
                        return (
                            f"func_sm_linear_quadratic_mixed_{bin_name}_"
                            + str(active_ops[operator_sub])
                            + "_"
                            + str(active_ops[operator])
                        )
                else:
                    if process == "quad_mixed_" + str(active_ops[operator]) + "_" + str(
                        active_ops[operator_sub]
                    ):
                        return (
                            f"func_quadratic_mixed_{bin_name}_"
                            + str(active_ops[operator_sub])
                            + "_"
                            + str(active_ops[operator])
                        )
                    if process == "quad_mixed_" + str(
                        active_ops[operator_sub]
                    ) + "_" + str(active_ops[operator]):
                        return (
                            f"func_quadratic_mixed_{bin_name}_"
                            + str(active_ops[operator_sub])
                            + "_"
                            + str(active_ops[operator])
                        )

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
#  Standard inputs:
#
#     S
#     S + Li + Qi
#     Qi
#     S + Li + Lj + Qi + Qj + 2*Mij
#
#
#
#  Alternative (triggered by eftAlternative):
#
#     S
#     S + Li + Qi
#     Qi
#     Qi + Qj + 2*Mij
#
#


analiticAnomalousCouplingEFTNegative_comb = AnaliticAnomalousCouplingEFTNegative_comb()
