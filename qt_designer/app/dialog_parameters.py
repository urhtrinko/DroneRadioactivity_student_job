# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_parameters.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(436, 252)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_RAD = QtWidgets.QLabel(Dialog)
        self.label_RAD.setObjectName("label_RAD")
        self.gridLayout.addWidget(self.label_RAD, 0, 0, 1, 2)
        self.label_Ab = QtWidgets.QLabel(Dialog)
        self.label_Ab.setObjectName("label_Ab")
        self.gridLayout.addWidget(self.label_Ab, 1, 0, 1, 1)
        self.lineEdit_Ab = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Ab.setInputMask("")
        self.lineEdit_Ab.setObjectName("lineEdit_Ab")
        self.gridLayout.addWidget(self.lineEdit_Ab, 1, 1, 1, 1)
        self.label_DET = QtWidgets.QLabel(Dialog)
        self.label_DET.setObjectName("label_DET")
        self.gridLayout.addWidget(self.label_DET, 2, 0, 1, 2)
        self.label_h = QtWidgets.QLabel(Dialog)
        self.label_h.setObjectName("label_h")
        self.gridLayout.addWidget(self.label_h, 3, 0, 1, 1)
        self.lineEdit_h = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_h.setObjectName("lineEdit_h")
        self.gridLayout.addWidget(self.lineEdit_h, 3, 1, 1, 1)
        self.label_xmax = QtWidgets.QLabel(Dialog)
        self.label_xmax.setObjectName("label_xmax")
        self.gridLayout.addWidget(self.label_xmax, 4, 0, 1, 1)
        self.lineEdit_xmax = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_xmax.setObjectName("lineEdit_xmax")
        self.gridLayout.addWidget(self.lineEdit_xmax, 4, 1, 1, 1)
        self.label_ymax = QtWidgets.QLabel(Dialog)
        self.label_ymax.setObjectName("label_ymax")
        self.gridLayout.addWidget(self.label_ymax, 4, 2, 1, 1)
        self.lineEdit_ymax = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ymax.setObjectName("lineEdit_ymax")
        self.gridLayout.addWidget(self.lineEdit_ymax, 4, 3, 1, 2)
        self.label_Ngrid = QtWidgets.QLabel(Dialog)
        self.label_Ngrid.setObjectName("label_Ngrid")
        self.gridLayout.addWidget(self.label_Ngrid, 5, 0, 1, 1)
        self.lineEdit_Ngrid = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Ngrid.setObjectName("lineEdit_Ngrid")
        self.gridLayout.addWidget(self.lineEdit_Ngrid, 5, 1, 1, 1)
        self.btn_Cancel = QtWidgets.QPushButton(Dialog)
        self.btn_Cancel.setObjectName("btn_Cancel")
        self.gridLayout.addWidget(self.btn_Cancel, 6, 2, 1, 2)
        self.btn_Save = QtWidgets.QPushButton(Dialog)
        self.btn_Save.setObjectName("btn_Save")
        self.gridLayout.addWidget(self.btn_Save, 6, 4, 1, 1)

        self.retranslateUi(Dialog)
        self.btn_Cancel.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_RAD.setText(_translate("Dialog", "RADIATION"))
        self.label_Ab.setText(_translate("Dialog", "A_b [Bq]:"))
        self.label_DET.setText(_translate("Dialog", "DETECTOR"))
        self.label_h.setText(_translate("Dialog", "h [h]:"))
        self.label_xmax.setText(_translate("Dialog", "x_max [m]:"))
        self.label_Ngrid.setText(_translate("Dialog", "N_grid []:"))
        self.label_ymax.setText(_translate("Dialog", "y_max [m]:"))

        #User input text
        self.lineEdit_xmax.setText(_translate("Dialog", "50"))
        self.lineEdit_ymax.setText(_translate("Dialog", "50"))
        self.lineEdit_Ngrid.setText(_translate("Dialog", "2"))
        #User input text

        self.btn_Cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_Save.setText(_translate("Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
