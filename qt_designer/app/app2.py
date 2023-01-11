import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5.uic import loadUi

from MainWindow2 import Ui_MainWindow
import numpy as np

# # import the file to loop over anf+d change lines between code
# from fileLOOP import betweenLinesFill

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.h = 40
        self.x_max = 50; self.y_max = 50
        self.N_grid = 2

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.btn_Save.clicked.connect(self.parsInput)
        self.btn_plotGraph.clicked.connect(self.pressPlot)

    def about(self):
        QMessageBox.about(
            self,
            "Aplication for locatiing a radioactive source.",
            "<p>A sample app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )

    def parsInput(self):
        self.h = self.lineEdit_h.text()
        self.x_max = self.lineEdit_xmax.text(); self.y_max = self.lineEdit_ymax.text()
        self.N_grid = self.lineEdit_Ngrid.text()

    def pressPlot(self):
        D1 = int(self.dose1.text()); eD1 = int(self.doseErr1.text())
        D2 = int(self.dose2.text()); eD2 = int(self.doseErr2.text())
        D3 = int(self.dose3.text()); eD3 = int(self.doseErr3.text())
        D4 = int(self.dose4.text()); eD4 = int(self.doseErr4.text())

        HDs = np.array([[D2, D3],
                        [D1, D4]])
        dHDs = np.array([[eD2, eD3],
                        [eD1, eD4]])

        i_max, j_max = np.unravel_index(HDs.argmax(), HDs.shape)
        x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
        maxI_range = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_x/2, y_c + square_x/2)}

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())