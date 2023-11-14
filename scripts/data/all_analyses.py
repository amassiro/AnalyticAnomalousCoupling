import math as mt
import ROOT 

# constants useful to convert from HISZ to WARSAW
vev = 246.22 # GeV
mW = 80.377 # pm 0.012 GeV pdg 
g = 2.*mW / vev
print("g--->", g)

mZ = 91.188 # pm 0.0021 GeV pdg
g1 = (2./vev)*mt.sqrt(mZ**2 - mW**2)
print("g1--->", g1)

fact = 1./mt.sqrt(2)

palette = {
    "Orange": (242, 108, 13), #f26c0d  
    "Yellow": (247, 195, 7), #f7c307
    "LightBlue": (153, 204, 255), #99ccff
    "MediumBlue": (72, 145, 234),  #4891ea
    "MediumBlue2": (56, 145, 224),    #3891e0
    "DarkBlue": (8, 103, 136), #086788
    "Green": (47, 181, 85), #2fb555
    "Green2": (55, 183, 76),  #37b74c
    "Green3": (16,235,52),#10eb34
    "Green4": (68, 175, 105), #44af69
    "Green5": (29,194,106),#1DC26A
    "Green6" : (27,177,97), #1BB161
    "Green7": (108, 198, 140), # 6CC68C
    "GreenLighter": (93, 192, 128),  #5DC080
    "GreenDarker": (14, 150, 78), # 14, 150, 78
    "LightGreen" : (82, 221, 135), #52dd87
    "Violet": (242, 67, 114), #f24372  
    "Pink": (247, 191, 223), #F7BFDF,
    "Peach": (255, 143, 133), #F7C59F
    "Peach2": (255, 146, 51), #FF9233
    "Peach3": (255, 157, 71), #
    "Pink2" : (253, 161, 155), #FD9BA1
    "Orange": (255,156, 51),
    "Orange2": (255,135, 31)
}


an = {
    "WV-semilep": {
        "reference": "10.1016/j.physletb.2022.137438",
        "name": "CMS VBS WV #rightarrow l#nuqq",
        "color": ROOT.kBlack,
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "topU3l",
        "constraints": {
           "expected": {
               
              "cW": [0.00, +0.345, -0.349],
              "cHW": [0.00, +1.575, -1.563],
              "cHB": [0.00, +4.716, -4.711],
              "cHWB": [0.00, +4.349, -4.347],
              "cHbox": [0.00, +9.671, -9.558],
              "cHj1": [0.00, +1.723, -1.747],
              "cHQ1": [0.00, +56.781, -57.679],
              "cHl1": [0.00, +55.164, -55.662]
           },
           "observed": {}
        }
    },
    "SSWW-2018": {
        "reference": "SSWW 2018 scaled to 137 fb^{-1}",
        "name": "SSWW 2018",
        "color": ROOT.kSpring+3,
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "topU3l",
        "constraints": {
            "expected": {
                "cW": [0.00, fact*0.54, fact*(-0.56)],
                "cHW": [0.00, fact*6.35, fact*(-6.85)],
                "cHbox": [0.00, fact*28.05, fact*(-24.15)],
                "cHj1": [0.00, fact*4.95, fact*(-4.89)],
                "cHl1": [0.00, fact*103.8, fact*(-102.6)],
                "cHl3": [0.00, fact*0.64, fact*(-0.86)],
                "cjj11": [0.00, fact*0.54, fact*(-0.42)],
                "cjj31": [0.00, fact*0.02, fact*(-0.02)],
                "cjj38": [0.00, fact*0.02,fact*( -0.02)],
                "cll1": [0.00, fact*0.79, fact*(-16.84)]
            },
            "observed": {}
        }
    },
    "HIG-19-009": {
        "reference": "10.1103/PhysRevD.104.052004",
        "name": "CMS VBF+VH+H#rightarrow 4l",
        "color": palette["Orange"],
        "PAG": "HIG",
        "model": "SMEFTsim",
        "symmetry": "topU3l",
        "constraints": {
            "expected": {
                "cHbox": [0.00, + 0.75, -0.93],
                "cHDD": [0.00, +1.06, -4.60],
                "cHW" : [0.00, +0.39, -0.28],
                "cHWB": [0.00, +0.42, -0.31],
                "cHB": [0.00, +0.03, -0.08],
                "cHWtil": [0.00, +1.11, -1.11],
                "cHWBtil": [0.00, +1.21, -1.21],
                "cHBtil": [0.00, +0.33, -0.33]
            },
            "observed": {
                
            }
        }
    },
    "SMP-22-008": {
        "reference": "CMS-PAS-SMP-22-008",
        "name": "CMS VBS SSWW+#tau_{h}",
        "color": palette["DarkBlue"],
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "U35",
        "constraints":{
            "expected": {
                "cll1": [[-10.9, 0.00], +2.12, -13.5],
                "cqq1": [0.00, +0.681, -0.605],
                "cqq11": [0.00, +0.059, -0.060],
                "cqq3": [0.00, +0.058, -0.060],
                "cqq31": [0.00, +0.172, -0.176],
                "cW": [0.00, +0.818, -0.842],
                "cHW": [0.00, +7.60, -8.68],
                "cHWB": [0.00, +110, -49.6],
                "cHbox": [0.00, +22.7, -20.9],
                "cHDD": [0.00, +45.5, -31.4],
                "cHl1": [0.00, +61.0, -62.0],
                "cHl3": [[0.0, 7.8], +9.94, -1.59],
                "cHq1": [0.00, +5.60, -5.55],
                "cHq3": [0.00, +1.61, -2.82]
            },
            "observed": {}
        }
    },
    "SMP-21-012": {
       "reference": "10.5445/IR/1000161725",
        "name": "CMS VBS VV#rightarrow 4q",
        "color": ROOT.kRed+1,
        "model": "SMEFTsim",
        "symmetry": "topU3l",
        "PAG": "SMP",
        "constraints": {
            "expected":{
                "cHbox": [0.00, +6.20,  -5.88],
                "cHW": [0.00, +1.30, -1.30],
                "cW": [0.00,  +0.256, -0.258]
            },
            "observed": {}
        }
    },
    "SMP-20-005": {
        "reference": "10.1103/PhysRevD.105.052003",
        "name": "CMS W^{#pm}#gamma",
        "color": palette["Yellow"],
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "topU3l",
        "constraints": {
            "expected": {
                "cW": [0.00, +0.052, -0.062]
            },
            "observed": {
                "cW": [-0.009, +0.052, -0.062]
            }
        }   
    },
    "CERN-EP-2023-025": {
        "reference": "10.1103/PhysRevD.108.072003",
        "name": "ATLAS H#rightarrow WW",
        "color": palette["MediumBlue"],
        "PAG": "HIG",
        "model": "SMEFTsim",
        "symmetry": "U35",
        "constraints": {
            "expected": {
                "cHW": [0.00, +1.4, -1.4],
                "cHB": [0.00, +0.66, -0.59],
                "cHWB": [0.00, +1.1, -1.2],
                "cHq1": [0.00, +1.7, -1.9],
                "cHq3": [0.00, +1.2, -0.43],
                "cHu": [0.00, +2.6, -2.0],
                "cHd": [0.00, +2.7, -3.0],
                "cHWtil": [0.00, +1.4, -1.4],
                "cHBtil": [0.00, +0.62, -0.62],
                "cHWBtil": [0.00, +1.1, -1.2]
            },
            "observed": {}
        }
    },
    "CERN-EP-2020-045": {
        "reference": "10.1140/epjc/s10052-020-08734-w",
        "name": "ATLAS Zjj",
        "color": palette["GreenDarker"],
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "U35",
        "constraints": {
            "expected": {
                "cW": [0.00, +0.29, -0.31],
                "cWtil": [0.00, +0.12, -0.12],
                "cHWB": [0.00, +2.10, -3.11],
                "cHWBtil": [0.00, +1.06, -1.06]
            },
            "observed": {},
        }
    },
    "CERN-EP-2021-019": {
        "reference": "10.1007/JHEP07(2021)005",
        "name": "ATLAS pp#rightarrow 4l",
        "color": palette["Pink2"],
        "PAG": "SMP",
        "model": "SMEFTsim",
        "symmetry": "U35",
        "constraints": {
            "expected": {
                "cHG": [0.00, +0.013, -0.011],
                "cHDD": [0.00, +0.45, -0.46],
                "cHWB": [0.00, +0.20, -0.21],
                "cHd": [0.00, +10,-10],
                "cHu": [0.00, +3.7, -3.5],
                "cHe": [0.00, +0.46, -0.47],
                "cHl1": [0.00, +0.38, -0.37],
                "cHl3": [0.00, +0.29, -0.29],
                "cHq1": [0.00, +0.78, 0.81],
                "cHq3": [0.00, +0.35, -0.34],
                "ced": [0.00, +1.8, -1.3],
                "cee": [0.00, +65, -59],
                "ceu": [0.00, +0.45, -0.62],
                "cld": [0.00, +2.5, -1.8],
                "cle": [0.00, +68, -63],
                "cll": [0.00, +43, -39],
                "cll1": [0.00, +0.34, -0.34],
                "clq1": [0.00, 0.4, -0.76],
                "clq3": [0.00, +0.083, -0.059],
                "clu": [0.00, +0.99, -1.4],
                "cqe": [0.00, +0.83, -1.1]
            },
            "observed": {}
        }
    },
    "CMS-SMP-20-014": {
        "reference": "10.1007/JHEP07(2022)032",
        "name": "CMS WZ#rightarrow 3l#nu",
        "color": palette["Violet"],
        "PAG": "SMP",
        "model": "HISZ",
        "symmetry": "",
        "constraints": {
            "expected": {
                "cW": [0.00, (g**3)/4 * (1.3), (g**3)/4 * (-1.3)],
                "cWtil": [0.00, (g**3)/4 * (0.65), (g**3)/4 * (-0.65)],
                "cHl1": [0.00, (g1**2)/8 * (125.0),  (g1**2)/8 * (-86.0)]
            },
            "observed": {}
        }
    },
    "CMS-SMP-18-004": {
        "reference": "10.1103/PhysRevD.102.092001",
        "name": "CMS WW#rightarrow 2l2#nu",
        "color": ROOT.kMagenta+1,
        "PAG": "SMP",
        "model": "HISZ",
        "symmetry": "",
        "constraints": {
            "expected": {
                "cW": [0.00, (g**3)/4 * (2.7), (g**3)/4 * (-2.7)],
                "cHl1": [0.00, (g1**2)/8 * (13.0),  (g1**2)/8 * (-14.0)]
            },
            "observed": {}
        }
    },
    "CMS-SMP-18-008": {
        "reference": "10.1007/JHEP12(2019)062",
        "name": "CMS WV#rightarrow l#nu qq",
        "color": ROOT.kOrange+4,
        "PAG": "SMP",
        "model": "HISZ",
        "symmetry": "",
        "constraints": {
            "expected": {
                "cW": [0.00, (g**3)/4 * (1.59), (g**3)/4 * (-1.58)],
                "cHl1": [0.00, (g1**2)/8 * (8.06),  (g1**2)/8 * (-8.38)]
            },
            "observed": {}
        }
    },
    "CMS-SMP-16-018": {
        "reference": "10.1140/epjc/s10052-018-6049-9",
        "name": "CMS Zjj",
        "color": ROOT.kCyan+1,
        "PAG": "SMP",
        "model": "HISZ",
        "symmetry": "",
        "constraints": {
            "expected": {
                "cW": [0.00, (g**3)/4 * (3.6), (g**3)/4 * (-3.7)]
            },
            "observed": {}
        }
    },
    "CMS-SMP-17-011": {
        "reference": "10.1140/epjc/s10052-019-7585-7",
        "name": "CMS Wjj",
        "color": palette["GreenLighter"],
        "PAG": "SMP",
        "model": "HISZ",
        "symmetry": "",
        "constraints": {
            "expected": {
                "cW": [0.00, (g**3)/4 * (2.5), (g**3)/4 * (-2.5)],
                "cHl1": [0.00, (g1**2)/8 * (61.0),  (g1**2)/8 * (-62.0)]
            },
            "observed": {}
        }
    },
                          
}
