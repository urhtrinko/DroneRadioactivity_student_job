# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tutorial01.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        self.main_label.setGeometry(QtCore.QRect(310, 170, 221, 71))
        self.main_label.setObjectName("main_label")
        self.button_OK = QtWidgets.QPushButton(self.centralwidget)
        self.button_OK.setGeometry(QtCore.QRect(280, 330, 241, 51))
        self.button_OK.setObjectName("button_OK")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        self.menuParameters = QtWidgets.QMenu(self.menubar)
        self.menuParameters.setObjectName("menuParameters")
        self.menuDoses = QtWidgets.QMenu(self.menubar)
        self.menuDoses.setObjectName("menuDoses")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuParameters.menuAction())
        self.menubar.addAction(self.menuDoses.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_label.setText(_translate("MainWindow", "Insert text"))
        self.button_OK.setText(_translate("MainWindow", "OK"))
        self.menuParameters.setTitle(_translate("MainWindow", "Parameters"))
        self.menuDoses.setTitle(_translate("MainWindow", "Doses"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
