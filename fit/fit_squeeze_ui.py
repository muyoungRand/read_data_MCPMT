# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_squeeze.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fit_sqzvac(object):
    def setupUi(self, fit_sqzvac):
        fit_sqzvac.setObjectName("fit_sqzvac")
        fit_sqzvac.resize(467, 375)
        self.label_4 = QtWidgets.QLabel(fit_sqzvac)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayoutWidget = QtWidgets.QWidget(fit_sqzvac)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 110, 427, 245))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.aSpinBox_1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.aSpinBox_1.setFont(font)
        self.aSpinBox_1.setDecimals(5)
        self.aSpinBox_1.setMaximum(9999.99)
        self.aSpinBox_1.setObjectName("aSpinBox_1")
        self.gridLayout_3.addWidget(self.aSpinBox_1, 0, 1, 1, 1)
        self.rSpinBox_1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rSpinBox_1.setFont(font)
        self.rSpinBox_1.setMaximum(99.99)
        self.rSpinBox_1.setProperty("value", 10.0)
        self.rSpinBox_1.setObjectName("rSpinBox_1")
        self.gridLayout_3.addWidget(self.rSpinBox_1, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)
        self.gammaSpinBox_1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.gammaSpinBox_1.setFont(font)
        self.gammaSpinBox_1.setDecimals(4)
        self.gammaSpinBox_1.setMaximum(100.0)
        self.gammaSpinBox_1.setProperty("value", 0.0)
        self.gammaSpinBox_1.setObjectName("gammaSpinBox_1")
        self.gridLayout_3.addWidget(self.gammaSpinBox_1, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 4, 0, 1, 1)
        self.aSpinBox_2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.aSpinBox_2.setFont(font)
        self.aSpinBox_2.setDecimals(5)
        self.aSpinBox_2.setMaximum(9999.99)
        self.aSpinBox_2.setObjectName("aSpinBox_2")
        self.gridLayout_3.addWidget(self.aSpinBox_2, 0, 2, 1, 1)
        self.rSpinBox_2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rSpinBox_2.setFont(font)
        self.rSpinBox_2.setDecimals(5)
        self.rSpinBox_2.setMaximum(9999.99)
        self.rSpinBox_2.setObjectName("rSpinBox_2")
        self.gridLayout_3.addWidget(self.rSpinBox_2, 1, 2, 1, 1)
        self.TpiSpinBox_1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.TpiSpinBox_1.setFont(font)
        self.TpiSpinBox_1.setMaximum(99999.99)
        self.TpiSpinBox_1.setProperty("value", 10.0)
        self.TpiSpinBox_1.setObjectName("TpiSpinBox_1")
        self.gridLayout_3.addWidget(self.TpiSpinBox_1, 3, 1, 1, 1)
        self.nSpinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.nSpinBox.setFont(font)
        self.nSpinBox.setMinimum(1)
        self.nSpinBox.setProperty("value", 10)
        self.nSpinBox.setObjectName("nSpinBox")
        self.gridLayout_3.addWidget(self.nSpinBox, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.TpiSpinBox_2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.TpiSpinBox_2.setFont(font)
        self.TpiSpinBox_2.setMaximum(99999.99)
        self.TpiSpinBox_2.setProperty("value", 10.0)
        self.TpiSpinBox_2.setObjectName("TpiSpinBox_2")
        self.gridLayout_3.addWidget(self.TpiSpinBox_2, 3, 2, 1, 1)
        self.gammaSpinBox_2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.gammaSpinBox_2.setFont(font)
        self.gammaSpinBox_2.setDecimals(4)
        self.gammaSpinBox_2.setMaximum(1.0)
        self.gammaSpinBox_2.setProperty("value", 0.0)
        self.gammaSpinBox_2.setObjectName("gammaSpinBox_2")
        self.gridLayout_3.addWidget(self.gammaSpinBox_2, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.DoneButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.DoneButton.setFont(font)
        self.DoneButton.setObjectName("DoneButton")
        self.gridLayout_3.addWidget(self.DoneButton, 5, 2, 1, 1)
        self.fitButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.fitButton.setFont(font)
        self.fitButton.setObjectName("fitButton")
        self.gridLayout_3.addWidget(self.fitButton, 5, 1, 1, 1)
        self.comboBox_chooseFile = QtWidgets.QComboBox(fit_sqzvac)
        self.comboBox_chooseFile.setGeometry(QtCore.QRect(20, 70, 406, 27))
        self.comboBox_chooseFile.setObjectName("comboBox_chooseFile")

        self.retranslateUi(fit_sqzvac)
        self.DoneButton.clicked.connect(fit_sqzvac.close)
        QtCore.QMetaObject.connectSlotsByName(fit_sqzvac)

    def retranslateUi(self, fit_sqzvac):
        _translate = QtCore.QCoreApplication.translate
        fit_sqzvac.setWindowTitle(_translate("fit_sqzvac", "fit_sqzvac"))
        self.label_4.setText(_translate("fit_sqzvac", "Fit: \n"
"y = a/2 * (1 - ...)"))
        self.label_5.setText(_translate("fit_sqzvac", "Tpi"))
        self.label_2.setText(_translate("fit_sqzvac", "r"))
        self.label_6.setText(_translate("fit_sqzvac", "gamma1E-4"))
        self.label.setText(_translate("fit_sqzvac", "a"))
        self.label_3.setText(_translate("fit_sqzvac", "n"))
        self.DoneButton.setText(_translate("fit_sqzvac", "Done"))
        self.fitButton.setText(_translate("fit_sqzvac", "Fit"))

