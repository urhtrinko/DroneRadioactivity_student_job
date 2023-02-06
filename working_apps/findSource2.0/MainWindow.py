# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 407)
        MainWindow.setMinimumSize(QtCore.QSize(789, 407))
        MainWindow.setMaximumSize(QtCore.QSize(789, 407))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_HD = QtWidgets.QLabel(self.centralwidget)
        self.label_HD.setObjectName("label_HD")
        self.gridLayout.addWidget(self.label_HD, 1, 1, 1, 1)
        self.lineEdit_HD = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_HD.setObjectName("lineEdit_HD")
        self.gridLayout.addWidget(self.lineEdit_HD, 1, 2, 1, 1)
        self.lineEdit_dHD = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dHD.setObjectName("lineEdit_dHD")
        self.gridLayout.addWidget(self.lineEdit_dHD, 1, 8, 1, 1)
        self.label_dHD = QtWidgets.QLabel(self.centralwidget)
        self.label_dHD.setObjectName("label_dHD")
        self.gridLayout.addWidget(self.label_dHD, 1, 5, 1, 1)
        self.progressBarHD = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBarHD.setProperty("value", 24)
        self.progressBarHD.setObjectName("progressBarHD")
        self.gridLayout.addWidget(self.progressBarHD, 2, 2, 1, 5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 8, 5, 1, 1)
        self.lineEditX0 = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditX0.setFont(font)
        self.lineEditX0.setObjectName("lineEditX0")
        self.gridLayout.addWidget(self.lineEditX0, 7, 1, 1, 1)
        self.labelY0 = QtWidgets.QLabel(self.centralwidget)
        self.labelY0.setObjectName("labelY0")
        self.gridLayout.addWidget(self.labelY0, 7, 2, 1, 1)
        self.btnFindSource = QtWidgets.QPushButton(self.centralwidget)
        self.btnFindSource.setObjectName("btnFindSource")
        self.gridLayout.addWidget(self.btnFindSource, 8, 2, 1, 1)
        self.lineEditA0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditA0.setObjectName("lineEditA0")
        self.gridLayout.addWidget(self.lineEditA0, 7, 9, 1, 1)
        self.lineEditY0 = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditY0.setFont(font)
        self.lineEditY0.setObjectName("lineEditY0")
        self.gridLayout.addWidget(self.lineEditY0, 7, 5, 1, 1)
        self.btnEditPars = QtWidgets.QPushButton(self.centralwidget)
        self.btnEditPars.setObjectName("btnEditPars")
        self.gridLayout.addWidget(self.btnEditPars, 5, 0, 1, 2)
        self.labelA0 = QtWidgets.QLabel(self.centralwidget)
        self.labelA0.setObjectName("labelA0")
        self.gridLayout.addWidget(self.labelA0, 7, 8, 1, 1)
        self.labelX0 = QtWidgets.QLabel(self.centralwidget)
        self.labelX0.setObjectName("labelX0")
        self.gridLayout.addWidget(self.labelX0, 7, 0, 1, 1)
        self.labelMeasurement = QtWidgets.QLabel(self.centralwidget)
        self.labelMeasurement.setMinimumSize(QtCore.QSize(148, 27))
        self.labelMeasurement.setMaximumSize(QtCore.QSize(16777215, 27))
        self.labelMeasurement.setObjectName("labelMeasurement")
        self.gridLayout.addWidget(self.labelMeasurement, 0, 1, 1, 1)
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setObjectName("btnClear")
        self.gridLayout.addWidget(self.btnClear, 5, 2, 1, 1)
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setObjectName("btnBack")
        self.gridLayout.addWidget(self.btnBack, 5, 5, 1, 1)
        self.btnNext = QtWidgets.QPushButton(self.centralwidget)
        self.btnNext.setObjectName("btnNext")
        self.gridLayout.addWidget(self.btnNext, 5, 8, 1, 1)
        self.lineEdit_X = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_X.setReadOnly(True)
        self.lineEdit_X.setObjectName("lineEdit_X")
        self.gridLayout.addWidget(self.lineEdit_X, 0, 2, 1, 1)
        self.lineEdit_Y = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Y.setReadOnly(True)
        self.lineEdit_Y.setObjectName("lineEdit_Y")
        self.gridLayout.addWidget(self.lineEdit_Y, 0, 5, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 31))
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
        self.label_HD.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">HD [mSv/s]:</p></body></html>"))
        self.label_dHD.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">dHD [mSv/s]:</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Plot Graph"))
        self.labelY0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">y</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\"> [m]:</span></p></body></html>"))
        self.btnFindSource.setText(_translate("MainWindow", "Find Source"))
        self.btnEditPars.setText(_translate("MainWindow", "Edit Parameters"))
        self.labelA0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">A</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\"> [Bq]:</span></p></body></html>"))
        self.labelX0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">x</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\"> [m]:</span></p></body></html>"))
        self.labelMeasurement.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Measurement at:</p></body></html>"))
        self.btnClear.setText(_translate("MainWindow", "Clear"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.btnNext.setText(_translate("MainWindow", "Next"))
        self.lineEdit_X.setText(_translate("MainWindow", "x = ?"))
        self.lineEdit_Y.setText(_translate("MainWindow", "y = ?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
