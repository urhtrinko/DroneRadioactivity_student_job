import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings

# from PyQt5.uic import loadUi

from MainWindow import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    #Connect the signal to the appropriate buttons
    def connectSignalsSlots(self):
       self.btnRadiation.clicked.connect(self.radiation)
       self.btnDetector.clicked.connect(self.detector)
       self.checkZIGZAG.toggled.connect(self.radButZigZag)

    def radButZigZag(self):
        self.x0lineEditRand.setEnabled(False)
        
    #Open radiation/detector dialog window
    def radiation(self):
        dialog = RadiationDialog(self)
        dialog.exec()
    def detector(self):
        dialog = DetectorDialog(self)
        dialog.exec()

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
        self.m = self.settingVariables.value("m")
        self.phi = self.settingVariables.value("phi")

        # Set text value
        self.lineEdit_h.setText(self.h)
        self.lineEdit_dt.setText(self.dt)
        self.lineEditX.setText(self.X); self.lineEditY.setText(self.Y)
        self.lineEditGrid.setText(self.grid); self.lineEditSgrid.setText(self.s_grid)
        self.lineEdit_m.setText(self.m)
        self.lineEditPhi.setText(self.phi)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "detVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClearInput.clicked.connect(self.clearInput)

    def ZigZag(self):
        self.lineEditGrid.setEnabled(True)
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
    
    def closeEvent(self, event):
        self.settingVariables.setValue("h", self.lineEdit_h.text())
        self.settingVariables.setValue("dt", self.lineEdit_dt.text())
        self.settingVariables.setValue("X", self.lineEditX.text())
        self.settingVariables.setValue("Y", self.lineEditY.text())
        self.settingVariables.setValue("grid", self.lineEditGrid.text())
        self.settingVariables.setValue("s_grid", self.lineEditSgrid.text())
        self.settingVariables.setValue("m", self.lineEdit_m.text())
        self.settingVariables.setValue("phi", self.lineEditPhi.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())