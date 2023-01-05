import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5.uic import loadUi

from MainWindow import Ui_MainWindow
from dialog_parameters import Ui_Dialog

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.about)

        self.btnPAR.clicked.connect(self.parameters)

    def parameters(self):
        dialog = ParametersDialog(self)
        dialog.exec()

    def about(self):
        QMessageBox.about(
            self,
            "Aplication for locatiing a radioactive source.",
            # "<p>A sample app built with:</p>"
            # "<p>- PyQt</p>"
            # "<p>- Qt Designer</p>"
            # "<p>- Python</p>",
        )

class ParametersDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        # self.defaultPAR()

    def connectSignalsSlots(self):
        self.btn_Cancel.clicked.connect(self.close)
        self.btn_Save.clicked.connect(self.userInput_parameters)
        # self.btn_Save.clicked.connect(self.defaultPAR)
        self.btn_Save.clicked.connect(self.close)


    def userInput_parameters(self):
        A_b = self.lineEdit_Ab.text()
        h = self.lineEdit_h.text()
        x_max = self.lineEdit_xmax.text(); y_max = self.lineEdit_ymax.text()
        N_grid = self.lineEdit_Ngrid.text()

        fieldRadiation = {"A_b": A_b}
        fieldDetector = {"h": h, "x_max": x_max, "y_max": y_max, "N_grid": N_grid}

        print(fieldRadiation, fieldDetector)
        return fieldRadiation, fieldDetector

    # def defaultPAR(self):
    #     fieldRadiation, fieldDetector = self.userInput_parameters()

    #     A_b = fieldRadiation['A_b']
    #     h = fieldDetector['h']; x_max = fieldDetector['x_max']; y_max = fieldDetector['y_max']; N_grid = fieldDetector['N_grid']

    #     _translate = QtCore.QCoreApplication.translate
    #     self.lineEdit_Ab.setText(_translate("Dialog", str(A_b)))
    #     self.lineEdit_h.setText(_translate("Dialog", str(h)))
    #     self.lineEdit_xmax.setText(_translate("Dialog", str(x_max)))
    #     self.lineEdit_ymax.setText(_translate("Dialog", str(y_max)))
    #     self.lineEdit_Ngrid.setText(_translate("Dialog", str(N_grid)))


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())