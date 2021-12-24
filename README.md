# AnalyticAnomalousCoupling

Install:

    cmsrel CMSSW_10_2_13
    cd CMSSW_10_2_13/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/
    git clone git@github.com:amassiro/AnalyticAnomalousCoupling.git
 
Where:

    /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling
    

    
Model to be used:

    AnomalousCouplingEFTNegative
    
    
How to run it:

    cd test 
    
    text2workspace.py      \
            datacard1opNew.txt   \
            -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  \
            -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
    
    
Remember you need to specify the operators you are considering, because the more operators you want to consider
the more inputs you need to provide in the datacard.

You can also add the dim8 operators by

    --PO  addDim8
    
but you can also just define the new operators by
 
    --PO eftOperators=cS0,cS1,cT0
    
    

Negative bin yield    
===

It may happen that the expected yield (SM+EFT) in a bin evaluates negative. Combine will complain and return the maximum FCN value up to that point in the minimization to force MIGRAD to back out of the region. If one want to disable such behaviour and ignore the negative bin (setting its content to zero) add to the combine command the following run-time arguments

   --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT


The partial sums will be set to one (so log is zero) and no error will be propagated to RooFit: 

https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/7bffa8b8758a5dc6824b8b93c098ce9afb1c32a4/src/CachingNLL.cc#L691

https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/7bffa8b8758a5dc6824b8b93c098ce9afb1c32a4/src/CachingNLL.cc#L692

    
Older examples
====
    
    
    
    
    
Run:

    get the file:
    wget https://www.dropbox.com/s/37auaiyq4qw4o3j/histo_0p3.root
    
     sm->Integral(-1, sm->GetNbinsX())
     linear->Integral(-1, linear->GetNbinsX())
     quadratic->Integral(-1, quadratic->GetNbinsX())

     histo_sm->Integral(-1, histo_sm->GetNbinsX())
     histo_linear->Integral(-1, histo_linear->GetNbinsX())
     histo_quadratic->Integral(-1, histo_quadratic->GetNbinsX())

     

                                                                 folder                    file.py             object defined in the file.py
    text2workspace.py        datacard.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCoupling:analiticAnomalousCoupling                 --PO=k_my,r  -o      model_test.root   
    
    
            
        
    combine -M MultiDimFit model_test.root  --algo=grid --points 120  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_my --freezeParameters r --setParameters r=1    --setParameterRanges k_my=-20,20     \
        --verbose -1
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 120  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_my --freezeParameters r --setParameters r=1    --setParameterRanges k_my=-20,20   
    

    
    text2workspace.py        datacard2op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCoupling:analiticAnomalousCoupling   -o  --numOperators=2    model_test.root   
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 120  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_my_1 --freezeParameters r,k_my_2 --setParameters r=1,k_my_1=0,k_my_2=0    --setParameterRanges k_my_1=-20,20     \
        --verbose -1
    
    
    
    
    text2workspace.py        datacard3op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFT:analiticAnomalousCouplingEFT   -o   model_test.root   
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 240  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH,k_cHB,k_cHBtil,k_cHDD,k_cHG,k_cHGtil,k_cHW,k_cHWB,k_cHWBtil,k_cHWtil,k_cHbox,k_cHd,k_cHe,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cHu,k_cHudAbs,k_cHudPh,k_cW,k_cWtil,k_cdBAbs,k_cdBPh,k_cdGAbs,k_cdGPh,k_cdHAbs,k_cdHPh,k_cdWAbs,k_cdWPh,k_cdd,k_cdd1,k_ceBAbs,k_ceBPh,k_ceHAbs,k_ceHPh,k_ceWAbs,k_ceWPh,k_ced,k_cee,k_ceu,k_cld,k_cle,k_cledqAbs,k_cledqPh,k_clequ1Abs,k_clequ1Ph,k_clequ3Abs,k_clequ3Ph,k_cll,k_cll1,k_clq1,k_clq3,k_clu,k_cqd1,k_cqd8,k_cqe,k_cqq1,k_cqq11,k_cqq3,k_cqq31,k_cqu1,k_cqu8,k_cquqd1Abs,k_cquqd1Ph,k_cquqd8Abs,k_cquqd8Ph,k_cuBAbs,k_cuBPh,k_cuGAbs,k_cuGPh,k_cuHAbs,k_cuHPh,k_cuWAbs,k_cuWPh,k_cud1,k_cud8,k_cuu,k_cuu1   \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
    
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 400  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_cG,k_cGtil \
        --freezeParameters r,k_cH,k_cHB,k_cHBtil,k_cHDD,k_cHG,k_cHGtil,k_cHW,k_cHWB,k_cHWBtil,k_cHWtil,k_cHbox,k_cHd,k_cHe,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cHu,k_cHudAbs,k_cHudPh,k_cW,k_cWtil,k_cdBAbs,k_cdBPh,k_cdGAbs,k_cdGPh,k_cdHAbs,k_cdHPh,k_cdWAbs,k_cdWPh,k_cdd,k_cdd1,k_ceBAbs,k_ceBPh,k_ceHAbs,k_ceHPh,k_ceWAbs,k_ceWPh,k_ced,k_cee,k_ceu,k_cld,k_cle,k_cledqAbs,k_cledqPh,k_clequ1Abs,k_clequ1Ph,k_clequ3Abs,k_clequ3Ph,k_cll,k_cll1,k_clq1,k_clq3,k_clu,k_cqd1,k_cqd8,k_cqe,k_cqq1,k_cqq11,k_cqq3,k_cqq31,k_cqu1,k_cqu8,k_cquqd1Abs,k_cquqd1Ph,k_cquqd8Abs,k_cquqd8Ph,k_cuBAbs,k_cuBPh,k_cuGAbs,k_cuGPh,k_cuHAbs,k_cuHPh,k_cuWAbs,k_cuWPh,k_cud1,k_cud8,k_cuu,k_cuu1   \
        --setParameters r=1    --setParameterRanges k_cG=-10,10:k_cGtil=-10,10      
    
    
    ,k_cG,k_cGtil,k_cH,
      
    
    
    
    
    
To simulate "sm" part, k_my == 0 :
    
    --setParameters r=1,k_my=0
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 120  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_my --freezeParameters r --setParameters r=1,k_my=0    --setParameterRanges k_my=-20,20
    

Plot:

    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx
    
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)

    r00t  higgsCombineTest.MultiDimFit.mH125.root    draw2D.cxx\(\"cG\",\"Gtil\",\"k_cG\",\"k_cGtil\"\)    
    
    
    
    
    

    
    
