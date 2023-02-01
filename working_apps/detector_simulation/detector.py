import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5.QtCore import QSettings

from MainWindow import Ui_MainWindow
from describtion import Ui_Dialog
from detectorCode import randSource
from detectorCode import fieldMeasurement

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectingSlots()
        self.getSettingsValues()

        # Set class atributes
        self.A_b = self.settingParameters.value("Ab"); self.A_max = self.settingParameters.value("Amax"); self.A_min = self.settingParameters.value("Amin")
        self.F = self.settingParameters.value("dose_factor")
        self.h = self.settingParameters.value("height"); self.dt = self.settingParameters.value("dt"); self.K = self.settingParameters.value("detector_constant")
        self.x_max = self.settingParameters.value("xmax"); self.y_max = self.settingParameters.value("ymax")

        # Set text value
        self.lineEdit_Ab.setText(self.A_b); self.lineEdit_Amax.setText(self.A_max); self.lineEdit_Amin.setText(self.A_min)
        self.lineEdit_F.setText(self.F)
        self.lineEdit_h.setText(self.h); self.lineEdit_dt.setText(self.dt); self.lineEdit_K.setText(self.K)
        self.lineEdit_xmax.setText(self.x_max); self.lineEdit_ymax.setText(self.y_max)

        # Additional atributes
        self.radiation = {}
        self.detector = {}

    def connectingSlots(self):
        self.btnSaveGenerate.clicked.connect(self.setParameters)
        self.btnSaveGenerate.clicked.connect(self.generateSource)
        self.btnMeasure.clicked.connect(self.locationOfmeasuremnt)
        self.btnDescribtion.clicked.connect(self.description)

    def getSettingsValues(self):
        self.settingParameters = QSettings("My App", "Parameters")

    def description(self):
        dialog = Dialog(self)
        dialog.exec()

    def setParameters(self):
        self.A_b = self.lineEdit_Ab.text(); self.A_max = self.lineEdit_Amax.text(); self.A_min = self.lineEdit_Amin.text()
        self.F = self.lineEdit_F.text()
        self.h = self.lineEdit_h.text(); self.dt = self.lineEdit_dt.text(); self.K = self.lineEdit_K.text()
        self.x_max = self.lineEdit_xmax.text(); self.y_max = self.lineEdit_ymax.text()

        self.radiation = {"A_min": float(self.A_min), "A_max": float(self.A_max), "A_b": float(self.A_b), "dose_factor": float(self.F)}
        self.detector = {"h": float(self.h), "dt": float(self.dt), "x_max": float(self.x_max), "y_max": float(self.y_max), "detector_constant": float(self.K)}

    def generateSource(self):
        self.source = randSource(self.radiation, self.detector)
        x0 = round(self.source[0], 2); y0 = round(self.source[1], 2); A0 = round(self.source[2])
        self.lineEdit_genSourceXY.setText("(" + str(x0) + " m, " + str(y0) + " m)")
        self.lineEdit_genSourceA0.setText(str(A0) + " Bq")

    def minusInStr(self, string):
        if string[0] == "-":
            return (-1) * float(string[1:])
        else:
            return float(string)

    def locationOfmeasuremnt(self):
        x = self.lineEdit_x.text(); y = self.lineEdit_y.text()
        HD, dHD = fieldMeasurement(self.radiation, self.detector, self.source, self.minusInStr(x), self.minusInStr(y), [])
        self.lineEdit_HD.setText(str(round(HD, 2)) + " +/- " + str(round(dHD, 2)))

    def closeEvent(self, event):
        self.settingParameters.setValue("Ab", self.lineEdit_Ab.text())
        self.settingParameters.setValue("Amax", self.lineEdit_Amax.text())
        self.settingParameters.setValue("Amin", self.lineEdit_Amin.text())
        self.settingParameters.setValue("dose_factor", self.lineEdit_F.text())
        self.settingParameters.setValue("height", self.lineEdit_h.text())
        self.settingParameters.setValue("dt", self.lineEdit_dt.text())
        self.settingParameters.setValue("detector_constant", self.lineEdit_K.text())
        self.settingParameters.setValue("xmax", self.lineEdit_xmax.text())
        self.settingParameters.setValue("ymax", self.lineEdit_ymax.text())

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


