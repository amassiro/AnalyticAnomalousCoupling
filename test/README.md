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
     
     
      
    
    