import sys

from read_sequence_func import *

from sequence_ui import * 

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem
)

class sequenceWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_SequenceWindow()
        self.ui.setupUi(self)
        
    def updateTable(self, seq_file, delay = False):  
        self.name, self.data = get_seq(seq_file)
        self.active_tab = self.name['tab']
        
        self.ui.active_tab.setText('Active Tab: ' + self.active_tab)

        seq = self.ui.seqViewer
        
        seq.setColumnCount(3)
        seq.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        seq.setHorizontalHeaderItem(1, QTableWidgetItem('Durations'))
        seq.setHorizontalHeaderItem(2, QTableWidgetItem('Details'))
        
        seq.setRowCount(len(self.data))
        seq.verticalHeader().setVisible(False)
        
        for i in range(len(self.data)):
            seq.setItem(i, 0, QTableWidgetItem(self.data[i]['name']))
            
            # Label each chapter with colours like in MainWin.
            #   SBC = Yellow
            #   AWG = Magenta
            #   Normal = Grey
            if self.data[i]['type'] == 'DDS':
                seq.item(i, 0).setBackground(QtGui.QColor('lightGray'))
            elif self.data[i]['type'] == 'SBC':
                seq.item(i, 0).setBackground(QtGui.QColor('yellow'))
            elif self.data[i]['type'] == 'AWG':
                seq.item(i, 0).setBackground(QtGui.QColor('magenta'))
            
            # Easy way to make sure all durations are counted
            durations = []
            for j in range(10):
                try:
                    d = str(self.data[i]['delay' + str(j)])
                    
                    # Check if this delay was scanned
                    if self.data[i]['scanned' + str(j)] == True and delay == True:
                        d = d + u' (\u2713)' # If delay scanned, indicate with tick mark
                    durations.append(d)
                except:
                    pass
            durations = '\n'.join(durations)
            seq.setItem(i, 1, QTableWidgetItem(durations))
            
            # Add any additional details
            if self.data[i]['type'] == 'SBC':
                details = self.data[i]['SBC_details']
                nBar = details[0]
                nCycles = details[1]
                
                details = 'nBar = ' + str(nBar) + '\nnCycles = ' + str(nCycles)
                
                seq.setItem(i, 2, QTableWidgetItem(details))
                
            elif self.data[i]['type'] == 'AWG':
                details = self.data[i]['AWG_details']    
                
                formula = details['Formula']
                parameters = []
                
                for j in range(1, 16):
                    try:
                        param = details['x' + str(j)]    
                        param = 'x' + str(j) + ': ' + param[0] + '= ' + str(param[1])
                        parameters.append(param)
                    except:
                        pass
                    
                str_parameters = '\n'.join(parameters)
                
                details = formula + '\n' + str_parameters
                
                seq.setItem(i, 2, QTableWidgetItem(details))
        
            # Update sizes to show everything without clipping
            seq.resizeRowToContents(i)
        seq.resizeColumnToContents(2)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = sequenceWindow()
    w.show()
    sys.exit(app.exec())