"""
SpectraViewer.py - Useful class and function for astro spectra visualization
Copyright 2021 Zechang Sun email: sunzc18@mails.tsinghua.edu.cn
"""
import pyqtgraph as pg
from defs import EMISSIONLINES


class EmissionLine(pg.InfiniteLine):

    def __init__(self, line=None, redshift=None, pos=None, angle=90, pen=None, movable=False, bounds=None, hoverPen=None, label=None, labelOpts=None, name=None):
        super().__init__(pos=pos, angle=angle, pen=pen, movable=movable, bounds=bounds, hoverPen=hoverPen, label=label, labelOpts=labelOpts, name=name)
        self.line = line
        self.redshift = redshift
        if self.line not in EMISSIONLINES:
            raise NameError("Can't find %s in the dict %s" % (line, EMISSIONLINES))
        if isinstance(redshift, float):
            self.setPos(EMISSIONLINES[self.line]*(1+self.redshift))

    def adjust(self, redshift, line=None):
        if line is not None and isinstance(line, str):
            if line in EMISSIONLINES:
                self.line = line
            else:
                raise NameError("Can't find %s in the dict %s" % (line, EMISSIONLINES))

        if isinstance(redshift, float):
            self.redshift = redshift
        else:
            raise TypeError("Redshift must be float, found %s" % type(redshift))
        self.setPos(EMISSIONLINES[self.line]*(1+self.redshift))
    
    
