import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QSlider, QLabel)
from PyQt5.QtCore import QSettings
from PyQt5 import QtGui

from MainWindow import Ui_MainWindow
from describtion import Ui_Dialog
from detectorCode import *

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectingSlots()
        self.getSettingsValues()

        # Set class atributes
        self.A_b = self.settingParameters.value("Ab"); self.A_max = self.settingParameters.value("Amax"); self.A_min = self.settingParameters.value("Amin")
        self.F = self.settingParameters.value("dose_factor")
        self.h = self.settingParameters.value("height"); self.dt = self.settingParameters.value("dt")
        self.X = self.settingParameters.value("X"); self.Y = self.settingParameters.value("Y")

        self.K = self.settingParameters.value("K")

        # Set text value
        self.lineEdit_Ab.setText(self.A_b); self.lineEdit_Amax.setText(self.A_max); self.lineEdit_Amin.setText(self.A_min)
        self.lineEdit_F.setText(self.F)
        self.lineEdit_h.setText(self.h); self.lineEdit_dt.setText(self.dt)
        self.lineEdit_X.setText(self.X); self.lineEdit_Y.setText(self.Y)

        # Factor-K slider)
        self.sliderForK.setMinimum(0)
        self.sliderForK.setMaximum(100)
        self.sliderForK.setSingleStep(1)
        self.sliderForK.setValue(int(round(float(self.K), 2)*100))
        self.sliderForK.setTickPosition(QSlider.TicksBelow)
        # self.sliderForK.setTickInterval(5)

        # Additional atributes
        self.radiation = {}
        self.detector = {}
        self.HD = 0; self.dHD = 0

    def connectingSlots(self):
        self.btn_Generate.clicked.connect(self.generateSource)
        self.btn_Generate.clicked.connect(self.setParameters)
        self.btn_Save.clicked.connect(self.setParameters)
        self.btnMeasure.clicked.connect(self.locationOfmeasuremnt)

        self.unitQuestionBtn.clicked.connect(self.unitsOfMeasurement)

        # Sliders
        self.sliderForK.valueChanged.connect(self.slide_it)

    def getSettingsValues(self):
        self.settingParameters = QSettings("My App", "Parameters")

    def description(self):
        dialog = Dialog(self)
        dialog.exec()

    def unitsOfMeasurement(self):
        info = QMessageBox()
        info.setWindowTitle("Information Message")
        r_HD = 0
        if (self.HD != 0) and (self.dHD != 0):
            r_HD = self.dHD/self.HD
        info.setText("<html><head/><body><p align=\"center\">Result is in mSv/s.</p></body></html>" + 
                    '\n' + "<html><head/><body><p align=\"center\">" + "Relative error of the measurement is" 
                    + "</p></body></html>" + str(round(r_HD*100, 2)) + "%.")
        info.setStandardButtons(QMessageBox.Ok)
        info = info.exec()

        if info == QMessageBox.Ok:
            pass

    def setParameters(self):
        List = [self.lineEdit_Ab.text(), self.lineEdit_Amax.text(),
                self.lineEdit_Amin.text(), self.lineEdit_F.text(),
                self.lineEdit_h.text(), self.lineEdit_dt.text(),
                self.lineEdit_X.text(), self.lineEdit_Y.text(),
                self.lineEdit_valueK.text()]

        if lineEditsFilled(List) == True:
            close = QMessageBox()
            close.setWindowTitle("Error Message")
            close.setText("<html><head/><body><p align=\"center\">Check if the lines contain only floats/intigers and are filled!</p></body></html>")
            close.setStandardButtons(QMessageBox.Ok)
            close = close.exec()

            if close == QMessageBox.Ok:
                pass
        else:
            self.A_b = self.lineEdit_Ab.text(); self.A_max = self.lineEdit_Amax.text(); self.A_min = self.lineEdit_Amin.text()
            self.F = self.lineEdit_F.text()
            self.h = self.lineEdit_h.text(); self.dt = self.lineEdit_dt.text()
            self.X = self.lineEdit_X.text(); self.Y = self.lineEdit_Y.text()
            self.K = self.sliderForK.value()*(1/100)

            self.radiation = {"A_min": float(self.A_min), "A_max": float(self.A_max), "A_b": float(self.A_b), "dose_factor": float(self.F)}
            self.detector = {"h": float(self.h), "dt": float(self.dt), "X": float(self.X), "Y": float(self.Y), "detector_constant": float(self.K)}

    def slide_it(self):
        value = round(self.sliderForK.value()*(1/100), 2)
        self.lineEdit_valueK.setText(str(value))

    def generateSource(self):
        self.source = randSource(self.radiation, self.detector)
        x0 = round(self.source[0], 2); y0 = round(self.source[1], 2); A0 = round(self.source[2])
        self.lineEdit_genSourceX.setText(str(x0))
        self.lineEdit_genSourceY.setText(str(y0))
        self.lineEdit_genSourceA0.setText(str(A0))

    def minusInStr(self, string):
        if string[0] == "-":
            return (-1) * float(string[1:])
        else:
            return float(string)

    def locationOfmeasuremnt(self):
        x = self.minusInStr(self.lineEdit_x.text()); y = self.minusInStr(self.lineEdit_y.text())
        if ((float(self.lineEdit_X.text())/2) < np.abs(x)) or ((float(self.lineEdit_Y.text())/2) < np.abs(y)):
            close = QMessageBox()
            close.setWindowTitle("Error Message")
            close.setText("<html><head/><body><p align=\"center\">Inputed measuring coordinates are out of bounds!</p></body></html>")
            close.setStandardButtons(QMessageBox.Ok)
            close = close.exec()

            if close == QMessageBox.Ok:
                pass
        else:
            self.HD, self.dHD = fieldMeasurement(self.radiation, self.detector, self.source, x, y, [])
            self.lineEdit_resultHD.setText(str(round(self.HD, 2)) + " +/- " + str(round(self.dHD, 2)))

    def closeEvent(self, event):
        self.settingParameters.setValue("Ab", self.lineEdit_Ab.text())
        self.settingParameters.setValue("Amax", self.lineEdit_Amax.text())
        self.settingParameters.setValue("Amin", self.lineEdit_Amin.text())
        self.settingParameters.setValue("dose_factor", self.lineEdit_F.text())
        self.settingParameters.setValue("height", self.lineEdit_h.text())
        self.settingParameters.setValue("dt", self.lineEdit_dt.text())
        self.settingParameters.setValue("X", self.lineEdit_X.text())
        self.settingParameters.setValue("Y", self.lineEdit_Y.text())

        self.settingParameters.setValue("K", round(self.sliderForK.value()*(1/100), 2))

class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()

    def connectSignalSlots(self):
        self.btnOK.clicked.connect(self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #open qss file
    File = open("stylesheets/Diplaytap/Diplaytap.qss", 'r')

    with File:
        qss = File.read()
        app.setStyleSheet(qss)

    win = Window()
    win.show()
    sys.exit(app.exec())


