import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5.uic import loadUi

from MainWindow import Ui_MainWindow
from dialog_parameters import Ui_Dialog

# import the file to loop over anf+d change lines between code
from fileLOOP import betweenLinesFill

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.about)

        self.btnPAR.clicked.connect(self.parameters) # Opens the parameters dialog for user input
        self.btnCalculate.clicked.connect(self.calculate) # Calculates the source position - NOT operational

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
        self.retranslateUi(self)
        # self.saveUserInput()

    def connectSignalsSlots(self):
        # the cancel button
        self.btn_Cancel.clicked.connect(self.close)
        # the save button
        self.btn_Save.clicked.connect(self.saveUserInput)
        self.btn_Save.clicked.connect(self.close)

    def saveUserInput(self):
        # saves the data the user inputed into the lineEdit - NOT operational yet
        # self.lineEdit_Ab.setText(str(1000))
        # self.lineEdit_h.setText(str(40))

        fieldRadiation, fieldDetector = self.userInput_parameters() # (?)
        A_b = fieldRadiation['A_b'] # (?)
        x_max = fieldDetector['x_max']; y_max = fieldDetector['y_max']
        N_grid = fieldDetector['N_grid']

        print(str(A_b))

        replaceLines = ("self.lineEdit_Ab.setText(_translate(" + "\"Dialog\"," + "\"" + str(A_b) + "\"" + "))" + "\n"
                        "self.lineEdit_xmax.setText(_translate(" + "\"Dialog\"," + "\"" + str(x_max) + "\"" + "))" + "\n"
                        "self.lineEdit_ymax.setText(_translate(" + "\"Dialog\"," + "\"" + str(y_max) + "\"" + "))" + "\n"
                        "self.lineEdit_Ngrid.setText(_translate(" + "\"Dialog\"," + "\"" + str(N_grid) + "\"" + "))" + "\n"
)  

        betweenLinesFill("dialog_parameters.py", "Begin user input", "End user input", replaceLines)


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