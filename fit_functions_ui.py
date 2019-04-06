# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_functions.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Fit_Window(object):
    def setupUi(self, Fit_Window):
        Fit_Window.setObjectName("Fit_Window")
        Fit_Window.resize(184, 313)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Fit_Window.sizePolicy().hasHeightForWidth())
        Fit_Window.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(Fit_Window)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 168, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_showFunctions = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget_showFunctions.setObjectName("listWidget_showFunctions")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_showFunctions.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_showFunctions.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_showFunctions.addItem(item)
        self.verticalLayout.addWidget(self.listWidget_showFunctions)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Fit_Window)
        self.buttonBox.rejected.connect(Fit_Window.reject)
        self.buttonBox.accepted.connect(Fit_Window.accept)
        QtCore.QMetaObject.connectSlotsByName(Fit_Window)

    def retranslateUi(self, Fit_Window):
        _translate = QtCore.QCoreApplication.translate
        Fit_Window.setWindowTitle(_translate("Fit_Window", "Dialog"))
        __sortingEnabled = self.listWidget_showFunctions.isSortingEnabled()
        self.listWidget_showFunctions.setSortingEnabled(False)
        item = self.listWidget_showFunctions.item(0)
        item.setText(_translate("Fit_Window", "Sine"))
        item = self.listWidget_showFunctions.item(1)
        item.setText(_translate("Fit_Window", "Summation of Sine"))
        item = self.listWidget_showFunctions.item(2)
        item.setText(_translate("Fit_Window", "Sinc"))
        self.listWidget_showFunctions.setSortingEnabled(__sortingEnabled)

