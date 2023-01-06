# Form implementation generated from reading ui file 'r2d2_sound_control.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 114)
        self.pushButton_speak = QtWidgets.QPushButton(Dialog)
        self.pushButton_speak.setGeometry(QtCore.QRect(300, 40, 89, 25))
        self.pushButton_speak.setObjectName("pushButton_speak")
        self.lineEdit_speak = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_speak.setGeometry(QtCore.QRect(60, 40, 201, 25))
        self.lineEdit_speak.setObjectName("lineEdit_speak")

        self.retranslateUi(Dialog)
        self.pushButton_speak.clicked.connect(Dialog.clicked_speak)
        self.lineEdit_speak.returnPressed.connect(Dialog.clicked_speak)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_speak.setText(_translate("Dialog", "Say Out"))