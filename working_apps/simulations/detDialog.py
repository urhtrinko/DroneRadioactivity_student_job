# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(419, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_m = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_m.setObjectName("lineEdit_m")
        self.gridLayout.addWidget(self.lineEdit_m, 5, 2, 1, 1)
        self.label_h = QtWidgets.QLabel(Dialog)
        self.label_h.setObjectName("label_h")
        self.gridLayout.addWidget(self.label_h, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 11, 1, 1)
        self.label_m = QtWidgets.QLabel(Dialog)
        self.label_m.setObjectName("label_m")
        self.gridLayout.addWidget(self.label_m, 5, 0, 1, 2)
        self.labelX = QtWidgets.QLabel(Dialog)
        self.labelX.setObjectName("labelX")
        self.gridLayout.addWidget(self.labelX, 2, 0, 1, 2)
        self.label_dt = QtWidgets.QLabel(Dialog)
        self.label_dt.setObjectName("label_dt")
        self.gridLayout.addWidget(self.label_dt, 1, 0, 1, 2)
        self.labelSgrid = QtWidgets.QLabel(Dialog)
        self.labelSgrid.setObjectName("labelSgrid")
        self.gridLayout.addWidget(self.labelSgrid, 3, 5, 1, 2)
        self.labePhi = QtWidgets.QLabel(Dialog)
        self.labePhi.setObjectName("labePhi")
        self.gridLayout.addWidget(self.labePhi, 6, 0, 1, 2)
        self.labelY = QtWidgets.QLabel(Dialog)
        self.labelY.setObjectName("labelY")
        self.gridLayout.addWidget(self.labelY, 2, 5, 1, 1)
        self.labelGrid = QtWidgets.QLabel(Dialog)
        self.labelGrid.setObjectName("labelGrid")
        self.gridLayout.addWidget(self.labelGrid, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 10, 1, 1)
        self.lineEdit_h = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_h.setObjectName("lineEdit_h")
        self.gridLayout.addWidget(self.lineEdit_h, 0, 2, 1, 1)
        self.lineEdit_K = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_K.setObjectName("lineEdit_K")
        self.gridLayout.addWidget(self.lineEdit_K, 4, 2, 1, 1)
        self.btnSave = QtWidgets.QPushButton(Dialog)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 7, 6, 1, 5)
        self.btnClearInput = QtWidgets.QPushButton(Dialog)
        self.btnClearInput.setObjectName("btnClearInput")
        self.gridLayout.addWidget(self.btnClearInput, 7, 2, 1, 2)
        self.lineEditPhi = QtWidgets.QLineEdit(Dialog)
        self.lineEditPhi.setEnabled(True)
        self.lineEditPhi.setObjectName("lineEditPhi")
        self.gridLayout.addWidget(self.lineEditPhi, 6, 2, 1, 1)
        self.lineEdit_dt = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_dt.setObjectName("lineEdit_dt")
        self.gridLayout.addWidget(self.lineEdit_dt, 1, 2, 1, 1)
        self.lineEditX = QtWidgets.QLineEdit(Dialog)
        self.lineEditX.setObjectName("lineEditX")
        self.gridLayout.addWidget(self.lineEditX, 2, 2, 1, 1)
        self.lineEditGrid = QtWidgets.QLineEdit(Dialog)
        self.lineEditGrid.setObjectName("lineEditGrid")
        self.gridLayout.addWidget(self.lineEditGrid, 3, 2, 1, 1)
        self.label_K = QtWidgets.QLabel(Dialog)
        self.label_K.setObjectName("label_K")
        self.gridLayout.addWidget(self.label_K, 4, 0, 1, 2)
        self.lineEditSgrid = QtWidgets.QLineEdit(Dialog)
        self.lineEditSgrid.setEnabled(True)
        self.lineEditSgrid.setObjectName("lineEditSgrid")
        self.gridLayout.addWidget(self.lineEditSgrid, 3, 7, 1, 3)
        self.lineEditY = QtWidgets.QLineEdit(Dialog)
        self.lineEditY.setObjectName("lineEditY")
        self.gridLayout.addWidget(self.lineEditY, 2, 7, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit_h, self.lineEdit_dt)
        Dialog.setTabOrder(self.lineEdit_dt, self.lineEditX)
        Dialog.setTabOrder(self.lineEditX, self.lineEditY)
        Dialog.setTabOrder(self.lineEditY, self.lineEditGrid)
        Dialog.setTabOrder(self.lineEditGrid, self.lineEditSgrid)
        Dialog.setTabOrder(self.lineEditSgrid, self.lineEdit_K)
        Dialog.setTabOrder(self.lineEdit_K, self.lineEdit_m)
        Dialog.setTabOrder(self.lineEdit_m, self.lineEditPhi)
        Dialog.setTabOrder(self.lineEditPhi, self.btnSave)
        Dialog.setTabOrder(self.btnSave, self.btnClearInput)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_h.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">h [m]:</p></body></html>"))
        self.label_m.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">m []:</p></body></html>"))
        self.labelX.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">X [m]:</p></body></html>"))
        self.label_dt.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">dt [s]:</p></body></html>"))
        self.labelSgrid.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">s_grid []:</p></body></html>"))
        self.labePhi.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">phi [rad]:</p></body></html>"))
        self.labelY.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Y [m]:</p></body></html>"))
        self.labelGrid.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">grid []:</p></body></html>"))
        self.btnSave.setText(_translate("Dialog", "Save"))
        self.btnClearInput.setText(_translate("Dialog", "Clear Input"))
        self.label_K.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">K []</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
