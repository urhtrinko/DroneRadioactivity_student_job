# imports
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

# load ui file
Ui_MainWindow, QMainWindow = uic.loadUiType("Parameters.ui")

# use loaded ui file in the logic class
class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
    
    def useInput_parameters(self):
        A_b = self.lineEdit_Ab.text()
        h = self.lineEdit_h.text()
        x_max = self.lineEdit_xmax.text(); y_max = self.lineEdit_ymax.text()
        N_grid = self.lineEdit_Ngrid.text()

        fieldRadiation = {"A_b": A_b}
        fieldDetector = {"h": h, "x_max": x_max, "y_max": y_max, "N_grid": N_grid}

        print(fieldRadiation, fieldDetector)
        return {'fieldRadiation': fieldRadiation, 'fieldDetector': fieldDetector}

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


main()