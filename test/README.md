Install
----

    cmsrel CMSSW_10_2_13
    cd CMSSW_10_2_13/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/
    git clone git@github.com:amassiro/AnalyticAnomalousCoupling.git
    cd ../
    scramv1 b -j 20

Test model
----

1D

    text2workspace.py        datacard1op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    

    combine -M MultiDimFit model_test_2_correct.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1

    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
        

3D


    text2workspace.py        datacard3op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH
    

    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
 
 
 

    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG,k_cGtil \
        --freezeParameters r,k_cH  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw2D.cxx\(\"cG\",\"Gtil\",\"k_cG\",\"k_cGtil\"\) 

    
    

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
     
     
      
 
Datacards
====

In the datacards you can add all backgrounds as a standard combine datacards, and they will not scale with the EFT couplings.

As an example, see datacard1opWithBkg.txt




Test model with only linear component
----

1D

    text2workspace.py        datacard1opLinearOnly.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingLinearEFTNegative:analiticAnomalousCouplingLinearEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    

    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1

    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
        

3D

    Both these two instructions, given how the datacards are built, shouldwork

    text2workspace.py        datacard3opLinearOnly.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingLinearEFTNegative:analiticAnomalousCouplingLinearEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH 

    text2workspace.py        datacard3op.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingLinearEFTNegative:analiticAnomalousCouplingLinearEFTNegative   -o   model_test.root    --X-allow-no-signal  \
          --PO eftOperators=cG,cGtil,cH    --PO reuseCompleteDatacards
    

    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r,k_cGtil,k_cH  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)
 
 
 

    combine -M MultiDimFit model_test.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG,k_cGtil \
        --freezeParameters r,k_cH  \
        --setParameters r=1    --setParameterRanges k_cG=-20,20:k_cGtil=-20,20    \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw2D.cxx\(\"cG\",\"Gtil\",\"k_cG\",\"k_cGtil\"\) 

    

Test for different components of SM, e.g. EWK_sm, QCD_sm, ttbar_sm, ...
Results should be identical to merging the samples (and treating properly the nuisances!), but splitting could be easier for analysers to prepare the datacards


    text2workspace.py        datacard1opWithBkg_signalSplit.txt  -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_1.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    text2workspace.py        datacard1opWithBkg_signalMerged.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative   -o   model_test_2.root    --X-allow-no-signal  \
          --PO eftOperators=cG
    

    combine -M MultiDimFit model_test_1.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1

    mv higgsCombineTest.MultiDimFit.mH125.root higgsCombineTest.MultiDimFit.mH125.1.root
    

    combine -M MultiDimFit model_test_1.root  --algo=grid --points 2000  -m 125   -t -1     \
        --redefineSignalPOIs k_cG \
        --freezeParameters r  \
        --setParameters r=1    --setParameterRanges k_cG=-10,10     \
        --verbose -1

    r99t higgsCombineTest.MultiDimFit.mH125.1.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"k_cG\"\)





