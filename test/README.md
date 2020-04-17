2D contour plot
~~~

Example

                                                                          x          y
    r00t  input/test.root   draw2D.cxx\(\"#mu_{ggH}\",\"#mu_{VBF/VH}\",\"muGGH\",\"muVBF\"\)    
                                                     
    
Plot
~~~

    mkPlotEFT.py \
          --inputFileROOT     SSWW_cHWB_cHl3_ptl2.root \
          --inputFilePairs    test_pairs.py    \
          --outputFile        mytest.root    \
          --sampleNameSM      sm     \
          --folderName        ""   
     
     
    ../scripts/mkPlotEFT.py \
          --inputFileROOT     SSWW_cHWB_cHl3_ptl2.root \
          --inputFilePairs    test_pairs.py    \
          --outputFile        mytest.root    \
          --sampleNameSM      sm     \
          --folderName        ""   
      
    
    