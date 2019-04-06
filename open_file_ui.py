# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_file.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileWindow(object):
    def setupUi(self, FileWindow):
        FileWindow.setObjectName("FileWindow")
        FileWindow.resize(464, 300)
        self.listWidget_SelectedFiles = QtWidgets.QListWidget(FileWindow)
        self.listWidget_SelectedFiles.setGeometry(QtCore.QRect(10, 10, 441, 191))
        self.listWidget_SelectedFiles.setObjectName("listWidget_SelectedFiles")
        self.horizontalLayoutWidget = QtWidgets.QWidget(FileWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 210, 441, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_AddFiles = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_AddFiles.setObjectName("pushButton_AddFiles")
        self.horizontalLayout.addWidget(self.pushButton_AddFiles)
        self.pushButton_PlotFiles = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_PlotFiles.setObjectName("pushButton_PlotFiles")
        self.horizontalLayout.addWidget(self.pushButton_PlotFiles)
        self.pushButton_RemoveFiles = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_RemoveFiles.setObjectName("pushButton_RemoveFiles")
        self.horizontalLayout.addWidget(self.pushButton_RemoveFiles)

        self.retranslateUi(FileWindow)
        QtCore.QMetaObject.connectSlotsByName(FileWindow)

    def retranslateUi(self, FileWindow):
        _translate = QtCore.QCoreApplication.translate
        FileWindow.setWindowTitle(_translate("FileWindow", "Open Files"))
        self.pushButton_AddFiles.setText(_translate("FileWindow", "Add"))
        self.pushButton_AddFiles.setShortcut(_translate("FileWindow", "Ctrl+A"))
        self.pushButton_PlotFiles.setText(_translate("FileWindow", "Plot"))
        self.pushButton_RemoveFiles.setText(_translate("FileWindow", "Remove"))

