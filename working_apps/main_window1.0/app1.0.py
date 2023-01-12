import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5.uic import loadUi

from MainWindow2 import Ui_MainWindow
import numpy as np
from main_code import field_combination
from main_code import visualize

# # import the file to loop over anf+d change lines between code
# from fileLOOP import betweenLinesFill

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.data = {}
        self.h = 40
        self.x_max = 50; self.y_max = 50
        self.N_grid = 2

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

        self.btn_Save.clicked.connect(self.parsInput)
        self.btn_Save2.clicked.connect(self.getData)
        self.btn_plotGraph.clicked.connect(self.pressPlot)
        self.btn_Source.clicked.connect(self.pressSource)

    def about(self):
        QMessageBox.about(
            self,
            "About the app",
            "The user inputs parameters of the detector and clicks SAVE."
            "The user inpusts the dose (left) and its error (right)"
            "The second SAVE runs the code that estimates the source location must be pressed before PLOT or SOURCE."
            "The user clicks PLOT to plot a colored grid of the input."
            "SOURCE displays the estimated x/y position of the point source.",
        )

    def parsInput(self):
        self.h = float(self.lineEdit_h.text())
        self.x_max = float(self.lineEdit_xmax.text()); self.y_max = float(self.lineEdit_ymax.text())
        self.N_grid = float(self.lineEdit_Ngrid.text())

    def getData(self):
        D00 = self.dose00.text(); eD00 = self.doseErr00.text()
        D01 = self.dose01.text(); eD01 = self.doseErr01.text()
        D10 = self.dose10.text(); eD10 = self.doseErr10.text()
        D11 = self.dose11.text(); eD11 = self.doseErr11.text()

        # Save what is written:
        self.dose00.setText(D00); self.doseErr00.setText(D00)


        HDs = np.array([[float(D00), float(D01)],
                        [float(D10), float(D11)]])
        dHDs = np.array([[float(eD00), float(eD01)],
                        [float(eD10), float(eD11)]])
        grid_x = np.array([[-25.,  25.],
                            [-25.,  25.]])
        grid_y = np.array([[ 25.,  25.],
                            [-25., -25.]])

        square_x = 2*self.x_max/self.N_grid
        square_y = 2*self.y_max/self.N_grid

        i_max, j_max = np.unravel_index(HDs.argmax(), HDs.shape)
        x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
        maxI_range = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_x/2, y_c + square_x/2)}


        measurement = {"m_dose": HDs, "dm_dose": dHDs, "source": [], "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": np.zeros((2, 2)), "grid_y_noise": np.zeros((2, 2)), "hotspot": maxI_range, "square_x": square_x, "square_y": square_y, "x_max": float(self.x_max), "y_max": float(self.y_max)}
        detector = {"h": self.h, "x_max": self.x_max, "y_max": self.y_max, "N_grid": self.N_grid}
        self.data = field_combination(detector, measurement, [])

    def pressPlot(self):
        visualize(self.data)

    def pressSource(self):
        u = self.data["sourceCF"][0]; du = self.data["sourceCF_stDev"][0]
        v = self.data["sourceCF"][1]; dv = self.data["sourceCF_stDev"][1]
        self.lineEdit_x0.setText(str(round(u, 2)) + " +/- " + str(round(du, 2))) 
        self.lineEdit_y0.setText(str(round(v, 2)) + " +/- " + str(round(dv, 2)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

    