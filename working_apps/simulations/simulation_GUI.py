import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5.QtCore import QSettings
from PyQt5.uic import loadUi

from MainWindow import Ui_MainWindow

sys.path.insert(1, 'C:/Users/urhtr/OneDrive/Documents/Studij_fizike/Absolventsko_delo/DroneRadioactivity_student_job')

from main_code.subsidary import point_source, lineEditsFilled
from main_code.zigzag import flyover, visualize
from main_code.spiral import spiral_flyover, spiral_visualize
from main_code.combination import combination
from main_code.location import locationCF

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.getSettingsValues()
        
        # Set parameter class atributes
        self.x0Rand = self.settingVariables.value("x0Rand")
        self.y0Rand = self.settingVariables.value("y0Rand")
        self.A0Rand = self.settingVariables.value("A0Rand")
        self.r0Rand = self.settingVariables.value("r0Rand")

        # Set text value
        self.x0lineEditRand.setText(self.x0Rand)
        self.y0lineEditRand.setText(self.y0Rand)
        self.A0lineEditRand.setText(self.A0Rand)
        self.r0lineEditRand.setText(self.r0Rand)

        # Atributes for saving values
        self.dataZIGZAG = {}
        self.dataSPIRAL = {}
        self.source = [self.x0Rand, self.y0Rand, self.A0Rand, self.r0Rand]

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "MainWindowVariables")

    #Connect the signal to the appropriate buttons
    def connectSignalsSlots(self):
       self.btnRadiation.clicked.connect(self.radiation)
       self.btnDetector.clicked.connect(self.detector)
       self.btnEstSource.clicked.connect(self.estimateSource)
       self.btnRandSource.clicked.connect(self.generateSource)
       self.btnPlot.clicked.connect(self.plotGraph)
       self.btnClearInput.clicked.connect(self.clearInput)
       self.btnUserGenSource.clicked.connect(self.userGenSource)

       self.actionExit.triggered.connect(self.close)
       self.actionAbout.triggered.connect(self.mainDes)

       self.infoZigZag.clicked.connect(self.ZigZagDes)
       self.infoSpiral.clicked.connect(self.SpiralDes)
        
    #Open the dialog windows
    def mainDes(self):
        dialog = MainDescribtion(self)
        dialog.exec()
    def ZigZagDes(self):
        dialog = ZigZagDescribtion(self)
        dialog.exec()
    def SpiralDes(self):
        dialog = SpiralDescribtion(self)
        dialog.exec()
    def radiation(self):
        dialog = RadiationDialog(self)
        dialog.exec()
    def detector(self):
        dialog = DetectorDialog(self)
        dialog.exec()

    def EnableDisable(self):
        if self.checkZIGZAG.isChecked():
            return {"ZigZag": True, "Spiral": False}
        elif self.checkSPIRAL.isChecked():
            return {"ZigZag": False, "Spiral": True}
        else:
            return {"ZigZag": False, "Spiral": False}

    def userGenSource(self):
        List = [self.x0lineEditRand.text(), self.y0lineEditRand.text(), self.A0lineEditRand.text(), self.r0lineEditRand.text()]
        print(List)
        if lineEditsFilled(List) == False:
            self.source = [float(List[0]), float(List[1]), float(List[2]), float(List[3])]

    def generateSource(self):
        radiation = RadiationDialog(self).giveRadiation()
        detector = DetectorDialog(self).giveDetector()
        Amax = radiation['A_max']; Amin = radiation['A_min']
        r0max = radiation['r0_max']; r0min = radiation['r0_min']
        xmax = detector['X']; ymax = detector['Y']
        self.source = point_source(xmax/2, ymax/2, Amin, Amax, r0max, r0min)
        self.x0lineEditRand.setText((str(round(self.source[0], 2)))); self.y0lineEditRand.setText(str(round(self.source[1], 2)))
        self.A0lineEditRand.setText(str(round(self.source[2], 2))); self.r0lineEditRand.setText(str(round(self.source[3], 2)))

    def estimateSource(self):
        radiation = RadiationDialog(self).giveRadiation()
        detector = DetectorDialog(self).giveDetector()
        if self.checkZIGZAG.isChecked():
            self.dataZIGZAG = combination(radiation, detector, flyover, locationCF, self.source)
            self.x0lineEditEst.setText(str(round(self.dataZIGZAG["sourceCF"][0], 2)) + " +/- "  + str(round(self.dataZIGZAG["sourceCF_stDev"][0], 2)))
            self.y0lineEditEst.setText(str(round(self.dataZIGZAG["sourceCF"][1], 2)) + " +/- " + str(round(self.dataZIGZAG["sourceCF_stDev"][1], 2)))
        elif self.checkSPIRAL.isChecked():
            self.dataSPIRAL = combination(radiation, detector, spiral_flyover, locationCF, self.source)
            self.x0lineEditEst.setText(str(round(self.dataSPIRAL["sourceCF"][0], 2)) + " +/- "  + str(round(self.dataSPIRAL["sourceCF_stDev"][0], 2)))
            self.y0lineEditEst.setText(str(round(self.dataSPIRAL["sourceCF"][1], 2)) + " +/- " + str(round(self.dataSPIRAL["sourceCF_stDev"][1], 2)))

    def plotGraph(self):
        if self.checkZIGZAG.isChecked():
            visualize(self.dataZIGZAG)
        elif self.checkSPIRAL.isChecked():
            spiral_visualize(self.dataSPIRAL)

    def clearInput(self):
        self.x0lineEditRand.setText(""); self.y0lineEditRand.setText(""); self.A0lineEditRand.setText(""); self.r0lineEditRand.setText("")
        self.x0lineEditEst.setText(""); self.y0lineEditEst.setText("")

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
        self.settingVariables.setValue("x0Rand", self.x0lineEditRand.text())
        self.settingVariables.setValue("y0Rand", self.y0lineEditRand.text())
        self.settingVariables.setValue("A0Rand", self.A0lineEditRand.text())
        self.settingVariables.setValue("r0Rand", self.r0lineEditRand.text())
        
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
        self.r0min = self.settingVariables.value("r0min")
        self.r0max = self.settingVariables.value("r0max")
        self.F = self.settingVariables.value("F")

        self.radiation = {"A_b": float(self.Ab), "A_min": float(self.Amin), "A_max": float(self.Amax), 'r0_min': float(self.r0min),
                          'r0_max': float(self.r0max), "dose_factor": float(self.F)}

        # Set text value
        self.lineEditAb.setText(self.Ab)
        self.lineEditAmin.setText(self.Amin)
        self.lineEditAmax.setText(self.Amax)
        self.lineEdit_r0min.setText(self.r0min)
        self.lineEdit_r0max.setText(self.r0max)
        self.lineEditF.setText(self.F)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "radVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClearInput.clicked.connect(self.clearInput)

    def clearInput(self):
        self.lineEditAb.setText("")
        self.lineEditAmin.setText("")
        self.lineEditAmax.setText("")
        self.lineEdit_r0min.setText("")
        self.lineEdit_r0max.setText("")
        self.lineEditF.setText("")

    def giveRadiation(self):
        return self.radiation

    def closeEvent(self, event): # After cosing the application the input information will remain saved
        List = [self.lineEditAb.text(), self.lineEditAmin.text(), self.lineEditAmax.text(), self.lineEdit_r0min.text(),
                self.lineEdit_r0max.text(), self.lineEditF.text()]
        if lineEditsFilled(List) == True:
            close = QMessageBox()
            close.setWindowTitle("Error Message")
            close.setText("<html><head/><body><p align=\"center\">Check if the lines contain only floats/intigers and are filled!</p></body></html>")
            close.setStandardButtons(QMessageBox.Ok)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.ignore()

        # Set parameter values
        self.settingVariables.setValue("Ab", self.lineEditAb.text())
        self.settingVariables.setValue("Amin", self.lineEditAmin.text())
        self.settingVariables.setValue("Amax", self.lineEditAmax.text())
        self.settingVariables.setValue("r0min", self.lineEdit_r0min.text())
        self.settingVariables.setValue("r0max", self.lineEdit_r0max.text())
        self.settingVariables.setValue("F", self.lineEditF.text())

from detDialog import Ui_Dialog

class DetectorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.getSettingsValues()

        self.boolDict = Window(self).EnableDisable()

        # Set parameter class atributes
        self.h = self.settingVariables.value("h")
        self.dt = self.settingVariables.value("dt")
        self.X = self.settingVariables.value("X"); self.Y = self.settingVariables.value("Y")
        self.grid = self.settingVariables.value("grid")
        self.K = self.settingVariables.value("K")
        self.phi = self.settingVariables.value("phi")

        self.detector = {"h": float(self.h), "dt": float(self.dt), "X": float(self.X), "Y": float(self.Y),
                        "grid": [int(self.grid), int(self.grid)], "detector_constant": float(self.K), "max_phi": float(self.phi)}

        # FOR EMERGANCIES, Whene you accidentaly save a line edit without anything written in it -> problem occures when converting to float
        # self.detector = {"h": self.h, "dt": self.dt, "X": self.X, "Y": self.Y, "measured_points": self.m, 
        #                 "grid": [self.grid, self.grid], "detector_constant": self.K, "max_phi": self.phi, "spiral_grid": self.s_grid}

        # Set text value
        self.lineEdit_h.setText(self.h)
        self.lineEdit_dt.setText(self.dt)
        self.lineEditX.setText(self.X); self.lineEditY.setText(self.Y)
        self.lineEditGrid.setText(self.grid)
        self.lineEdit_K.setText(self.K)
        self.lineEditPhi.setText(self.phi)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "detVariables")

    def connectSignalsSlots(self):
        self.btnSave.clicked.connect(self.close)
        self.btnClearInput.clicked.connect(self.clearInput)

    def clearInput(self):
        self.lineEdit_h.setText("")
        self.lineEdit_dt.setText("")
        self.lineEditX.setText("")
        self.lineEditY.setText("")
        self.lineEditGrid.setText("")
        self.lineEdit_K.setText("")
        self.lineEditPhi.setText("")

    def giveDetector(self):
        return self.detector
    
    def printSth(self):
        print(self.boolDict)
    
    def closeEvent(self, event):
        List = [self.lineEdit_h.text(), self.lineEdit_dt.text(), self.lineEditX.text(), 
                self.lineEditY.text(), self.lineEditGrid.text(), self.lineEdit_K.text(),
                self.lineEditPhi.text()]
        if lineEditsFilled(List) == True:
            close = QMessageBox()
            close.setWindowTitle("Error Message")
            close.setText("<html><head/><body><p align=\"center\">Check if the lines contain only floats/intigers and are filled!</p></body></html>")
            close.setStandardButtons(QMessageBox.Ok)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.ignore()

        self.settingVariables.setValue("h", self.lineEdit_h.text())
        self.settingVariables.setValue("dt", self.lineEdit_dt.text())
        self.settingVariables.setValue("X", self.lineEditX.text())
        self.settingVariables.setValue("Y", self.lineEditY.text())
        self.settingVariables.setValue("grid", self.lineEditGrid.text())
        self.settingVariables.setValue("K", self.lineEdit_K.text())
        self.settingVariables.setValue("phi", self.lineEditPhi.text())

class MainDescribtion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("mainDescribtion.ui", self)

class ZigZagDescribtion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ZigZagDescribtion.ui", self)

class SpiralDescribtion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("SpiralDescribtion.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())