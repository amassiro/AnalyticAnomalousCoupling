#!/usr/bin/env python3

import json
import sys
from sys import exit
argv = sys.argv
sys.argv = argv[:1]
import ROOT
import optparse
import os.path
import string
import logging
import traceback
from array import array
from collections import OrderedDict
import math
from tqdm import tqdm
#import os.path


# ----------------------------------------------------- Scythe --------------------------------------

class Scythe:
    _logger = logging.getLogger('Scythe')
 
    # _____________________________________________________________________________
    def __init__(self):

        variables = {}
        self._variables = variables

        
    # _____________________________________________________________________________
    def defineStyle(self):
    
        print("==================")
        import HiggsAnalysis.AnalyticAnomalousCoupling.tdrStyle as tdrStyle
        tdrStyle.setTDRStyle()
        
        ROOT.TGaxis.SetExponentOffset(-0.08, 0.00,"y")

 
    # _____________________________________________________________________________
    def makePlotEFT(self, gifName="plot.gif", frameDelay=5):
      """
      Draw EFT histograms and create a GIF where the legend label updates dynamically.
      Includes a ratio panel: BSM/SM
      """
      print("===================")
      print("==== mkPlotEFT ====")
      print("===================")
      self.defineStyle()

      fileIn = ROOT.TFile(self._inputFileROOT, "READ")
      self._outFile = ROOT.TFile.Open(self._outputFileName, 'update')

      cc_all_together = ROOT.TCanvas("cc_all_together", "", 800, 600)

      # Define two pads: main + ratio
      pad_main = ROOT.TPad("pad_main", "pad_main", 0, 0.3, 1, 1.0)
      pad_ratio = ROOT.TPad("pad_ratio", "pad_ratio", 0, 0.0, 1, 0.3)
      pad_main.SetBottomMargin(0.02)
      pad_ratio.SetTopMargin(0.05)
      pad_ratio.SetBottomMargin(0.3)
      pad_main.Draw()
      pad_ratio.Draw()

      # SM histogram
      histo_sm = fileIn.Get(self._folderName + self._sampleNameSM).Clone()
      histo_sm.SetLineColor(ROOT.kBlue)
      histo_sm.SetLineWidth(2)
      histo_sm.GetYaxis().SetTitle("Events")
      histo_sm.GetYaxis().SetRangeUser(0., 2 * histo_sm.GetMaximum())
      histo_sm.Write()

      # Create legend once
      pad_main.cd()
      leg = ROOT.TLegend(0.60, 0.70, 0.90, 0.90)
      leg.AddEntry(histo_sm, "SM", "L")

      # Create EFT histogram once
      h_eft = histo_sm.Clone("h_eft")
      h_eft.SetLineColor(ROOT.kRed)
      h_eft.SetLineWidth(2)
      leg_eft_entry = leg.AddEntry(h_eft, "", "L")  # Add entry once, empty label

      for key, pair in tqdm(self._pairs.items(), desc="Processing pairs"):

          # Reset EFT histogram
          h_eft.Reset()
          h_eft.Add(histo_sm, 1)

          # Build variations
          histo_bsm_x = fileIn.Get(self._folderName + "quad_" + pair['xName']).Clone()
          histo_sm_int_bsm_x = fileIn.Get(self._folderName + "sm_lin_quad_" + pair['xName']).Clone()
          histo_int_x = histo_sm_int_bsm_x.Clone()
          histo_int_x.Add(histo_sm, -1)
          histo_int_x.Add(histo_bsm_x, -1)

          h_eft.Add(histo_bsm_x, pair['xValue']**2)
          h_eft.Add(histo_int_x, pair['xValue'])

          if 'yName' in pair:
              histo_bsm_y = fileIn.Get(self._folderName + "quad_" + pair['yName']).Clone()
              histo_sm_int_bsm_y = fileIn.Get(self._folderName + "sm_lin_quad_" + pair['yName']).Clone()
              histo_int_y = histo_sm_int_bsm_y.Clone()
              histo_int_y.Add(histo_sm, -1)
              histo_int_y.Add(histo_bsm_y, -1)

              xy_name = self._folderName + f"sm_lin_quad_mixed_{pair['xName']}_{pair['yName']}"
              if xy_name not in [i.GetName() for i in fileIn.GetListOfKeys()]:
                  xy_name = self._folderName + f"sm_lin_quad_mixed_{pair['yName']}_{pair['xName']}"
              histo_int_xy = fileIn.Get(xy_name).Clone()
              histo_int_xy.Add(histo_sm, 1)
              histo_int_xy.Add(histo_sm_int_bsm_x, -1)
              histo_int_xy.Add(histo_sm_int_bsm_y, -1)

              h_eft.Add(histo_bsm_y, pair['yValue']**2)
              h_eft.Add(histo_int_y, pair['yValue'])
              h_eft.Add(histo_int_xy, pair['xValue']*pair['yValue'])

          # Update legend label
          if 'yName' in pair:
              legend_label = f"{pair['xName']}={pair['xValue']:.2f} ; {pair['yName']}={pair['yValue']:.2f}"
          else:
              legend_label = f"{pair['xName']}={pair['xValue']:.2f}"
          leg_eft_entry.SetLabel(legend_label)

          # --- Draw top pad ---
          pad_main.cd()
          pad_main.Clear()
          #ROOT.gPad.SetLogy(1)
          histo_sm.Draw()
          h_eft.Draw("same")
          leg.Draw()
          pad_main.Update()

          # --- Draw ratio pad ---
          pad_ratio.cd()
          pad_ratio.Clear()
          h_ratio = h_eft.Clone("h_ratio")
          h_ratio.Divide(histo_sm)
          h_ratio.SetLineColor(ROOT.kRed)
          h_ratio.SetMarkerSize(0)
          h_ratio.GetYaxis().SetTitle("BSM / SM")
          h_ratio.GetYaxis().SetNdivisions(505)
          h_ratio.GetYaxis().SetTitleSize(0.15)
          h_ratio.GetYaxis().SetTitleOffset(0.35)
          h_ratio.GetXaxis().SetTitleSize(0.15)
          h_ratio.GetXaxis().SetLabelSize(0.12)
          h_ratio.SetMinimum(0)
          h_ratio.SetMaximum(2)
          h_ratio.Draw("hist")
          pad_ratio.Update()

          # Save frame
          cc_all_together.Update()
          if self._makeGif:
              cc_all_together.Print(f"{gifName}+{frameDelay}")
          else:
              cc_all_together.SaveAs("plot.png")

       
       



if __name__ == '__main__':
    sys.argv = argv
    
    print ('''
----------------------------------------------------------------------------------------------------------------------------------

       ____|  ____| __ __|             |         |         
       __|    |        |        __ \   |   _ \   __|   __|  
       |      __|      |        |   |  |  (   |  |   \__ \ 
      _____| _|       _|        .__/  _| \___/  \__| ____/ 
                               _|                          
     
----------------------------------------------------------------------------------------------------------------------------------
''')    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFileROOT'         , dest='inputFileROOT'         , help='input file with histograms'                                   , default='input.root')
    parser.add_option('--inputFilePairs'        , dest='inputFilePairs'        , help='input file with pair of operators values to be plotted'       , default='pairs.py')
    parser.add_option('--outputFile'            , dest='outputFile'            , help='output file with TCanvas'                                     , default='output.root')
    parser.add_option('--sampleNameSM'          , dest='sampleNameSM'          , help='sample name in as in histogram for SM contribution'           , default='sm')
    parser.add_option('--folderName'            , dest='folderName'            , help='folder name inside the root file where histograms are stored' , default='mll')
    parser.add_option('--gif'                   , dest='makeGif'               , help='Make GIF animation', default=False, action='store_true')
          
    # read default parsing options as well
    #addOptions(parser)
    #loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print (" inputFileROOT         =          ", opt.inputFileROOT)
    print (" inputFilePairs        =          ", opt.inputFilePairs)
    print (" outputFile            =          ", opt.outputFile)
    print (" sampleNameSM          =          ", opt.sampleNameSM)
    print (" folderName            =          ", opt.folderName)


    factory = Scythe()
    factory._outputFileName    = opt.outputFile
    factory._inputFileROOT     = opt.inputFileROOT
    factory._sampleNameSM      = opt.sampleNameSM
    factory._folderName        = opt.folderName
    factory._makeGif           = opt.makeGif

    # ~~~~
    pairs = {}

    if os.path.exists(opt.inputFilePairs):
      with open(opt.inputFilePairs, 'r') as handle:
          code = handle.read()
          exec(code)

    factory._pairs = pairs


    # ~~~~

    factory.makePlotEFT()
    
    print ('... and now closing ...')
        
       
       
       
       