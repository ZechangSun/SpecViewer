"""
Mainwindow.py - Mainwindow for the GUI.
Copyright 2021: Zechang Sun
Email: sunzc18@mails.tsinghua.edu.cn
"""
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QCheckBox, QFileDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QTextEdit, QDialog
from Widget import SelectWindow
from EmissionLine import EmissionLine
from scipy.interpolate import interp1d
import pyqtgraph as pg
import numpy as np
import os
import defs
import script


class MainWindow(QMainWindow):

    # signal detect whether reach the end of the dataset
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # set title and size
        self.setWindowTitle('SpecViewer')
        self.setWindowIcon(QIcon(os.path.join("asset", "teleIcon.ico")))
        self.width = 1500
        self.height = int(0.618*self.width)
        self.resize(self.width, self.height)

        # menu bar setting
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("Files")
        self.openAction = QAction("Open")
        self.saveAction = QAction("Save")
        self.exitAction = QAction("Exit")
        # set shortcut
        self.openAction.setShortcut("Ctrl+O")
        self.exitAction.setShortcut("Ctrl+E")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveDataProduct = QAction("Save Data Product")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveDataProduct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        self.helpMenu = self.menu.addMenu("Help")
        self.settingMenu = self.menu.addMenu("Settings")
        self.enableTopX = QAction("Enable X Movable", checkable=True)
        self.enableTopX.setChecked(True)
        self.settingMenu.addAction(self.enableTopX)
        self.enableTopY = QAction("Enable Y Movable", checkable=True)
        self.enableTopY.setChecked(False)
        self.settingMenu.addAction(self.enableTopY)
        self.displayEmissionLine = QAction("Display Emission Line", checkable=True)
        self.displayLabel = QAction("Display Emission Label", checkable=True)
        self.settingMenu.addAction(self.displayEmissionLine)
        self.settingMenu.addAction(self.displayLabel)
        self.displayEmissionLine.setChecked(True)
        self.displayLabel.setChecked(True)
        self.selectEmissionLine = QAction("Select Emission Lines")
        self.settingMenu.addAction(self.selectEmissionLine)
        self.selectEmissionLine.triggered.connect(self.select_emission_line)

        # state  bar setting
        self.statusBar = self.statusBar()

        # set layout
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        left_widget = QWidget()
        right_widget = QWidget()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        right_widget.setLayout(right_layout)
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_layout.setStretch(0, 4)
        main_layout.setStretch(4, 6)

        # set check box and text edit
        self.checkbox1 = QCheckBox("QSO without BAL?")
        self.checkbox1.setShortcut("Alt+1")
        self.checkbox2 = QCheckBox("DLA?")
        self.checkbox2.setShortcut("Alt+2")
        self.checkbox3 = QCheckBox("Associated DLA?")
        self.checkbox3.setShortcut("Alt+3")
        self.checkbox4 = QCheckBox("Interesting?")
        self.checkbox4.setShortcut("Alt+4")
        self.buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        self.buttonWidget.setLayout(buttonLayout)
        self.textEdit = QTextEdit()
        self.fileWidget = QWidget()
        fileLayout = QHBoxLayout()
        self.fileWidget.setLayout(fileLayout)
        self.setWidget = QWidget()
        setLayout = QHBoxLayout()
        self.setWidget.setLayout(setLayout)

        # set slider
        self.smoothIndicator = QLabel("Smooth: 1 pixel")
        self.smoothSlider = QSlider(Qt.Horizontal)
        self.smoothSlider.setMinimum(1)
        self.smoothSlider.setMaximum(15)
        self.smoothSlider.setSingleStep(2)
        self.smoothSlider.setTickPosition(QSlider.TicksBelow)
        self.smoothSlider.sliderReleased.connect(self.smooth)
        self.smoothSlider.valueChanged.connect(self.updateSmoothIndicator)

        self.noiseIndicator = QLabel("Drop Pixels with SNR<Inf")
        self.noiseSlider = QSlider(Qt.Horizontal)
        self.noiseSlider.setMinimum(0)
        self.noiseSlider.setMaximum(50)
        self.noiseSlider.valueChanged.connect(self.noise_clip)

        # add widget
        self.label = QLabel("Any Comment?")
        self.label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.checkbox1)
        right_layout.addWidget(self.checkbox2)
        right_layout.addWidget(self.checkbox3)
        right_layout.addWidget(self.checkbox4)
        right_layout.addWidget(self.fileWidget)
        right_layout.addWidget(self.setWidget)
        right_layout.addWidget(self.buttonWidget)
        right_layout.addWidget(self.smoothIndicator)
        right_layout.addWidget(self.smoothSlider)
        right_layout.addWidget(self.noiseIndicator)
        right_layout.addWidget(self.noiseSlider)
        right_layout.addWidget(self.label)
        right_layout.addWidget(self.textEdit)

        # add button
        self.backButton = QPushButton("Back")
        self.nextButton = QPushButton("Next")
        buttonLayout.addWidget(self.backButton)
        buttonLayout.addWidget(self.nextButton)
        self.backButton.pressed.connect(self.lastSpectra)
        self.nextButton.pressed.connect(self.nextSpectra)
        self.backButton.setShortcut("left")
        self.nextButton.setShortcut("right")

        self.openButton = QPushButton("Open")
        self.exitButton = QPushButton("Exit")
        self.saveButton = QPushButton("Save")
        fileLayout.addWidget(self.openButton)
        fileLayout.addWidget(self.exitButton)
        fileLayout.addWidget(self.saveButton)
        self.openButton.pressed.connect(self.load_data)
        self.exitButton.pressed.connect(QCoreApplication.quit)
        self.saveButton.pressed.connect(self.save_result)

        self.selectButton = QPushButton("Select Emission Line")
        setLayout.addWidget(self.selectButton)
        self.selectButton.pressed.connect(self.select_emission_line)

        # set pyqtgraph widget
        pg.setConfigOptions(background=defs.default_background)
        self.pgwindow = pg.GraphicsWindow()
        left_layout.addWidget(self.pgwindow)

        self.exitAction.triggered.connect(QCoreApplication.quit)
        self.openAction.triggered.connect(self.load_data)
        self.saveAction.triggered.connect(self.save_result)
        self.saveDataProduct.triggered.connect(self.save_cont)
        self.enableTopX.triggered.connect(self.enableTopMovable)
        self.enableTopY.triggered.connect(self.enableTopMovable)
        self.displayEmissionLine.triggered.connect(self.setEmissionDisplay)
        self.displayLabel.triggered.connect(self.setLabelDisplay)

        # dict store the spectra information
        self.data = []
        self.result = []

        # data cursor
        self.cursor = 0
        self.z = None

        # add plot
        self.topPanel = self.pgwindow.addPlot(row=1, col=0)
        self.bottomPanel = self.pgwindow.addPlot(row=2, col=0)
        self.bottomPanel.setMouseEnabled(x=False, y=False)
        self.topPanel.setMouseEnabled(y=False)
        self.topPanel.addLegend()
        self.bottomPanel.addLegend()
        self.region = pg.LinearRegionItem()
        self.bottomPanel.addItem(self.region, ignoreBounds=True)
        self.region.sigRegionChanged.connect(self.updateRegion)
        self.topPanel.scene().sigMouseMoved.connect(self.mouseMoved)
        self.topPanel.scene().sigMouseClicked.connect(self.mouseClicked)
        self.LineElems = {}
        self.LineElems["TopFlux"] = pg.PlotCurveItem(clear=True, pen="b", name="FLUX")
        self.LineElems["TopErr"] = pg.PlotCurveItem(clear=True, pen="r", name="ERROR")
        self.LineElems["BottomFlux"] = pg.PlotCurveItem(clear=True, pen="k", name="FLUX")
        self.LineElems["BottomErr"] = pg.PlotCurveItem(clear=True, pen="r", name="ERROR")
        self.LineElems["BottomCont"] = pg.PlotCurveItem(clear=True, pen=pg.mkPen(color="r", width=1.5), name="CONT")
        self.topPanel.addItem(self.LineElems["TopFlux"])
        self.topPanel.addItem(self.LineElems["TopErr"])
        self.bottomPanel.addItem(self.LineElems["BottomFlux"])
        self.bottomPanel.addItem(self.LineElems["BottomErr"])
        self.bottomPanel.addItem(self.LineElems["BottomCont"])

        # add EmissionLine
        self.EmissionLines = {}
        for key in defs.EMISSIONLINES:
            self.EmissionLines[key] = EmissionLine(key, redshift=None, movable=True, pen=pg.mkPen(defs.EMISSIONLINES[key]["style"]), label=key, labelOpts={"movable": True, "color": "k"})
            self.EmissionLines[key].sigDragged.connect(self.updateEmission)
            self.EmissionLines[key].setToolTip("<b>%s:</b> %.2f Angstorm" % (key, defs.EMISSIONLINES[key]["lambda"]))
            self.EmissionLines[key].setLabelVisible(False)
            self.topPanel.addItem(self.EmissionLines[key], ignoreBounds=True)

        self.EmissionLineVisibleState = {}
        for key in defs.EMISSIONLINES:
            self.EmissionLineVisibleState[key] = True

        # add ROI
        self.roi = pg.PolyLineROI([], closed=False, pen=defs.roiPen)
        self.roi.handlePen = defs.handlePen
        self.topPanel.addItem(self.roi)
        clearROI = self.topPanel.vb.menu.addAction("Clear")
        clearROI.triggered.connect(self.clearROI)
        plotROI = self.topPanel.vb.menu.addAction("Plot")
        plotROI.triggered.connect(self.plotCont)

        # sconnect signal
        self.signal.connect(self.warning)

    def load_data(self):
        files, file_type = QFileDialog.getOpenFileNames(self, "Load Spectra", filter="npz Files (*.npz);;Text Files (*.txt);;CSV Files (*.csv)")
        if len(files) == 0:
            print("No Files Selected!!!")
        else:
            self.data = script.load(files, file_type)
            self.result = [{"File": self.data[i]["file"], "BAL": False, "DLA": False, "Associated DLA": False, "Interesting": False, "comment": "", "z": self.data[i]["z"], "cont": ([], [])} for i in range(len(self.data))]
            self.plot()

    def warning(self):
        QMessageBox.information(self, "Notice", "Have reached the end of the dataset...", QMessageBox.Yes)

    def updateSmoothIndicator(self):
        self.smoothIndicator.setText("Smooth: %2i pixel" % self.smoothSlider.value())

    def smooth(self):
        kernel_size = self.smoothSlider.value()
        kernel = np.ones(kernel_size, dtype=float)/kernel_size
        flux_smoothed = np.convolve(self.data[self.cursor]["flux"], kernel, mode="same")
        err_smoothed = np.convolve(self.data[self.cursor]["error"], kernel, mode="same")
        self.LineElems["TopFlux"].setData(self.data[self.cursor]["wav"], flux_smoothed)
        self.LineElems["TopErr"].setData(self.data[self.cursor]["wav"], err_smoothed)

    def noise_clip(self):
        if "SNR" not in self.data[self.cursor]:
            self.data[self.cursor]["SNR"] = self.data[self.cursor]["flux"]/(self.data[self.cursor]["error"]+1e-30)
        critical_point = np.percentile(self.data[self.cursor]["SNR"], 100-self.noiseSlider.value())
        self.noiseIndicator.setText("Drop Pixels with SNR < %2.2f" % critical_point)
        sig = self.data[self.cursor]["SNR"] < critical_point
        wav = self.data[self.cursor]["wav"][sig]
        flux = self.data[self.cursor]["flux"][sig]
        err = self.data[self.cursor]["error"][sig]
        self.LineElems["TopFlux"].setData(wav, flux)
        self.LineElems["TopErr"].setData(wav, err)

    def plot(self):
        self.clearROI()
        maxwav, minwav = max(self.data[self.cursor]["wav"]), min(self.data[self.cursor]["wav"])
        fmax, fmin = max(self.data[self.cursor]["flux"]), min(self.data[self.cursor]["flux"])
        self.z = self.data[self.cursor]["z"]
        for key in defs.EMISSIONLINES:
            self.EmissionLines[key].setVisible(True)
            self.EmissionLines[key].adjust(self.z)
            self.EmissionLines[key].label.setPosition(np.random.uniform(0, 1))
            self.EmissionLines[key].label.updatePosition()
            self.EmissionLines[key].setLabelVisible(True)
        self.topPanel.setXRange(0.98*minwav, 1.02*maxwav, padding=0)
        self.topPanel.setYRange(0.98*fmin, 1.02*fmax, padding=0)
        self.bottomPanel.setXRange(0.98*minwav, 1.02*maxwav, padding=0)
        self.bottomPanel.setYRange(0.98*fmin, 1.02*fmax, padding=0)
        self.LineElems["TopFlux"].setData(self.data[self.cursor]["wav"], self.data[self.cursor]["flux"])
        self.LineElems["TopErr"].setData(self.data[self.cursor]["wav"], self.data[self.cursor]["error"])
        self.LineElems["BottomFlux"].setData(self.data[self.cursor]["wav"], self.data[self.cursor]["flux"])
        self.LineElems["BottomErr"].setData(self.data[self.cursor]["wav"], self.data[self.cursor]["error"])
        xROI, yROI = self.result[self.cursor]["cont"][0], self.result[self.cursor]["cont"][1]
        if xROI and yROI:
            nx, ny = self.interp(xROI, yROI)
            self.LineElems["BottomCont"].setData(nx, ny)
            roiPos = list(map(lambda x: (x[0], x[1]), zip(xROI, yROI)))
            self.roi.setPoints(roiPos)
        self.region.setBounds((minwav, maxwav))
        self.region.setRegion((minwav, maxwav))

    def updateRegion(self):
        minX, maxX = self.region.getRegion()
        self.topPanel.setXRange(minX, maxX, padding=0)

    def updateEmission(self, e):
        current_pos = e.getXPos()
        self.z = current_pos/defs.EMISSIONLINES[e.line]["lambda"] - 1.
        for key in defs.EMISSIONLINES:
            self.EmissionLines[key].adjust(self.z)
        return

    def mouseMoved(self, evt):
        if self.topPanel.sceneBoundingRect().contains(evt.x(), evt.y()):
            mousePoint = self.topPanel.vb.mapSceneToView(evt)
            if len(self.data) > 0 and self.cursor < len(self.data):
                self.statusBar.showMessage("File: %s   ;   MousePos: x = %.2f, y = %e   ;   Redshift: %.3f" % (self.data[self.cursor]["file"], mousePoint.x(), mousePoint.y(), self.z))
            else:
                self.statusBar.clearMessage()
        else:
            self.statusBar.clearMessage()

    def mouseClicked(self, evt):
        if evt.double():
            mousePos = evt.scenePos()
            if self.topPanel.sceneBoundingRect().contains(mousePos):
                mousePoint = self.topPanel.vb.mapSceneToView(mousePos)
                x, y = mousePoint.x(), mousePoint.y()
                info = {'name': None, 'type': defs.handleTyp, 'pos': (x, y)}
                h = self.roi.addHandle(info=info)
                if len(self.roi.handles) >= 2:
                    h0 = self.roi.handles[-2]['item']
                    self.roi.addSegment(h0, h)

    def clearROI(self):
        self.roi.clearPoints()
        self.LineElems["BottomCont"].setData([], [])

    def plotCont(self):
        positions = self.roi.getState()['points']
        positions.sort(key=(lambda p: p.x()))
        x = list(map(lambda p: p.x(), positions))
        y = list(map(lambda p: p.y(), positions))
        if x and y:
            nx, ny = self.interp(x, y)
            self.LineElems["BottomCont"].setData(nx, ny)
            self.result[self.cursor]["cont"] = (x, y)

    def interp(self, x, y):
        func = interp1d(x, y, kind=defs.interpTyp, assume_sorted=True)
        nx = np.linspace(min(x), max(x), num=defs.pointsNum)
        ny = func(nx)
        return nx, ny

    def nextSpectra(self):
        if len(self.data) > 0:
            self.result[self.cursor]["File"] = self.data[self.cursor]["file"]
            self.result[self.cursor]["BAL"] = self.checkbox1.isChecked()
            self.result[self.cursor]["DLA"] = self.checkbox2.isChecked()
            self.result[self.cursor]["Associated DLA"] = self.checkbox3.isChecked()
            self.result[self.cursor]["Interesting"] = self.checkbox4.isChecked()
            self.result[self.cursor]["z"] = self.z
            self.result[self.cursor]["comment"] = self.textEdit.toPlainText()
            if self.cursor + 1 < len(self.data):
                self.cursor = (1 + self.cursor)
            else:
                self.signal.emit()
                self.cursor = 0
            self.checkbox1.setChecked(self.result[self.cursor]["BAL"])
            self.checkbox2.setChecked(self.result[self.cursor]["DLA"])
            self.checkbox3.setChecked(self.result[self.cursor]["Associated DLA"])
            self.checkbox4.setChecked(self.result[self.cursor]["Interesting"])
            self.textEdit.setPlainText(self.result[self.cursor]["comment"])
            self.plot()
            self.smoothIndicator.setText("Smooth: %2i pixel" % 1)
            self.noiseIndicator.setText("Drop Pixels with SNR < Inf")
            self.noiseSlider.setValue(0)
            self.smoothSlider.setValue(1)

    def lastSpectra(self):
        if len(self.data) > 0:
            self.result[self.cursor]["File"] = self.data[self.cursor]["file"]
            self.result[self.cursor]["BAL"] = self.checkbox1.isChecked()
            self.result[self.cursor]["DLA"] = self.checkbox2.isChecked()
            self.result[self.cursor]["Associated DLA"] = self.checkbox3.isChecked()
            self.result[self.cursor]["Interesting"] = self.checkbox4.isChecked()
            self.result[self.cursor]["z"] = self.z
            self.result[self.cursor]["comment"] = self.textEdit.toPlainText()
            if self.cursor-1 >= 0:
                self.cursor = self.cursor-1
            else:
                self.signal.emit()
                self.cursor = len(self.data)-1
            self.checkbox1.setChecked(self.result[self.cursor]["BAL"])
            self.checkbox2.setChecked(self.result[self.cursor]["DLA"])
            self.checkbox3.setChecked(self.result[self.cursor]["Associated DLA"])
            self.checkbox4.setChecked(self.result[self.cursor]["Interesting"])
            self.textEdit.setPlainText(self.result[self.cursor]["comment"])
            self.plot()
            self.smoothIndicator.setText("Smooth: %2i pixel" % 1)
            self.noiseIndicator.setText("Drop Pixels with SNR < Inf")
            self.noiseSlider.setValue(0)
            self.smoothSlider.setValue(1)

    def save_result(self):
        result_file, file_type = QFileDialog.getSaveFileName(self, 'Save Result', filter="CSV File (*.csv)")
        script.save(self.result, result_file, file_type)

    def save_cont(self):
        dir = QFileDialog.getExistingDirectory(self, caption="Data Product Dict")
        script.save_cont(self.result, self.data, dir)

    def enableTopMovable(self):
        self.topPanel.setMouseEnabled(x=self.enableTopX.isChecked(), y=self.enableTopY.isChecked())

    def setEmissionDisplay(self):
        for key in defs.EMISSIONLINES:
            self.EmissionLineVisibleState[key] = self.displayEmissionLine.isChecked()
        self.updateEmissionDisplay()
        self.displayLabel.setChecked(self.displayEmissionLine.isChecked())

    def updateEmissionDisplay(self):
        for key in defs.EMISSIONLINES:
            self.EmissionLines[key].setVisible(self.EmissionLineVisibleState[key])
            self.EmissionLines[key].setLabelVisible(self.EmissionLineVisibleState[key])

    def setLabelDisplay(self):
        for key in defs.EMISSIONLINES:
            self.EmissionLines[key].setLabelVisible(self.displayLabel.isChecked())

    def select_emission_line(self):
        self.select_window = SelectWindow(self.EmissionLineVisibleState)
        self.select_window.show()
        self.select_window.exec_()
        self.EmissionLineVisibleState = self.select_window.emission_line_states
        del self.select_window
        self.updateEmissionDisplay()
