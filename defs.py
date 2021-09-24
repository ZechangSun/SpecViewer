from PyQt5 import QtCore


EMISSIONLINES = {"OVI 1031": 1031.912, "OVI 1037": 1037.613, "LYA": 1215.670, "NV 1238": 1238.821, "NV 1242": 1242.804, "CII 1334": 1334.532, "CII 1335": 1335.708, "SiIV": 1393.755, "CIV 1548": 1548.187, "CIV 1550": 1550.772, "HeII": 1640.4, "CIII": 1908.734}
default_background = "#F8F8FF"
EMISSIONSTYLE = {"color": (40, 151, 30), "width": 2, "style": QtCore.Qt.DashLine}
maxwav = 8500
minwav = 4000