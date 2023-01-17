import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)

from MainWindow import Ui_MainWindow
from describtion import Ui_Dialog
from detectorCode import randSource
from detectorCode import fieldMeasurement

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectingSlots()
        
        self.radiation = {}
        self.detector = {}
        self.source = []

    def connectingSlots(self):
        self.btnSaveGenerate.clicked.connect(self.setParameters)
        self.btnSaveGenerate.clicked.connect(self.generateSource)
        self.btnMeasure.clicked.connect(self.locationOfmeasuremnt)
        self.btnDescribtion.clicked.connect(self.description)

    def description(self):
        dialog = Dialog(self)
        dialog.exec()

    def setParameters(self):
        A_b = self.lineEdit_Ab.text(); A_max = self.lineEdit_Amax.text(); A_min = self.lineEdit_Amin.text()
        F = self.lineEdit_F.text()
        h = self.lineEdit_h.text(); dt = self.lineEdit_dt.text(); K = self.lineEdit_K.text()
        x_max = self.lineEdit_xmax.text(); y_max = self.lineEdit_ymax.text()

        self.radiation = {"A_min": float(A_min), "A_max": float(A_max), "A_b": float(A_b), "dose_factor": float(F)}
        self.detector = {"h": float(h), "dt": float(dt), "x_max": float(x_max), "y_max": float(y_max), "detector_constant": float(K)}

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

class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()

    def connectSignalSlots(self):
        self.btnOK.clicked.connect(self.close)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


