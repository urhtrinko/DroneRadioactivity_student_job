# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Parameters.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(609, 444)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_RAD = QtWidgets.QLabel(self.centralwidget)
        self.label_RAD.setGeometry(QtCore.QRect(20, 20, 100, 30))
        self.label_RAD.setObjectName("label_RAD")
        self.label_DET = QtWidgets.QLabel(self.centralwidget)
        self.label_DET.setGeometry(QtCore.QRect(20, 120, 100, 30))
        self.label_DET.setObjectName("label_DET")
        self.label_Ab = QtWidgets.QLabel(self.centralwidget)
        self.label_Ab.setGeometry(QtCore.QRect(50, 70, 70, 20))
        self.label_Ab.setObjectName("label_Ab")
        self.lineEdit_Ab = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Ab.setGeometry(QtCore.QRect(140, 70, 113, 25))
        self.lineEdit_Ab.setObjectName("lineEdit_Ab")
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setGeometry(QtCore.QRect(50, 170, 70, 20))
        self.label_h.setObjectName("label_h")
        self.lineEdit_h = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_h.setGeometry(QtCore.QRect(140, 170, 113, 25))
        self.lineEdit_h.setObjectName("lineEdit_h")
        self.label_xmax = QtWidgets.QLabel(self.centralwidget)
        self.label_xmax.setGeometry(QtCore.QRect(50, 220, 83, 20))
        self.label_xmax.setObjectName("label_xmax")
        self.label_ymax = QtWidgets.QLabel(self.centralwidget)
        self.label_ymax.setGeometry(QtCore.QRect(300, 220, 83, 20))
        self.label_ymax.setObjectName("label_ymax")
        self.lineEdit_xmax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_xmax.setGeometry(QtCore.QRect(140, 220, 113, 25))
        self.lineEdit_xmax.setObjectName("lineEdit_xmax")
        self.lineEdit_ymax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ymax.setGeometry(QtCore.QRect(390, 220, 113, 25))
        self.lineEdit_ymax.setObjectName("lineEdit_ymax")
        self.label_Ngrid = QtWidgets.QLabel(self.centralwidget)
        self.label_Ngrid.setGeometry(QtCore.QRect(50, 270, 83, 20))
        self.label_Ngrid.setObjectName("label_Ngrid")
        self.lineEdit_Ngrid = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Ngrid.setGeometry(QtCore.QRect(140, 270, 113, 25))
        self.lineEdit_Ngrid.setObjectName("lineEdit_Ngrid")
        self.but_Save = QtWidgets.QPushButton(self.centralwidget)
        self.but_Save.setGeometry(QtCore.QRect(470, 340, 112, 34))
        self.but_Save.setObjectName("but_Save")
        self.but_Cancel = QtWidgets.QPushButton(self.centralwidget)
        self.but_Cancel.setGeometry(QtCore.QRect(340, 340, 112, 34))
        self.but_Cancel.setObjectName("but_Cancel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 609, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_RAD.setText(_translate("MainWindow", "RADIATION"))
        self.label_DET.setText(_translate("MainWindow", "DETECTOR"))
        self.label_Ab.setText(_translate("MainWindow", "A_b [Bq]:"))
        self.label_h.setText(_translate("MainWindow", "h [m]:"))
        self.label_xmax.setText(_translate("MainWindow", "x_max [m]:"))
        self.label_ymax.setText(_translate("MainWindow", "y_max [m]:"))
        self.label_Ngrid.setText(_translate("MainWindow", "N_grid:"))
        self.but_Save.setText(_translate("MainWindow", "Save"))
        self.but_Cancel.setText(_translate("MainWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
