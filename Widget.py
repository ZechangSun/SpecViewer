"""
Mainwindow.py - Mainwindow for the GUI.
Copyright 2021: Zechang Sun
Email: sunzc18@mails.tsinghua.edu.cn
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QGridLayout, QDialog
import numpy as np


class SelectWindow(QDialog):
    """Dialog window to select which emission lines to be displayed

    Args:
        emission_lines: dict {"line name": True|False}
    """
    def __init__(self, emission_lines):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Select which emission lines to be displayed")
        self.emission_line_states = emission_lines
        self.width = 1000
        self.height = int(0.618*self.width)
        self.resize(self.width, self.height)

        layout = QGridLayout()
        self.setLayout(layout)
        n_emission_line = len(self.emission_line_states)
        nrows = int(np.sqrt(n_emission_line))+1
        self.checkbox = {}
        for idx, key in enumerate(self.emission_line_states):
            xx = idx//nrows
            yy = idx%nrows
            self.checkbox[key] = QCheckBox(key)
            layout.addWidget(self.checkbox[key], xx, yy)
            self.checkbox[key].setChecked(self.emission_line_states[key])

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'SpecViewer', "Want to exit?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            for key in self.emission_line_states:
                self.emission_line_states[key] = self.checkbox[key].isChecked()
            event.accept()
        else:
            event.ignore()
