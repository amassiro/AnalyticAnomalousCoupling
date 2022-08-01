# AnalyticAnomalousCoupling

The AnalyticAnomalousCoupling provides a ***Combine-based model for EFT fits*** overcoming the issues of negative templates that may arise from interference terms.

Suppose to expand the SM Lagrangian with the inclusion of a dimension 6 operator ($Q_{\alpha}$):

$$ \mathcal{L}\_{SMEFT} = \mathcal{L}\_{SM} + \frac{c\_{\alpha}}{\Lambda^{2}} Q\_{\alpha} $$

Then the scattering amplitude would be written as

$$ \mathcal{A}\_{SMEFT} = \mathcal{A}\_{SM} + \frac{c\_{\alpha}}{\Lambda^{2}} \mathcal{A}\_{Q\_{\alpha}}  $$

Where $\mathcal{A}\_{SM}$ is the Standard Model Amplitude and $\mathcal{A}\_{\alpha}$ is the total amplitude obtained with the insertion of the operatoer $Q\_{\alpha}$ 

As a consequence, the expected number of events in a given phase-space region scales with the Wilson coefficient $c\_{\alpha}$ as:

$$ N \propto |\mathcal{A}\_{SMEFT}|^{2} = |\mathcal{A}\_{SM}|^2 + \frac{c\_\alpha}{\Lambda^2} \cdot 2\Re(\mathcal{A}\_{SM}\mathcal{A}\_{Q\_\alpha}^{\dagger})
    +   
 \frac{c\_{\alpha}^{2}}{\Lambda^4}  \cdot |\mathcal{A}\_{Q\_{\alpha}}|^2 $$
 
In order to fit the parameter $c\_{\alpha}$ one would need to provide combine with a SM template ($|\mathcal{A}\_{SM}|^2$), a template for the linear-scaling term $2\Re(\mathcal{A}\_{SM}\mathcal{A}\_{Q\_\alpha}^{\dagger})$ and the tempate for the quadratic term $|\mathcal{A}\_{Q\_{\alpha}}|^2$. The problem stands in the linear term that, being an interference between a dimension-6 and SM amplitudes, can be negative and cannot be interpreted as a p.d.f by combine.

This package provides a workaround to this problem by rewriting the formula in terms of positive definite quantities (amplitude squared). For the simple example of the one-operator case the formule reads as:

$$ 
N = (1 − c\_{\alpha}) \cdot |\mathcal{A}\_{SM}|^2 + c\_{\alpha} \cdot (|\mathcal{A}\_{SM}|^2 + 2\Re(\mathcal{A}\_{SM}\mathcal{A}\_{Q\_\alpha}^{\dagger}) + |\mathcal{A}\_{Q\_{\alpha}}|^2) + (c\_{\alpha}^2 − c\_{\alpha}) \cdot |\mathcal{A}\_{Q\_{\alpha}}|^2 $$

By renaming 

**Sm** = $|\mathcal{A}\_{SM}|^2$,

**Lin**$\_\alpha$ = $2\Re(\mathcal{A}\_{SM}\mathcal{A}\_{Q\_\alpha}^{\dagger})$

**Quad**$\_\alpha$ = $|\mathcal{A}\_{Q\_{\alpha}}|^2$

$$ N = (1 − c\_{\alpha}) \cdot \text{Sm} + c\_{\alpha} \cdot (\text{Sm} + \text{Lin}\_\alpha + \text{Quad}\_\alpha) + (c\_{\alpha}^2 − c\_{\alpha}) \cdot \text{Quad}\_\alpha $$

Where the component **Sm** is the Standard Model amplitude squared, **Quad** is the dimmension-6 amplitude squared and **Sm + Lin + Quad** is given by the square of the sum of the SM and dimension-6 amplitudes $|\mathcal{A}\_{SMEFT}|^2 = | \mathcal{A}\_{SM} + \frac{1}{\Lambda^{2}} \mathcal{A}\_{Q\_{\alpha}} |^2$ for $c\_\alpha = 1$. All these terms are positive definite and are allowed to use in combine.

This model generalises the previous strategy to an arbitrary number of operators where the expected nuber of events in a given phase-space can be now written as:

$$ N \propto |\mathcal{A}\_{SMEFT}|^{2} = 
    |\mathcal{A}\_{SM}|^2
    + 
    \sum\_\alpha\frac{c\_\alpha}{\Lambda^2} \cdot 2\Re(\mathcal{A}\_{SM}\mathcal{A}\_{Q\_\alpha}^{\dagger})
    +   
    \sum\_{\alpha,\beta}\frac{c\_\alpha c\_\beta}{\Lambda^4}  \cdot (\mathcal{A}\_{Q\_\alpha}\mathcal{A}\_{Q\_\beta}^\dagger) $$
    
    
And the rewriting in terms of positive defined quantities reads as:

$$N \propto  \text{Sm} \cdot \left( 1 - \sum\_{\alpha} c\_\alpha + \sum\_{\alpha, \alpha < \beta} \sum\_{\beta} c\_\alpha \cdot c\_\beta  \right) +   \sum\_{\alpha} \left[ \left( c\_\alpha - \sum\_{\alpha \neq \beta} c\_\alpha \cdot c\_\beta \right)  \cdot \left(  \text{Sm} + \text{Lin}\_\alpha + \text{Quad}\_\alpha  \right) \right] + \sum\_\alpha \left(c\_\alpha ^2 - c\_\alpha \right) \cdot \text{Quad}\_\alpha + $$

$$ + \sum\_{\alpha, \alpha<\beta}\sum\_{\beta} c\_\alpha \cdot c\_\beta \cdot \left[ \text{Sm} + \text{Lin}\_\alpha + \text{Quad}\_\alpha + \text{Lin}\_\beta + \text{Quad}\_\beta + 2\cdot \text{Mix}\_{\alpha,\beta} \right] $$

Where 

**Sm** = $|\mathcal{A}\_{SM}|^2$,

**Quad**$\_\alpha$ = $|\mathcal{A}\_{Q\_{\alpha}}|^2$

**Sm + Lin**$\_\alpha$ **+ Quad**$\_\alpha$ = $| \mathcal{A}\_{SM} + \frac{1}{\Lambda^{2}} \mathcal{A}\_{Q\_{\alpha}} |^2$

**Sm + Lin**$\_\alpha$ **+ Quad**$\_\alpha$ **+ Lin**$\_\beta$ **+ Quad**$\_\beta$ **+ 2**$\cdot$ **Mix**$\_{\alpha,\beta}$ = $| \mathcal{A}\_{SM} + \frac{1}{\Lambda^{2}} \mathcal{A}\_{Q\_{\alpha}} + \frac{1}{\Lambda^{2}} \mathcal{A}\_{Q\_{\beta}} |^2$

---- 

# Install:

    cmsrel CMSSW_10_2_13
    cd CMSSW_10_2_13/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/
    git clone git@github.com:amassiro/AnalyticAnomalousCoupling.git

    
# Model to be used:

    AnomalousCouplingEFTNegative
    

# Example Datacards
    
    
# How to run it:

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


# Plotting Tools

This frameworks comes with plotting tools to support analyst with fast instruments to draw results of fits. For obvious reasons plots are available for 1D and 2D scans on the parameters of interests.

For plots of likelihood profiles `scripts/mkEFTScan.py` supports both:

```
./scripts/mkEFTScan.py oned.root -p k_cqq3 -maxNLL 10 -lumi 138 -cms -preliminary -xlabel "c_{qq}^{(3)} [TeV^{-2}]"
./scripts/mkEFTScan.py twod.root -p k_cqq3 k_cqq31 -maxNLL 10 -lumi 138 -cms -preliminary -xlabel "c_{qq}^{(3)} [TeV^{-2}]" -ylabel "c_{qq}^{(3,1)} [TeV^{-2}]"
```

<div href="url">
<img src="./images/1d.png" height="420" width="420" align="center" >
<img src="./images/2d.png" height="420" width="420"align="center"  >
</div>


For profiled fits one usually scans one/two parameter of interest while leaving the others floating and free to maximse the likelihood at a specific POI. A debugging plotting tool can be useful to print the template (full BSM or single templates) at the fixed POI values on the scan. For plotting options can be concatenated to create a gif: `scan` will just draw the scan as a gif, `overall` will read the datacard and retrieve all templates for SM background and BSM EFT (as many operators as you want) and display the stacked distribution (this function also provides support for rateParameters). `signal` does the same without but backgrounds (only `sm` template from datacard). Lastly `templates` method will draw `signal` plus all the single templates that scale as a function of the various parameters.
The process is repeated for all regions of the datacards.

An example is provided in the following gif:
```
./scripts/mkEFTGifs.py -d datacard.txt -s higgsCombineTest.MultiDimFit.mH125.root -op k_cqq3 -rp top:CMS_hww_Topnorm2j WW:CMS_hww_WWnorm2j DY_hardJets:CMS_hww_DYnorm2j_hardJets DY_PUJets:CMS_hww_DYnorm2j_PUJets_2016 --frequency 2 -t scan overall signal templates --variables ewkz_2016_zjj_specified:"m_{jj} [GeV]" ewkz_2016_dycr:"m_{jj} [GeV]" --logy -drawSigma -lumi 138
```


# Negative bin yield    


It may happen that the expected yield (SM+EFT) in a bin evaluates negative. Combine will complain and return the maximum FCN value up to that point in the minimization to force MIGRAD to back out of the region. If one want to disable such behaviour and ignore the negative bin (setting its content to zero) add to the combine command the following run-time arguments

   `--X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT`


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
    
    
    
    
    

    
    
