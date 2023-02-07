import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QSettings
from PyQt5.uic import loadUi

from MainWindow import Ui_MainWindow

from python_methods.subsidary import *

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.btnNext.setShortcut("Return")
        self.btnBack.setShortcut("Shift+Return")

        self.connectSignalsSlots()
        self.getSettingsValues()

        # Set text value
        self.i = -1 # a variable - it allows the user to iterate through the measurements
        self.parameters = {}
        self.List = []; self.HDs = np.zeros((1, 2)); self.dHDs = np.zeros((1, 2))
        self.FC = {}

        self.progressBarHD.setValue(0)
        
        # Set parameter class atributes
        # (???????????????????)
        # self.i = self.settingVariables.value("i")
        # self.parameters = self.settingVariables.value("parameters")
        # self.List = self.settingVariables.value("list")
        # self.HDs = self.settingVariables.value("HDs")
        # self.dHDs = self.settingVariables.value("dHDs")
        # ???

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "MainWindowVariables")

    #Connect the signal to the appropriate buttons
    def connectSignalsSlots(self):
       self.btnEditPars.clicked.connect(self.Parameters)
       self.btnNext.clicked.connect(self.Next)
       self.btnBack.clicked.connect(self.Back)
       self.btnFindSource.clicked.connect(self.estimateSource)
        
    #Open the dialog windows
    def Parameters(self):
        dialog = ParametersDialog(self)
        dialog.exec()

    def clearInput(self):
        pass

    def Message(self, title, message):
        close = QMessageBox()
        close.setWindowTitle(title)
        close.setText("<html><head/><body><p align=\"center\">" + message + "</p></body></html>")
        close.setStandardButtons(QMessageBox.Ok)
        close = close.exec()

        if close == QMessageBox.Ok:
            pass

    def Next(self):
        if self.i == -1:
            self.parameters = ParametersDialog(self).giveParameters()
            Dictionary = makeArrays(self.parameters)
            self.List = Dictionary['list']; self.HDs = Dictionary['HDs']; self.dHDs = Dictionary['dHDs']
            self.i = 0
            x, y = self.List[self.i]['xy']
            self.lineEdit_X.setText("x = " + str(round(x, 2)) + " m"); self.lineEdit_Y.setText("y = " + str(round(y, 2)) + " m")
            i, j = self.List[self.i]['ij']
            self.lineEdit_HD.setText(str(self.HDs[i, j])); self.lineEdit_dHD.setText(str(self.dHDs[i, j]))
        else:
            i, j = self.List[self.i]['ij']
            self.HDs[i, j] = float(self.lineEdit_HD.text()); self.dHDs[i, j] = float(self.lineEdit_dHD.text())
            self.progressBarHD.setValue(count0InArray(self.HDs))
            if self.parameters['m'] - 1 <= self.i: 
                self.Message("Border Message", "You have reached the end, mate.")
            else:
                self.i += 1
                x, y = self.List[self.i]['xy']
                self.lineEdit_X.setText("x = " + str(round(x, 2)) + " m"); self.lineEdit_Y.setText("y = " + str(round(y, 2)) + " m")
                i, j = self.List[self.i]['ij']
                self.lineEdit_HD.setText(str(self.HDs[i, j])); self.lineEdit_dHD.setText(str(self.dHDs[i, j]))

    def Back(self):
        if self.i < 0:
            self.Message("Border Message", "You have reached the beginning, mate.")
        else:
            i, j = self.List[self.i]['ij']
            self.HDs[i, j] = float(self.lineEdit_HD.text()); self.dHDs[i, j] = float(self.lineEdit_dHD.text())
            self.progressBarHD.setValue(count0InArray(self.HDs))
            if self.i - 1 < 0:
                self.Message("Border Message", "You have reached the beginning, mate.")
            else:
                self.i = self.i - 1
                x, y = self.List[self.i]['xy']
                self.lineEdit_X.setText("x = " + str(round(x, 2)) + " m"); self.lineEdit_Y.setText("y = " + str(round(y, 2)) + " m")
                i, j = self.List[self.i]['ij']
                self.lineEdit_HD.setText(str(self.HDs[i, j])); self.lineEdit_dHD.setText(str(self.dHDs[i, j]))

    def resetIndex(self):
        self.i = -1
        self.lineEdit_X.setText("x = ? m"); self.lineEdit_Y.setText("y = ? m")

    def estimateSource(self):
        measurement = {"m_dose": self.HDs, "dm_dose": self.dHDs}
        detector = self.parameters

        self.FC = field_combination(detector, measurement)
        self.lineEditX0.setText(str(round(self.FC['sourceCF'][0], 2)) + " +/- " + str(round(self.FC['sourceCF_stDev'][0], 2)))
        self.lineEditY0.setText(str(round(self.FC['sourceCF'][1], 2)) + " +/- " + str(round(self.FC['sourceCF_stDev'][1], 2)))
        self.lineEditA0.setText(str(round(self.FC['sourceCF'][2], 2)) + " +/- " + str(round(self.FC['sourceCF_stDev'][2], 2)))

    def plotGraph(self):
        visualize(self.FC)

    def closeEvent(self, event): # After cosing the application the input information will remain saved
        close = QMessageBox()
        close.setWindowTitle("Exit Message")
        close.setText("<html><head/><body><p align=\"center\">Are you sure you want to close?</p></body></html>")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

        # Set parameter values
        #?
        # self.settingVariables.setValue("i", 0)
        # self.settingVariables.setValue("parameters", self.parameters)
        # self.settingVariables.setValue("list", self.List)
        # self.settingVariables.setValue("HDs", self.HDs)
        # self.settingVariables.setValue("dHDs", self.dHDs)
        #?

from DialogPars import Ui_Dialog

class ParametersDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.getSettingsValues()

        # Set parameter class atributes
        self.h = self.settingVariables.value("h")
        self.X = self.settingVariables.value("X"); self.Y = self.settingVariables.value("Y")
        self.m = self.settingVariables.value("m")
        
        # Set text value
        self.lineEdit_h.setText(self.h)
        self.lineEdit_X.setText(self.X); self.lineEdit_Y.setText(self.Y)
        self.lineEdit_m.setText(self.m)
        
        # Setting atributes
        self.parameters = {"h": float(self.h), "X": float(self.X), "Y": float(self.Y), "m": float(self.m)}

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "radVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClear.clicked.connect(self.clearInput)

    def clearInput(self):
        self.lineEdit_h.setText("")
        self.lineEdit_X.setText(""); self.lineEdit_Y.setText("")
        self.lineEdit_m.setText("")

    def giveParameters(self):
        return self.parameters

    def closeEvent(self, event): # After cosing the application the input information will remain saved
        List = [self.lineEdit_h.text(), self.lineEdit_X.text(), self.lineEdit_Y.text(),
                self.lineEdit_m.text()]
        if lineEditsFilled(List) == True:
            close = QMessageBox()
            close.setWindowTitle("Error Message")
            close.setText("<html><head/><body><p align=\"center\">Check if the lines contain only floats/integers and are filled!</p></body></html>")
            close.setStandardButtons(QMessageBox.Ok)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.ignore()

        # Set parameter values
        self.settingVariables.setValue("h", self.lineEdit_h.text())
        self.settingVariables.setValue("X", self.lineEdit_X.text()); self.settingVariables.setValue("Y", self.lineEdit_Y.text())
        self.settingVariables.setValue("m", self.lineEdit_m.text())

# class MainDescribtion(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         loadUi("mainDescribtion.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # #open qss file
    # File = open("stylesheets/Diplaytap/Diplaytap.qss", 'r')

    # with File:
    #     qss = File.read()
    #     app.setStyleSheet(qss)

    win = Window()
    win.show()
    sys.exit(app.exec())