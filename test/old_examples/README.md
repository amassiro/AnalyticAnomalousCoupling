2D contour plot
~~~

Example

                                                                          x          y
    r00t  input/test.root   draw2D.cxx\(\"#mu_{ggH}\",\"#mu_{VBF/VH}\",\"muGGH\",\"muVBF\"\)    
                                                     
    
Plot
~~~

    ../scripts/mkPlotEFT.py \
          --inputFileROOT     inWW_cHWB_cHl3_ptl1.root \
          --inputFilePairs    test_pairs.py    \
          --outputFile        mytest.root    \
          --sampleNameSM      sm     \
          --folderName        ""   

          
    mkPlotEFT.py \
          --inputFileROOT     inWW_cHWB_cHl3_ptl1.root \
          --inputFilePairs    test_pairs.py    \
          --outputFile        mytest.root    \
          --sampleNameSM      sm     \
          --folderName        ""   
     
     
      
    
Test new model
----

    text2workspace.py        datacard3opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root   
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 1000  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH,k_cHB,k_cHBtil,k_cHDD,k_cHG,k_cHGtil,k_cHW,k_cHWB,k_cHWBtil,k_cHWtil,k_cHbox,k_cHd,k_cHe,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cHu,k_cHudAbs,k_cHudPh,k_cW,k_cWtil,k_cdBAbs,k_cdBPh,k_cdGAbs,k_cdGPh,k_cdHAbs,k_cdHPh,k_cdWAbs,k_cdWPh,k_cdd,k_cdd1,k_ceBAbs,k_ceBPh,k_ceHAbs,k_ceHPh,k_ceWAbs,k_ceWPh,k_ced,k_cee,k_ceu,k_cld,k_cle,k_cledqAbs,k_cledqPh,k_clequ1Abs,k_clequ1Ph,k_clequ3Abs,k_clequ3Ph,k_cll,k_cll1,k_clq1,k_clq3,k_clu,k_cqd1,k_cqd8,k_cqe,k_cqq1,k_cqq11,k_cqq3,k_cqq31,k_cqu1,k_cqu8,k_cquqd1Abs,k_cquqd1Ph,k_cquqd8Abs,k_cquqd8Ph,k_cuBAbs,k_cuBPh,k_cuGAbs,k_cuGPh,k_cuHAbs,k_cuHPh,k_cuWAbs,k_cuWPh,k_cud1,k_cud8,k_cuu,k_cuu1   \
        --setParameters r=1    --setParameterRanges k_cG=-2,2     \
        --verbose -1
    
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 1000  -m 125   -t -1 --expectSignal=1     \
        --redefineSignalPOIs k_cG,k_cGtil \
        --freezeParameters r,k_cH,k_cHB,k_cHBtil,k_cHDD,k_cHG,k_cHGtil,k_cHW,k_cHWB,k_cHWBtil,k_cHWtil,k_cHbox,k_cHd,k_cHe,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cHu,k_cHudAbs,k_cHudPh,k_cW,k_cWtil,k_cdBAbs,k_cdBPh,k_cdGAbs,k_cdGPh,k_cdHAbs,k_cdHPh,k_cdWAbs,k_cdWPh,k_cdd,k_cdd1,k_ceBAbs,k_ceBPh,k_ceHAbs,k_ceHPh,k_ceWAbs,k_ceWPh,k_ced,k_cee,k_ceu,k_cld,k_cle,k_cledqAbs,k_cledqPh,k_clequ1Abs,k_clequ1Ph,k_clequ3Abs,k_clequ3Ph,k_cll,k_cll1,k_clq1,k_clq3,k_clu,k_cqd1,k_cqd8,k_cqe,k_cqq1,k_cqq11,k_cqq3,k_cqq31,k_cqu1,k_cqu8,k_cquqd1Abs,k_cquqd1Ph,k_cquqd8Abs,k_cquqd8Ph,k_cuBAbs,k_cuBPh,k_cuGAbs,k_cuGPh,k_cuHAbs,k_cuHPh,k_cuWAbs,k_cuWPh,k_cud1,k_cud8,k_cuu,k_cuu1   \
        --setParameters r=1    --setParameterRanges k_cG=-2,2:k_cGtil=-2,2      
    

    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)

    r00t  higgsCombineTest.MultiDimFit.mH125.root    draw2D.cxx\(\"cG\",\"Gtil\",\"k_cG\",\"k_cGtil\"\)    

    
    
    
    
    
    
    
    
    text2workspace.py        datacard1opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH

    text2workspace.py        datacard1opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH,k_cHB,k_cHBtil,k_cHDD,k_cHG,k_cHGtil,k_cHW,k_cHWB,k_cHWBtil,k_cHWtil,k_cHbox,k_cHd,k_cHe,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cHu,k_cHudAbs,k_cHudPh,k_cW,k_cWtil,k_cdBAbs,k_cdBPh,k_cdGAbs,k_cdGPh,k_cdHAbs,k_cdHPh,k_cdWAbs,k_cdWPh,k_cdd,k_cdd1,k_ceBAbs,k_ceBPh,k_ceHAbs,k_ceHPh,k_ceWAbs,k_ceWPh,k_ced,k_cee,k_ceu,k_cld,k_cle,k_cledqAbs,k_cledqPh,k_clequ1Abs,k_clequ1Ph,k_clequ3Abs,k_clequ3Ph,k_cll,k_cll1,k_clq1,k_clq3,k_clu,k_cqd1,k_cqd8,k_cqe,k_cqq1,k_cqq11,k_cqq3,k_cqq31,k_cqu1,k_cqu8,k_cquqd1Abs,k_cquqd1Ph,k_cquqd8Abs,k_cquqd8Ph,k_cuBAbs,k_cuBPh,k_cuGAbs,k_cuGPh,k_cuHAbs,k_cuHPh,k_cuWAbs,k_cuWPh,k_cud1,k_cud8,k_cuu,k_cuu1   \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
    
    
    
    
    text2workspace.py        datacard1opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1,k_cG=0    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    # r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
    
    

    
    
    cp higgsCombineTest.MultiDimFit.mH125.root higgsCombineTest.MultiDimFit.mH125.Negative.root
    
    text2workspace.py        datacard1op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFT:analiticAnomalousCouplingEFT   -o   model_test.root    --X-allow-no-signal
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1,k_cG=0    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.Negative.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
    
    
Negative:
expr::sm_func("@0*(1-(@1))",r,k_cG)
expr::func_sm_linear_quadratic_cG("@0*(@1)",r,k_cG)
expr::func_quadratic_cG("@0*(@1*@1-@1)",r,k_cG)

    
Standard:
expr::sm_func("@0",r)
expr::linear_func_cG("@0*@1",r,k_cG)
expr::quadratic_func_cG("@0*@1*@1",r,k_cG)
    
    
    
    
    
expr::sm_func("@0*(1-(@1-@))",r,k_cG)
expr::func_quadratic_cG("@0*(@1*@1-@1)",r,k_cG)
 parameters of interest =  r,k_cG

 
    text2workspace.py        datacard3opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
 


 
expr::sm_func("@0*(1-(@1+@2+@3-@1*@2-@1*@3-@2*@1-@2*@3-@3*@1-@3*@2))",r,k_cG, k_cGtil, k_cH)
expr::func_sm_linear_quadratic_cG("@0*(@1 * (1-2*(@2+@3) ))",r,k_cG, k_cGtil, k_cH)
expr::func_sm_linear_quadratic_cGtil("@0*(@1 * (1-2*(@2+@3) ))",r,k_cGtil, k_cG, k_cH)
expr::func_sm_linear_quadratic_cH("@0*(@1 * (1-2*(@2+@3) ))",r,k_cH, k_cG, k_cGtil)
expr::func_quadratic_cH("@0*(@1*@1-@1)",r,k_cH)
expr::func_sm_linear_quadratic_mixed_cGtil_cG("@0*@1*@2*2",r,k_cG,k_cGtil)
expr::func_sm_linear_quadratic_mixed_cH_cG("@0*@1*@2*2",r,k_cG,k_cH)
expr::func_sm_linear_quadratic_mixed_cH_cGtil("@0*@1*@2*2",r,k_cGtil,k_cH)





If in the model there are N-operators, ALL histograms should be provided.
Otherwise I need a flag of the operators that I want IN THE MODEL BUILDING







    text2workspace.py        datacard3opNew.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH  \
          --PO  eftAlternative
    
    

    text2workspace.py        datacard_cHDD_mjj_1D.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_1_wrong.root    --X-allow-no-signal  \
          --PO eftOperators=cHDD,cHWB  \    
    
    text2workspace.py        datacard_cHDD_mjj_1D.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_1.root    --X-allow-no-signal  \
          --PO eftOperators=cHDD  \
      
    text2workspace.py        datacard_cHDD_cHWB_mjj_2D.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_2.root    --X-allow-no-signal  \
          --PO eftOperators=cHDD,cHWB  \

    text2workspace.py        datacard_cHDD_cHWB_mjj_2D.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_2_correct.root    --X-allow-no-signal  \
          --PO eftOperators=cHDD  \
          

          
          
    combine -M MultiDimFit model_test_1_wrong.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cHDD \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cHDD=-10,10     \
        --verbose -1
    mv higgsCombineTest.MultiDimFit.mH125.root scan_model_test_1_wrong.root

    
    combine -M MultiDimFit model_test_1.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cHDD \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cHDD=-10,10     \
        --verbose -1
    mv higgsCombineTest.MultiDimFit.mH125.root scan_model_test_1.root
    
    
    combine -M MultiDimFit model_test_2.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cHDD \
        --freezeParameters r,k_cHWB  \
        --setParameters r=1,k_cHWB=0    --setParameterRanges k_cHDD=-10,10     \
        --verbose -1
    mv higgsCombineTest.MultiDimFit.mH125.root scan_model_test_2.root
    
    
    combine -M MultiDimFit model_test_2_correct.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cHDD \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cHDD=-10,10     \
        --verbose -1
    mv higgsCombineTest.MultiDimFit.mH125.root scan_model_test_2_correct.root
     
     
    r99t scan_model_test_1.root  scan_model_test_1_wrong.root   draw.cxx\(\"k_cHDD\"\)    --> they are different, since missing pieces and formula is wrong
    r99t scan_model_test_1.root  scan_model_test_2.root   draw.cxx\(\"k_cHDD\"\)          --> they are the same
    r99t scan_model_test_1.root  scan_model_test_2_correct.root   draw.cxx\(\"k_cHDD\"\)  --> they are the same
    r99t scan_model_test_2.root  scan_model_test_2_correct.root   draw.cxx\(\"k_cHDD\"\)  --> they are the same, thanks to the new fix (return 0) in the model

    
    
    
    