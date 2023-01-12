import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)

from MainWindow import Ui_MainWindow
from detectorCode import randSource
from detectorCode import fieldMeasurement

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectingSlots()
        
        # self.Ab = 0; self.Amax = 0; self.Amin = 0; self.F = 0
        # self.h = 0; self.dt = 0; self.K = 0
        self.radiation = {}
        self.detector = {}
        self.source = []

    def connectingSlots(self):
        self.btnSaveGenerate.clicked.connect(self.setParameters)
        self.btnSaveGenerate.clicked.connect(self.generateSource)

    def setParameters(self):
        A_b = self.lineEdit_Ab.text(); A_max = self.lineEdit_Amax.text(); A_min = self.lineEdit_Amin.text()
        F = self.lineEdit_F.text()
        h = self.lineEdit_h.text(); dt = self.lineEdit_dt.text(); K = self.lineEdit_K.text()

        self.radiation = {"A_min": A_min, "A_max": A_max, "A_b": A_b, "dose_factor": F}
        self.detector = {"h": h, "dt": dt, "detector_constant": K}

    def generateSource(self):
        self.source = randSource(self.radiation, self.detector)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


