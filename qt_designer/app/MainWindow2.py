# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_ymax = QtWidgets.QLabel(self.centralwidget)
        self.label_ymax.setObjectName("label_ymax")
        self.gridLayout.addWidget(self.label_ymax, 2, 5, 1, 2)
        self.dose01 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose01.setObjectName("dose01")
        self.gridLayout.addWidget(self.dose01, 7, 5, 1, 2)
        self.dose00 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose00.setObjectName("dose00")
        self.gridLayout.addWidget(self.dose00, 7, 3, 1, 1)
        self.doseErr01 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr01.setObjectName("doseErr01")
        self.gridLayout.addWidget(self.doseErr01, 7, 7, 1, 1)
        self.doseErr00 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr00.setObjectName("doseErr00")
        self.gridLayout.addWidget(self.doseErr00, 7, 4, 1, 1)
        self.lineEdit_xmax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_xmax.setObjectName("lineEdit_xmax")
        self.gridLayout.addWidget(self.lineEdit_xmax, 2, 1, 1, 4)
        self.btn_Save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save.setObjectName("btn_Save")
        self.gridLayout.addWidget(self.btn_Save, 3, 10, 1, 1)
        self.lineEdit_h = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_h.setObjectName("lineEdit_h")
        self.gridLayout.addWidget(self.lineEdit_h, 1, 1, 1, 4)
        self.btn_plotGraph = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plotGraph.setObjectName("btn_plotGraph")
        self.gridLayout.addWidget(self.btn_plotGraph, 12, 3, 1, 2)
        self.label_Source = QtWidgets.QLabel(self.centralwidget)
        self.label_Source.setObjectName("label_Source")
        self.gridLayout.addWidget(self.label_Source, 12, 8, 1, 3)
        self.label_xmax = QtWidgets.QLabel(self.centralwidget)
        self.label_xmax.setObjectName("label_xmax")
        self.gridLayout.addWidget(self.label_xmax, 2, 0, 1, 1)
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setObjectName("label_h")
        self.gridLayout.addWidget(self.label_h, 1, 0, 1, 1)
        self.label_RAD = QtWidgets.QLabel(self.centralwidget)
        self.label_RAD.setObjectName("label_RAD")
        self.gridLayout.addWidget(self.label_RAD, 0, 0, 1, 4)
        self.btn_Source = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Source.setObjectName("btn_Source")
        self.gridLayout.addWidget(self.btn_Source, 12, 5, 1, 3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 3, 1, 5)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 7, 0, 2, 2)
        self.lineEdit_Ngrid = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Ngrid.setObjectName("lineEdit_Ngrid")
        self.gridLayout.addWidget(self.lineEdit_Ngrid, 3, 1, 1, 4)
        self.label_Ngrid = QtWidgets.QLabel(self.centralwidget)
        self.label_Ngrid.setObjectName("label_Ngrid")
        self.gridLayout.addWidget(self.label_Ngrid, 3, 0, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 8, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 5, 1, 3)
        self.lineEdit_ymax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ymax.setObjectName("lineEdit_ymax")
        self.gridLayout.addWidget(self.lineEdit_ymax, 2, 7, 1, 3)
        self.label_DOSE = QtWidgets.QLabel(self.centralwidget)
        self.label_DOSE.setObjectName("label_DOSE")
        self.gridLayout.addWidget(self.label_DOSE, 4, 0, 1, 11)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 3, 1, 2)
        self.btn_Save2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save2.setObjectName("btn_Save2")
        self.gridLayout.addWidget(self.btn_Save2, 12, 2, 1, 1)
        self.doseErr11 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr11.setObjectName("doseErr11")
        self.gridLayout.addWidget(self.doseErr11, 8, 7, 1, 1)
        self.dose11 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose11.setObjectName("dose11")
        self.gridLayout.addWidget(self.dose11, 8, 6, 1, 1)
        self.dose10 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose10.setObjectName("dose10")
        self.gridLayout.addWidget(self.dose10, 8, 3, 1, 1)
        self.doseErr10 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr10.setObjectName("doseErr10")
        self.gridLayout.addWidget(self.doseErr10, 8, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_ymax.setText(_translate("MainWindow", "y_max [m]:"))
        self.lineEdit_xmax.setText(_translate("MainWindow", "50"))
        self.btn_Save.setText(_translate("MainWindow", "Save"))
        self.lineEdit_h.setText(_translate("MainWindow", "40"))
        self.btn_plotGraph.setText(_translate("MainWindow", "Plot"))
        self.label_Source.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">x</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\"> = ? +/- ?</span></p><p align=\"center\"><span style=\" font-size:10pt;\"> y</span><span style=\" font-size:10pt; vertical-align:sub;\">0 </span><span style=\" font-size:10pt;\">= ? +/- ?</span></p></body></html>"))
        self.label_xmax.setText(_translate("MainWindow", "x_max [m]:"))
        self.label_h.setText(_translate("MainWindow", "h [h]:"))
        self.label_RAD.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">PARAMETERS</span></p></body></html>"))
        self.btn_Source.setText(_translate("MainWindow", "Source"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">x-coordinate[m]</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">25</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">y-coordinate[m]</p></body></html>"))
        self.lineEdit_Ngrid.setText(_translate("MainWindow", "2"))
        self.label_Ngrid.setText(_translate("MainWindow", "N_grid []:"))
        self.label_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">-25</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">25</p></body></html>"))
        self.lineEdit_ymax.setText(_translate("MainWindow", "50"))
        self.label_DOSE.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">DOSES AND ERRORS</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">-25</p></body></html>"))
        self.btn_Save2.setText(_translate("MainWindow", "Save"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_as.setText(_translate("MainWindow", "Save As"))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
