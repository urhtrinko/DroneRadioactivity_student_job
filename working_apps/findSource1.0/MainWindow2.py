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
        self.btn_Save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save.setObjectName("btn_Save")
        self.gridLayout.addWidget(self.btn_Save, 3, 10, 1, 1)
        self.label_xmax = QtWidgets.QLabel(self.centralwidget)
        self.label_xmax.setObjectName("label_xmax")
        self.gridLayout.addWidget(self.label_xmax, 2, 0, 1, 1)
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setObjectName("label_h")
        self.gridLayout.addWidget(self.label_h, 1, 0, 1, 1)
        self.label_RAD = QtWidgets.QLabel(self.centralwidget)
        self.label_RAD.setObjectName("label_RAD")
        self.gridLayout.addWidget(self.label_RAD, 0, 0, 1, 4)
        self.label_Xaxis = QtWidgets.QLabel(self.centralwidget)
        self.label_Xaxis.setObjectName("label_Xaxis")
        self.gridLayout.addWidget(self.label_Xaxis, 5, 3, 1, 5)
        self.label_y1 = QtWidgets.QLabel(self.centralwidget)
        self.label_y1.setObjectName("label_y1")
        self.gridLayout.addWidget(self.label_y1, 7, 2, 1, 1)
        self.label_Yaxis = QtWidgets.QLabel(self.centralwidget)
        self.label_Yaxis.setObjectName("label_Yaxis")
        self.gridLayout.addWidget(self.label_Yaxis, 7, 0, 2, 2)
        self.label_Ngrid = QtWidgets.QLabel(self.centralwidget)
        self.label_Ngrid.setObjectName("label_Ngrid")
        self.gridLayout.addWidget(self.label_Ngrid, 3, 0, 1, 1)
        self.label_y2 = QtWidgets.QLabel(self.centralwidget)
        self.label_y2.setObjectName("label_y2")
        self.gridLayout.addWidget(self.label_y2, 8, 2, 1, 1)
        self.label_x2 = QtWidgets.QLabel(self.centralwidget)
        self.label_x2.setObjectName("label_x2")
        self.gridLayout.addWidget(self.label_x2, 6, 5, 1, 3)
        self.doseErr11 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr11.setObjectName("doseErr11")
        self.gridLayout.addWidget(self.doseErr11, 8, 7, 1, 1)
        self.doseErr10 = QtWidgets.QLineEdit(self.centralwidget)
        self.doseErr10.setObjectName("doseErr10")
        self.gridLayout.addWidget(self.doseErr10, 8, 4, 1, 1)
        self.dose10 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose10.setObjectName("dose10")
        self.gridLayout.addWidget(self.dose10, 8, 3, 1, 1)
        self.btn_Save2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save2.setObjectName("btn_Save2")
        self.gridLayout.addWidget(self.btn_Save2, 11, 2, 2, 1)
        self.btn_plotGraph = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plotGraph.setObjectName("btn_plotGraph")
        self.gridLayout.addWidget(self.btn_plotGraph, 11, 3, 2, 2)
        self.lineEdit_ymax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ymax.setText("")
        self.lineEdit_ymax.setObjectName("lineEdit_ymax")
        self.gridLayout.addWidget(self.lineEdit_ymax, 2, 7, 1, 3)
        self.label_DOSE = QtWidgets.QLabel(self.centralwidget)
        self.label_DOSE.setObjectName("label_DOSE")
        self.gridLayout.addWidget(self.label_DOSE, 4, 0, 1, 11)
        self.label_x1 = QtWidgets.QLabel(self.centralwidget)
        self.label_x1.setObjectName("label_x1")
        self.gridLayout.addWidget(self.label_x1, 6, 3, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 11, 9, 1, 1)
        self.lineEdit_x0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x0.setObjectName("lineEdit_x0")
        self.gridLayout.addWidget(self.lineEdit_x0, 11, 10, 1, 1)
        self.label_x0 = QtWidgets.QLabel(self.centralwidget)
        self.label_x0.setObjectName("label_x0")
        self.gridLayout.addWidget(self.label_x0, 11, 8, 1, 1)
        self.label_y0 = QtWidgets.QLabel(self.centralwidget)
        self.label_y0.setObjectName("label_y0")
        self.gridLayout.addWidget(self.label_y0, 12, 8, 1, 1)
        self.lineEdit_h = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_h.setText("")
        self.lineEdit_h.setObjectName("lineEdit_h")
        self.gridLayout.addWidget(self.lineEdit_h, 1, 1, 1, 3)
        self.lineEdit_xmax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_xmax.setText("")
        self.lineEdit_xmax.setObjectName("lineEdit_xmax")
        self.gridLayout.addWidget(self.lineEdit_xmax, 2, 1, 1, 3)
        self.lineEdit_Ngrid = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Ngrid.setEnabled(False)
        self.lineEdit_Ngrid.setObjectName("lineEdit_Ngrid")
        self.gridLayout.addWidget(self.lineEdit_Ngrid, 3, 1, 1, 3)
        self.dose11 = QtWidgets.QLineEdit(self.centralwidget)
        self.dose11.setObjectName("dose11")
        self.gridLayout.addWidget(self.dose11, 8, 5, 1, 2)
        self.btn_Source = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Source.setObjectName("btn_Source")
        self.gridLayout.addWidget(self.btn_Source, 11, 5, 2, 3)
        self.lineEdit_y0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_y0.setObjectName("lineEdit_y0")
        self.gridLayout.addWidget(self.lineEdit_y0, 12, 10, 1, 1)
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
        self.label_ymax.setText(_translate("MainWindow", "<html><head/><body><p>y<span style=\" vertical-align:sub;\">max</span> [m]:</p></body></html>"))
        self.btn_Save.setText(_translate("MainWindow", "Save"))
        self.label_xmax.setText(_translate("MainWindow", "<html><head/><body><p>x<span style=\" vertical-align:sub;\">max</span> [m]:</p></body></html>"))
        self.label_h.setText(_translate("MainWindow", "h [h]:"))
        self.label_RAD.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">PARAMETERS</span></p></body></html>"))
        self.label_Xaxis.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">x-coordinate[m]</p></body></html>"))
        self.label_y1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">25</p></body></html>"))
        self.label_Yaxis.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">y-coordinate[m]</p></body></html>"))
        self.label_Ngrid.setText(_translate("MainWindow", "<html><head/><body><p>N<span style=\" vertical-align:sub;\">grid</span> []:</p></body></html>"))
        self.label_y2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">-25</p></body></html>"))
        self.label_x2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">25</p></body></html>"))
        self.btn_Save2.setText(_translate("MainWindow", "Save"))
        self.btn_plotGraph.setText(_translate("MainWindow", "Plot"))
        self.label_DOSE.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">DOSES AND ERRORS</span></p></body></html>"))
        self.label_x1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">-25</p></body></html>"))
        self.label_x0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">x</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\">[m]:</span></p></body></html>"))
        self.label_y0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">y</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\">[m]:</span></p></body></html>"))
        self.lineEdit_Ngrid.setText(_translate("MainWindow", "2"))
        self.btn_Source.setText(_translate("MainWindow", "Source"))
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
