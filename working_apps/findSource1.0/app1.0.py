import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings

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
        self.getSettingsValues()
        self.data = {}
        self.xs = {}
        self.ys = {}

        # Set parameter class atributes
        self.h = self.settingVariables.value("height")
        self.x_max = self.settingVariables.value("xmax"); self.y_max = self.settingVariables.value("ymax")
        self.N_grid = 2
        # Set doses and error of the doses atributes
        self.D00 = self.settingVariables.value("dose00"); self.eD00 = self.settingVariables.value("doseErr00")
        self.D01 = self.settingVariables.value("dose01"); self.eD01 = self.settingVariables.value("doseErr01")
        self.D10 = self.settingVariables.value("dose10"); self.eD10 = self.settingVariables.value("doseErr10")
        self.D11 = self.settingVariables.value("dose11"); self.eD11 = self.settingVariables.value("doseErr11")

        # Set pararameter text
        self.lineEdit_h.setText(self.h)
        self.lineEdit_xmax.setText(self.x_max); self.lineEdit_ymax.setText(self.y_max)
        # Set doses and error of the doses text
        self.dose00.setText(self.D00); self.doseErr00.setText(self.eD00)
        self.dose01.setText(self.D01); self.doseErr01.setText(self.eD01)
        self.dose10.setText(self.D10); self.doseErr10.setText(self.eD10)
        self.dose11.setText(self.D11); self.doseErr11.setText(self.eD11)


    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

        self.btn_Save.clicked.connect(self.parsInput)
        self.btn_Save2.clicked.connect(self.getData)
        self.btn_plotGraph.clicked.connect(self.pressPlot)
        self.btn_Source.clicked.connect(self.pressSource)
        self.btn_Clear.clicked.connect(self.clearInput)

    def getSettingsValues(self):
        self.settingVariables = QSettings("My App", "Variables")

    def about(self):
        QMessageBox.about(
            self,
            "About the app",
            "The user inputs parameters of the detector and clicks SAVE.\n"
            "The user inpusts the dose (left) and its error (right).\n"
            "The second SAVE runs the code that estimates the source location must be pressed before PLOT or SOURCE.\n"
            "The user clicks PLOT to plot a colored grid of the input.\n"
            "SOURCE displays the estimated x/y position of the point source.\n"
            "The button CLEAR empties all line edits under DOSES AND ERRORS."
        )

    def parsInput(self):
        self.h = float(self.lineEdit_h.text())
        self.x_max = float(self.lineEdit_xmax.text()); self.y_max = float(self.lineEdit_ymax.text())
        self.N_grid = float(self.lineEdit_Ngrid.text())

        _translate = QtCore.QCoreApplication.translate
        self.xs = np.linspace(-self.x_max + self.x_max/self.N_grid, self.x_max - self.x_max/self.N_grid, int(self.N_grid))
        self.ys = np.linspace(-self.y_max + self.y_max/self.N_grid, self.y_max - self.y_max/self.N_grid, int(self.N_grid))
        x1 = str(round(self.xs[0], 2)); x2 = str(round(self.xs[1], 2))
        y2 = str(round(self.ys[0], 2)); y1 = str(round(self.ys[1], 2))
        self.label_x1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">" + x1 + "</p></body></html>"))
        self.label_x2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">" + x2 + "</p></body></html>"))
        self.label_y1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">" + y1 + "</p></body></html>"))
        self.label_y2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">" + y2 + "</p></body></html>"))

    def getData(self):
        HDs = np.array([[float(self.D00), float(self.D01)],
                        [float(self.D10), float(self.D11)]])
        dHDs = np.array([[float(self.eD00), float(self.eD01)],
                        [float(self.eD10), float(self.eD11)]])
        grid_x = np.array([[self.xs[0], self.xs[1]],
                            [self.xs[0],self.xs[1]]])
        grid_y = np.array([[self.ys[1],  self.ys[1]],
                            [self.ys[0], self.ys[0]]])

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

    def clearInput(self):
        self.dose00.setText(""); self.doseErr00.setText("")
        self.dose01.setText(""); self.doseErr01.setText("")
        self.dose10.setText(""); self.doseErr10.setText("")
        self.dose11.setText(""); self.doseErr11.setText("")
        
        self.lineEdit_x0.setText(""); self.lineEdit_y0.setText("")

    def closeEvent(self, event): # After cosing the application the input information will remain saved
        # Set parameter values
        self.settingVariables.setValue("height", self.lineEdit_h.text())
        self.settingVariables.setValue("xmax", self.lineEdit_xmax.text()); self.settingVariables.setValue("ymax", self.lineEdit_ymax.text())

        # Set doses and errors values
        self.settingVariables.setValue("dose00", self.dose00.text()); self.settingVariables.setValue("doseErr00", self.doseErr00.text())
        self.settingVariables.setValue("dose01", self.dose01.text()); self.settingVariables.setValue("doseErr01", self.doseErr01.text())
        self.settingVariables.setValue("dose10", self.dose10.text()); self.settingVariables.setValue("doseErr10", self.doseErr10.text())
        self.settingVariables.setValue("dose11", self.dose11.text()); self.settingVariables.setValue("doseErr11", self.doseErr11.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

    