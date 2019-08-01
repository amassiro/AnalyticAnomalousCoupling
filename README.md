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
    
    
    
    
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx
