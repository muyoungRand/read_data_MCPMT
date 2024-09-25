import sys
import numpy as np

from read_settings_func import *
from settings_ui import * 

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeWidgetItem
)

class settingWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
    def updateTree(self, set_file, freq = False):
        self.dds, self.scanned = get_set(set_file)

        scanned = []
        
        dev = self.scanned['dev']
        if self.scanned['prop'] == "CH0, Frequency":
            propp = "freq0"
        elif self.scanned['prop'] == "CH1, Frequency":
            propp = "freq1"
        elif self.scanned['prop'] == "CH0, Amplitude":
            propp = 'ampl0'
        elif self.scanned['prop'] == 'CH1, Amplitude':
            propp = 'ampl1'
        else:
            propp = self.scanned['prop']   
        scanned.append([dev.replace('DDS-', ''), propp])
            
        dev2 = self.scanned['dev2']
        if self.scanned['prop2'] == "CH0, Frequency":
            propp = "freq0"
        elif self.scanned['prop2'] == "CH1, Frequency":
            propp = "freq1"
        elif self.scanned['prop2'] == "CH0, Amplitude":
            propp = 'ampl0'
        elif self.scanned['prop2'] == 'CH1, Amplitude':
            propp = 'ampl1'
        else:
            propp = self.scanned['prop2']
        scanned.append([dev2.replace('DDS-', ''), propp])
        
        print(scanned)
        tree = self.ui.setViewer
        
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Devices", "Details"])

        devices = []
        params = dict()
        
        for dev in self.dds:
            name = dev['name']
            devices.append(name)
            
            params[name] = []
            
            for key, values in dev.items():
                if 'freq' in key:
                    params[name].append([key, np.round(values * 10**(-6), 5)])
                elif key != 'name':
                    params[name].append([key, values])
                    
        for device in devices:
            item = QTreeWidgetItem(tree)
            item.setText(0, device)
            
            for param in params[device]:
                subitem = QTreeWidgetItem(tree)
                subitem.setText(1, str(param))
 
                item.addChild(subitem)
                if device in scanned[0] and param[0] in scanned[0] and freq == True:
                    item.setBackground(0, QtGui.QColor('red'))
                    subitem.setBackground(1, QtGui.QColor('red'))
                elif device in scanned[1] and param[0] in scanned[1] and freq == True:
                    item.setBackground(0, QtGui.QColor('blue'))
                    subitem.setBackground(1, QtGui.QColor('blue'))
        
        if 'AWG' in scanned[0][0]:
            item = QTreeWidgetItem(tree)
            item.setText(0, scanned[0][0])
            
            subitem = QTreeWidgetItem(tree)
            subitem.setText(1, 'Param: ' + scanned[0][1])
            
            if freq == True:
                item.setBackground(0, QtGui.QColor('red'))
                subitem.setBackground(1, QtGui.QColor('red'))
            
        if 'AWG' in scanned[1][0]:
            item = QTreeWidgetItem(tree)
            item.setText(0, scanned[1][0])
            
            subitem = QTreeWidgetItem(tree)
            subitem.setText(1, scanned[1][1])
            
            if freq == True:
                item.setBackground(0, QtGui.QColor('red'))
                subitem.setBackground(1, QtGui.QColor('red'))
                
        tree.resizeColumnToContents(1)
                    
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = settingWindow()
    w.show()
    sys.exit(app.exec())