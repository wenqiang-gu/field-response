#!/usr/bin/python3

import sys
filename = sys.argv[1]
print(filename)

import bz2
import json
import ROOT

# time vs wire number
# time has unit of us
# icarus assumes three planes in Y, U, V
hfr = [
#ICARUS
 ROOT.TH2F("FieldRes_Y","Y plane (1st ind.) unit: electrons/ns",210, -10.5-0.05, 10.5-0.05, 1000,-60,40 )
,ROOT.TH2F("FieldRes_U","U plane (2nd ind.) unit: electrons/ns",210, -10.5-0.05, 10.5-0.05, 1000,-60,40 )
,ROOT.TH2F("FieldRes_V","V plane (col.) unit: electrons/ns",210, -10.5-0.05, 10.5-0.05, 1000,-60,40 )
#VD coldbox
#  ROOT.TH2F("FieldRes_U","U plane (1st ind.) unit: electrons/ns",420, -20.5-0.05, 20.5-0.05, 1208,0,1208 )
# ,ROOT.TH2F("FieldRes_Y","Y plane (2nd ind.) unit: electrons/ns",420, -20.5-0.05, 20.5-0.05, 1208,0,1208 )
# ,ROOT.TH2F("FieldRes_Z","Z plane (col.) unit: electrons/ns",210, -10.5-0.05, 10.5-0.05, 1205,0,1205 )
]

with bz2.BZ2File(filename) as bzinput:
  obj = json.load(bzinput)
  for iplane in [0,1,2]:
    hfr[iplane].GetXaxis().SetTitle("Wire Number")
    hfr[iplane].GetYaxis().SetTitle("Time [#mus]")
    
    wire_pitch = obj["FieldResponse"]["planes"][iplane]["PlaneResponse"]["pitch"]
    npaths = len(obj["FieldResponse"]["planes"][iplane]["PlaneResponse"]["paths"])
    print("plane: %d, npaths=%d"%(iplane,npaths))
    for ipitch in range(npaths):
      fr_array = obj["FieldResponse"]["planes"][iplane]["PlaneResponse"]["paths"][ipitch]["PathResponse"]["current"]["array"]["elements"]
      nelements = len(fr_array)
      print("nelements=%d"%len(fr_array))
      path_position = obj["FieldResponse"]["planes"][iplane]["PlaneResponse"]["paths"][ipitch]["PathResponse"]["pitchpos"]
      ipos1 = hfr[iplane].GetXaxis().FindBin(path_position / wire_pitch)
      for itick in range(nelements):
        hfr[iplane].SetBinContent(ipos1, itick+1, -fr_array[itick])
        ipos2 = hfr[iplane].GetXaxis().FindBin(-path_position / wire_pitch)
        if hfr[iplane].GetBinContent(ipos2, itick+1)>0:
          print("ignore bin %d" %ipos2)
        else:
          hfr[iplane].SetBinContent(ipos2, itick+1, -fr_array[itick])
        
     
#hfr[1].Draw("colz")

ofile = ROOT.TFile(filename[:-9]+".root","recreate") # assume filename ends with ".json.bz2"
hfr[0].Write()
hfr[1].Write()
hfr[2].Write()
ofile.Close()

# average over wire pitch (1 wire = 10 pitchs)
# hfravg = [
#  ROOT.TH2F("FieldResponse_U","U plane", 1000,0,1000, 21, -106,104)
# ,ROOT.TH2F("FieldResponse_V","V plane", 1000,0,1000, 21, -106,104)
# ,ROOT.TH2F("FieldResponse_W","W plane", 1000,0,1000, 21, -106,104)
# ]
# 
# for iplane in range(3):
#   for i in range(1000):
#     for j in range(21):
#       content =0
#       for idx in range(j*10+1, j*10+11):
#         content += hfr[iplane].GetBinContent(idx,i+1) 
#       content *= 0.1
# 
#       hfravg[iplane].SetBinContent(i+1, j+1, content)
# 
# ofile = ROOT.TFile(filename[:-9]+".root","recreate") # assume filename ends with ".json.bz2"
# hfravg[0].Write()
# hfravg[1].Write()
# hfravg[2].Write()
# ofile.Close()

