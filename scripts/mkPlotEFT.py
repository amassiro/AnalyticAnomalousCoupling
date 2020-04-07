#!/usr/bin/env python

import json
import sys
from sys import exit
argv = sys.argv
sys.argv = argv[:1]
import ROOT
import optparse
#import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path
import string
import logging
#import LatinoAnalysis.Gardener.odict as odict
import traceback
from array import array
from collections import OrderedDict
import math

#import os.path



# ----------------------------------------------------- Scythe --------------------------------------

class Scythe:
    _logger = logging.getLogger('Scythe')
 
    # _____________________________________________________________________________
    def __init__(self):

        variables = {}
        self._variables = variables

        
 
    # _____________________________________________________________________________
    def makePlotEFT(self):

        print "==================="
        print "==== mkPlotEFT ===="
        print "==================="
        
        print " self._pairs " , self._pairs
        
        
        #
        #  self._pairs = {
        #                 
        #                 'cG_cGtil_04_03': {
        #                     'xName': 'cG',
        #                     'yName': 'cGtil',
        #                     'xValue': 0.4,
        #                     'yValue': 0.3,    
        #                 }
        #                 
        #                }
        #

        
        fileIn = ROOT.TFile(self._inputFileROOT, "READ")
        
        self._outFile = ROOT.TFile.Open( self._outputFileName, 'update')  # need to append in an existing file if more cuts/variables are wanted
       
        self._outFile.cd    ( "./" )
        
        TCanvas cc_all_together("cc_all_together", "", 800, 600)
        histo_sm  = fileIn.Get( self._folderName + "/histo_" + self._sampleNameSM)
        histo_sm.Draw();
        
        for nameHR, pair in self._pairs.iteritems():
        
          self._outFile.mkdir ( nameHR )
          self._outFile.cd    ( nameHR )

          histo_bsm_x  = fileIn.Get( self._folderName + "/histo_" + "_quadratic_" + pair['xName'] )
          histo_int_x  = fileIn.Get( self._folderName + "/histo_" + "_linear_"    + pair['xName'] )
          histo_bsm_y  = fileIn.Get( self._folderName + "/histo_" + "_quadratic_" + pair['yName'] )
          histo_int_y  = fileIn.Get( self._folderName + "/histo_" + "_linear_"    + pair['yName'] )
          histo_int_xy = fileIn.Get( self._folderName + "/histo_" + "_linear_mixed_" + pair['xName'] + "_" + pair['yName'] )
          
          histo_varied = histo_sm.Clone ("histo_" + self._sampleNameSM + "_varied_" + pair['xName'] + "_" + pair['xValue'] + "_" + pair['yName'] + "_" + pair['yValue'] )
                    
          histo_varied.Add(histo_bsm_x, pair['xValue']*pair['xValue'] )
          histo_varied.Add(histo_int_x, pair['xValue'] )
          histo_varied.Add(histo_bsm_y, pair['yValue']*pair['yValue'] )
          histo_varied.Add(histo_int_y, pair['yValue'] )
          histo_varied.Add(histo_int_xy, pair['xValue']*pair['yValue'] )
          
          #histo_varied.SetName  ('histo_' + cardName)
          #histo_varied.SetTitle ('histo_' + cardName)
          histo_varied.Write()
          
          histo_varied.Draw("same");
          
       self._outFile.cd    ( "./" )
       cc_all_together.Write()
       



if __name__ == '__main__':
    sys.argv = argv
    
    print '''
----------------------------------------------------------------------------------------------------------------------------------

       ____|  ____| __ __|             |         |         
       __|    |        |        __ \   |   _ \   __|   __|  
       |      __|      |        |   |  |  (   |  |   \__ \ 
      _____| _|       _|        .__/  _| \___/  \__| ____/ 
                               _|                          
     
----------------------------------------------------------------------------------------------------------------------------------
'''    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFileROOT'         , dest='inputFileROOT'         , help='input file with histograms'                                   , default='input.root')
    parser.add_option('--inputFilePairs'        , dest='inputFilePairs'        , help='input file with pair of operators values to be plotted'       , default='pairs.py')
    parser.add_option('--outputFile'            , dest='outputFile'            , help='output file with TCanvas'                                     , default='output.root')
    parser.add_option('--sampleNameSM'          , dest='sampleNameSM'          , help='sample name in as in histogram for SM contribution'           , default='sm')
    parser.add_option('--folderName'            , dest='folderName'            , help='folder name inside the root file where histograms are stored' , default='mll')
          
    # read default parsing options as well
    addOptions(parser)
    loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print " inputFilePairs        =          ", opt.inputFilePairs
    print " outputFile            =          ", opt.outputFile
    print " sampleNameSM          =          ", opt.sampleNameSM
    print " folderName            =          ", opt.folderName


    factory = Scythe()
    factory._outputFileName    = opt.outputFile
    factory._inputFileROOT     = opt.inputFileROOT
    factory._sampleNameSM      = opt.sampleNameSM
    factory._folderName        = opt.folderName


    # ~~~~
    pairs = {}

    if os.path.exists(opt.inputFilePairs) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()

    factory._pairs = pairs


    # ~~~~

    factory.makePlotEFT()
    
    print '... and now closing ...'
        
       
       
       
       