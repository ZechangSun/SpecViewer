"""
defs.py - define settings of the GUI (Emission lines and style)
Copyright 2021: Zechang Sun
Email: sunzc18@mails.tsinghua.edu.cn
"""
from PyQt5 import QtCore
import pyqtgraph as pg

EMISSIONSTYLE = {"color": (40, 151, 30), "width": 2, "style": QtCore.Qt.DashLine}
LYASTYLE = {"color": (139, 0, 139), "width": 3, "style": QtCore.Qt.DashLine}
EMISSIONLINES = {"OVI 1031": {"lambda": 1031.912, "style": EMISSIONSTYLE}, 
                 "OVI 1037": {"lambda": 1037.613, "style": EMISSIONSTYLE}, 
                 "LYA": {"lambda": 1215.670, "style": LYASTYLE}, 
                 "NV 1238": {"lambda": 1238.821, "style": EMISSIONSTYLE},
                 "NV 1242": {"lambda": 1242.804, "style": EMISSIONSTYLE}, 
                 "CII 1334": {"lambda": 1334.532, "style": EMISSIONSTYLE}, 
                 "OI": {"lambda": 1355.5977, "style": EMISSIONSTYLE}, 
                 "CII 1335": {"lambda": 1335.708, "style": EMISSIONSTYLE},
                 "SiIV": {"lambda": 1393.755, "style": EMISSIONSTYLE}, 
                 "CIV 1548": {"lambda": 1548.187, "style": EMISSIONSTYLE}, 
                 "CIV 1550": {"lambda": 1550.772, "style": EMISSIONSTYLE}, 
                 "HeII": {"lambda": 1640.4, "style": EMISSIONSTYLE}, 
                 "CIII": {"lambda": 1908.734, "style": EMISSIONSTYLE}}
default_background = "#F8F8FF"
roiPen = pg.mkPen({"color": (255, 140, 0), "width": 2, "style": QtCore.Qt.DotLine})
handlePen = pg.mkPen({"color": "k", "width": 1})
handleTyp = 'f'
interpTyp = 'quadratic'
pointsNum = 1000
