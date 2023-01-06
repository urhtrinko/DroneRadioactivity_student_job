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
        self.btnCalculate.clicked.connect(self.calculate)

    def parameters(self):
        dialog = ParametersDialog(self)
        dialog.exec()

    def calculate(self):
        fieldRadiation, fieldDetector = ParametersDialog(self).userInput_parameters()
        print([fieldRadiation, fieldDetector])
        

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
        self.saveUserInput()

    def connectSignalsSlots(self):
        # the cancel button
        self.btn_Cancel.clicked.connect(self.close)
        # the save button
        self.btn_Save.clicked.connect(self.saveUserInput)
        self.btn_Save.clicked.connect(self.close)

    def saveUserInput(self):
        # saves the data the user inputed into the lineEdit - not operational yet
        # self.lineEdit_Ab.setText(str(1000))
        # self.lineEdit_h.setText(str(40))

        fieldRadiation, fieldDetector = self.userInput_parameters() # (?)
        A_b = fieldRadiation['A_b'] # (?)

        _translate = QtCore.QCoreApplication.translate # (?)
        self.lineEdit_Ab.setText(_translate("Dialog", self.lineEdit_Ab.text())) # (?)


    def userInput_parameters(self):
        # reads the data writtwn in the lineEdit and is called in the Window class to transfer the data into that class - works
        A_b = self.lineEdit_Ab.text()
        h = self.lineEdit_h.text()
        x_max = self.lineEdit_xmax.text(); y_max = self.lineEdit_ymax.text()
        N_grid = self.lineEdit_Ngrid.text()

        fieldRadiation = {"A_b": A_b}
        fieldDetector = {"h": h, "x_max": x_max, "y_max": y_max, "N_grid": N_grid}
        
        # print(fieldRadiation, fieldDetector)
        return fieldRadiation, fieldDetector


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())