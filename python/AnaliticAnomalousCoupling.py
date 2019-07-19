from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class AnaliticAnomalousCoupling(PhysicsModel):

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
        # model: https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/HiggsSelfCoupling
        #

        
        #
        # N -->   N * ( 1 + C1 * (k-1) + (k*k-1)*C2(k) ) = N * alpha(k)
        #
        # C2(k) = -1.536/1000 /  (1 + k*k*1.536/1000)
        #
        # N -->   N * ( 1 + C1 * (k-1) - (k*k-1)* 1.536/1000 /  (1 + k*k*1.536/1000) )
        # with z_0 hardcoded for each bin of p_T Higgs
        #
        #
        #
        #            0             1         2
        # Pt bin: [150, inf] , [50, 150], [0, 50]
        #   ttH     
        #   W-H     
        #   W+H     
        #    ZH     
        # 
        #
        #     Pt binning: 0 50 150 500
        #     ttH Hadronic: 0.0508135 0.036604 0.0155118
        #     ttH Leptonic: 0.050483 0.0377599 0.0160557
        #     VH Hadronic: 0.0119485 0.00274689 -0.000572456
        #     VH Leptonic Loose: 0.0137786 0.00723102 -9.21914e-05
        #     WH: 0.0138817 0.0062774 -0.000408755
        #     ZH: 0.0166121 0.00798076 -0.000183597       
        #
        #C1map = {
        #         #"ttH_hgg_0":0.893,
        #         #"ttH_hgg_1":0.915,
        #         #"ttH_hgg_2":0.950,
        #         ##
        #         #"WH_hgg_1":0.967,
        #         #"WH_hgg_2":0.973,
        #         #"WH_hgg_3":0.990,
        #         ##
        #         #"ZH_hgg_1":0.963,
        #         #"ZH_hgg_2":0.972,
        #         #"ZH_hgg_3":0.990,
        #         ##
        #         ## VH as WH
        #         ##
        #         #"VH_0":0.967,
        #         #"VH_1":0.973,
        #         #"VH_2":0.990,
        #         #
        #         "ttH_hgg_0":0.0155118,
        #         "ttH_hgg_1":0.036604,
        #         "ttH_hgg_2":0.0508135,
        #         #
        #         #"ttH_hgg_0":0.05,
        #         #"ttH_hgg_1":0.04,
        #         #"ttH_hgg_2":0.02,
        #         #
        #         "WH_hgg_1":0.004,
        #         "WH_hgg_2":0.010,
        #         "WH_hgg_3":0.015,
        #         #
        #         "ZH_hgg_1":0.005,
        #         "ZH_hgg_2":0.015,
        #         "ZH_hgg_3":0.020,
        #         #
        #         # VH as WH
        #         #
        #         "VH_0":0.0,
        #         "VH_1":0.0062774,
        #         "VH_2":0.0138817,
        #         }
        #
        C1map =  self.C1map
        #z0map = {
                 #"hpt1":1.10,
                 #"hpt2":0.30,
                 #"hpt3":0.10,
                 #"hpt4":0.03
                 #}
        #for proc in ["hpt1","hpt2","hpt3","hpt4"]: 

        for proc in ["ttH_hgg_0","ttH_hgg_1","ttH_hgg_2",
                     "WH_hgg_1", "WH_hgg_2", "WH_hgg_3",
                     "ZH_hgg_1", "ZH_hgg_2", "ZH_hgg_3",
                     "VH_0", "VH_1", "VH_2"
                     ]: 
          alpha = C1map[proc]

          # not considering the effects on BR (H>xx)
          #self.modelBuilder.factory_("expr::XSscal_%s(\"(1+(@0-1)*%g-(@0*@0-1)*(1.536/1000/(1 + @0*@0*1.536/1000)))*@1\",k_my,r)" % (proc,alpha))

          # including also the BR effect
          # N -->   N * ( 1 + C1 * (k-1) - (k*k-1)* 1.536/1000 /  (1 + k*k*1.536/1000) )
          # N -->   N * ( 1 + C1 * (k-1) - (k*k-1)* 1.536/1000 /  (1 + k*k*1.536/1000) )  * (1 + (k-1)*(Ci - Ctot) / (1+ (k-1)*Ctot) )
          #
          # Ci = 0.49*10-3
          # Ctot = 2.3*10-3
          # 
          self.modelBuilder.factory_("expr::XSscal_%s(\"(1+(@0-1)*%g-(@0*@0-1)*(1.536/1000/(1 + @0*@0*1.536/1000)))*(1+(@0-1)*(0.49-2.3)/1000/(1+(@0-1)*2.3/1000))*@1\",k_my,r)" % (proc,alpha))
          # FIXME

          #self.modelBuilder.factory_("expr::XSscal_%s(\"@0\",r)" % (proc))
          #self.modelBuilder.factory_("expr::XSscal_%s(\"(1+(@0-1)*%g)*@1\",k_my,r)" % (proc,alpha))


        print self.poiNames
        self.modelBuilder.doSet("POI",self.poiNames)




#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

      #if process in ["hpt1","hpt2","hpt3","hpt4"]: 

      if process in ["ttH_hgg_0","ttH_hgg_1","ttH_hgg_2",
                     "WH_hgg_1", "WH_hgg_2", "WH_hgg_3",
                     "ZH_hgg_1", "ZH_hgg_2", "ZH_hgg_3",
                     "VH_0", "VH_1", "VH_2"
                     ]: 
        return "XSscal_" + process
  
      else:
        return 1



analiticAnomalousCoupling = AnaliticAnomalousCoupling()


