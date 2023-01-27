import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings

from MainWindow import Ui_MainWindow

from python_methods.ZigZag import *
from python_methods.Spiral import *

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        
        # Atributes for saving values
        self.dataZIGZAG = {}
        self.dataZIGRAND = {}
        self.dataSPIRAL = {}
        self.source = []

    #Connect the signal to the appropriate buttons
    def connectSignalsSlots(self):
       #Push buttons
       self.btnRadiation.clicked.connect(self.radiation)
       self.btnDetector.clicked.connect(self.detector)
       self.btnEstSource.clicked.connect(self.estimateSource)
       self.btnRandSource.clicked.connect(self.generateSource)
       self.btnPlot.clicked.connect(self.plotGraph)
       #Radio buttons
       self.checkZIGZAG.toggled.connect(self.radButZigZag)
       self.checkZIGRAND.toggled.connect(self.radButZigRand)
       self.checkSPIRAL.toggled.connect(self.radButSpiral)

    def radButZigZag(self):
        DetectorDialog(self).ZigZag()
    def radButZigRand(self):
        DetectorDialog(self).ZigRand()
    def radButSpiral(self):
        DetectorDialog(self).Spiral()
        
    #Open radiation/detector dialog window
    def radiation(self):
        dialog = RadiationDialog(self)
        dialog.exec()
    def detector(self):
        dialog = DetectorDialog(self)
        dialog.exec()

    def generateSource(self):
        radiation = RadiationDialog(self).giveRadiation()
        detector = DetectorDialog(self).giveDetector()
        Amax = radiation['A_max']; Amin = radiation['A_min']
        xmax = detector['width']; ymax = detector['height']
        self.source = point_source(xmax, ymax, Amin, Amax)
        self.x0lineEditRand.setText((str(round(self.source[0], 2)))); self.y0lineEditRand.setText(str(round(self.source[1], 2)))
        self.A0lineEditRand.setText(str(round(self.source[-1], 2)))

    def estimateSource(self):
        radiation = RadiationDialog(self).giveRadiation()
        detector = DetectorDialog(self).giveDetector()
        if self.checkZIGZAG.isChecked():
            self.dataZIGZAG = combination(radiation, detector, flyover, locationCF, self.source)
            self.x0lineEditEst.setText(str(round(self.dataZIGZAG["sourceCF"][0], 2)) + " +/- "  + str(round(self.dataZIGZAG["sourceCF_stDev"][0], 2)))
            self.y0lineEditEst.setText(str(round(self.dataZIGZAG["sourceCF"][1], 2)) + " +/- " + str(round(self.dataZIGZAG["sourceCF_stDev"][1], 2)))
            self.A0lineEditEst.setText(str(round(self.dataZIGZAG['A0'][0], 2)) + " +/- " + str(round(self.dataZIGZAG['A0'][1], 2)))
        elif self.checkZIGRAND.isChecked():
            self.dataZIGRAND = combination(radiation, detector, flyoverZigRand, locationCF, self.source)
            self.x0lineEditEst.setText(str(round(self.dataZIGRAND["sourceCF"][0], 2)) + " +/- "  + str(round(self.dataZIGRAND["sourceCF_stDev"][0], 2)))
            self.y0lineEditEst.setText(str(round(self.dataZIGRAND["sourceCF"][1], 2)) + " +/- " + str(round(self.dataZIGRAND["sourceCF_stDev"][1], 2)))
            self.A0lineEditEst.setText(str(round(self.dataZIGRAND['A0'][0], 2)) + " +/- " + str(round(self.dataZIGRAND['A0'][1], 2)))
        elif self.checkSPIRAL.isChecked():
            self.dataSPIRAL = combination(radiation, detector, spiral_flyover, spiral_locationCF, self.source)
            self.x0lineEditEst.setText(str(round(self.dataSPIRAL["sourceCF"][0], 2)) + " +/- "  + str(round(self.dataSPIRAL["sourceCF_stDev"][0], 2)))
            self.y0lineEditEst.setText(str(round(self.dataSPIRAL["sourceCF"][1], 2)) + " +/- " + str(round(self.dataSPIRAL["sourceCF_stDev"][1], 2)))
            self.A0lineEditEst.setText(str(round(self.dataSPIRAL['A0'][0], 2)) + " +/- " + str(round(self.dataSPIRAL['A0'][1], 2)))

    def plotGraph(self):
        if self.checkZIGZAG.isChecked():
            visualize(self.dataZIGZAG)
        elif self.checkZIGRAND.isChecked():
            visualize(self.dataZIGRAND)
        elif self.checkSPIRAL.isChecked():
            spiral_visualize(self.dataSPIRAL)
        
from radDialog import Ui_Dialog

class RadiationDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.getSettingsValues()

        # Set parameter class atributes
        self.Ab = self.settingVariables.value("Ab")
        self.Amin = self.settingVariables.value("Amin")
        self.Amax = self.settingVariables.value("Amax")
        self.F = self.settingVariables.value("F")

        self.radiation = {"A_b": float(self.Ab), "A_min": float(self.Amin), "A_max": float(self.Amax), "dose_factor": float(self.F)}

        # Set text value
        self.lineEditAb.setText(self.Ab)
        self.lineEditAmin.setText(self.Amin)
        self.lineEditAmax.setText(self.Amax)
        self.lineEditF.setText(self.F)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "radVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClearInput.clicked.connect(self.clearInput)

    def userInput_parameters(self):
        pass

    def clearInput(self):
        self.lineEditAb.setText("")
        self.lineEditAmin.setText("")
        self.lineEditAmax.setText("")
        self.lineEditF.setText("")

    def giveRadiation(self):
        return self.radiation

    def closeEvent(self, event): # After cosing the application the input information will remain saved
        # Set parameter values
        self.settingVariables.setValue("Ab", self.lineEditAb.text())
        self.settingVariables.setValue("Amin", self.lineEditAmin.text())
        self.settingVariables.setValue("Amax", self.lineEditAmax.text())
        self.settingVariables.setValue("F", self.lineEditF.text())

from detDialog import Ui_Dialog

class DetectorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.getSettingsValues()

        # Set parameter class atributes
        self.h = self.settingVariables.value("h")
        self.dt = self.settingVariables.value("dt")
        self.X = self.settingVariables.value("X"); self.Y = self.settingVariables.value("Y")
        self.grid = self.settingVariables.value("grid"); self.s_grid = self.settingVariables.value("s_grid")
        self.K = self.settingVariables.value("K")
        self.m = self.settingVariables.value("m")
        self.phi = self.settingVariables.value("phi")

        self.detector = {"h": float(self.h), "dt": float(self.dt), "width": float(self.X), "height": float(self.Y), "measured_points": 
                        int(self.m), "grid": [int(self.grid), int(self.grid)], "detector_constant": float(self.K),
                        "max_phi": float(self.phi), "spiral_grid": int(self.s_grid)}

        # Set text value
        self.lineEdit_h.setText(self.h)
        self.lineEdit_dt.setText(self.dt)
        self.lineEditX.setText(self.X); self.lineEditY.setText(self.Y)
        self.lineEditGrid.setText(self.grid); self.lineEditSgrid.setText(self.s_grid)
        self.lineEdit_K.setText(self.K)
        self.lineEdit_m.setText(self.m)
        self.lineEditPhi.setText(self.phi)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "detVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClearInput.clicked.connect(self.clearInput)

    #Enable/disable certian lineEdits depending on the method selected with the radio button (?)
    def ZigZag(self):
        self.lineEditGrid.setEnabled(True)
        self.lineEditSgrid.setEnabled(False)
        self.lineEditPhi.setEnabled(False)

    def ZigRand(self):
        self.lineEditGrid.setEnabled(False)
        self.lineEditSgrid.setEnabled(False)
        self.lineEditPhi.setEnabled(False)

    def Spiral(self):
        self.lineEditGrid.setEnabled(False)
        self.lineEditSgrid.setEnabled(True)
        self.lineEditPhi.setEnabled(True)

    def userInput_parameters(self):
        pass

    def clearInput(self):
        self.lineEdit_h.setText("")
        self.lineEdit_dt.setText("")
        self.lineEditX.setText("")
        self.lineEditY.setText("")
        self.lineEditGrid.setText("")
        self.lineEditSgrid.setText("")
        self.lineEdit_m.setText("")
        self.lineEditPhi.setText("")

    def giveDetector(self):
        return self.detector
    
    def closeEvent(self, event):
        self.settingVariables.setValue("h", self.lineEdit_h.text())
        self.settingVariables.setValue("dt", self.lineEdit_dt.text())
        self.settingVariables.setValue("X", self.lineEditX.text())
        self.settingVariables.setValue("Y", self.lineEditY.text())
        self.settingVariables.setValue("grid", self.lineEditGrid.text())
        self.settingVariables.setValue("s_grid", self.lineEditSgrid.text())
        self.settingVariables.setValue("K", self.lineEdit_K.text())
        self.settingVariables.setValue("m", self.lineEdit_m.text())
        self.settingVariables.setValue("phi", self.lineEditPhi.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())