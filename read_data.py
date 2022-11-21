import sys
import os

from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from PyQt5.QtCore import *
from netgraph import EditableGraph

from read_data_ui import *
from open_file_ui import *
from fit_functions_ui import *

from read_data_func import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

sys.path.insert(0, 'fit')
from fit import *

class dataStore():
    def __init__(self, filename):
        self.filename = filename

class fitFunctions(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Fit_Window()
        self.ui.setupUi(self)
        #for i in
        #self.ui.listWidget_showFunctions.addItem()


class dataPlot():
    '''
    A class to represent data to plot. Also contains a fit.
    '''
    def __init__(self, file_path):
        self.file_path = file_path

        (self.x, self.y1, self.yerr1, self.y2, self.yerr2) = (None, None, None, None, None)

        self.ifProcessedData = False
        self.fitdata_x = None
        self.fitdata_y = None

    def set_fitdata(self, x, y):
        self.fitdata_x = x
        self.fitdata_y = y

    def get_fitdata(self):
        return (self.fitdata_x, self.fitdata_y)

    def getdata(self, channels = [5, 7, 9]):
        if self.ifProcessedData == False:
            (self.x, self.y1, self.yerr1, self.y2, self.yerr2) = self.read_data(channels)

        return (self.x, self.y1, self.yerr1, self.y2, self.yerr2)

    def read_data(self, channels):
        '''
        Process raw data
        Replace get_x_y by another processing_data script.

        :return:
            (x,y1,err1,y2,err2):    five self-explained columns data
        '''
        print('Processing File', str(self.file_path))

        (x, y, err1, y2, err2) = get_x_y(self.file_path, channels = channels)

        return (x, y, err1, y2, err2)

    def getFilePath(self):
        return self.file_path

class openFile(QDialog):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_FileWindow()
        self.ui.setupUi(self)
        #self.ui.pushButton_AddFiles.clicked.connect(self.openFileDialog)
        self.ui.pushButton_RemoveFiles.clicked.connect(self.removeFile)
        self.resized.connect(self.resizeFunction)

        self.ui.listWidget_SelectedFiles.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.ui.listWidget_SelectedFiles.setFocusPolicy(Qt.StrongFocus)
        #self.ui.listWidget_SelectedFiles.itemClicked.connect(self.addItemtoQueuePlot)

    def openFileDialog(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home/')
        print(fname)
        for i,f in enumerate(fname[0]):
            item = QtWidgets.QListWidgetItem(f)
            self.ui.listWidget_SelectedFiles.addItem(item)

    def removeFile(self):
        items = self.ui.listWidget_SelectedFiles.selectedItems()
        #for i in items:
        #self.ui.listWidget_SelectedFiles.takeItems(items)
        if not items: return
        for item in items:
            self.ui.listWidget_SelectedFiles.takeItem(self.ui.listWidget_SelectedFiles.row(item))
        '''
        Not sure if the attached dataPlot objects is also removed to clean memory.
        Move on for now. Should be ok with a small set of loaded dataFiles
        '''

    def retrieveSelectedObject(self):
        temp = []
        for i in self.ui.listWidget_SelectedFiles.selectedItems():
            temp.append(i.data(QtCore.Qt.UserRole))
        return temp

    def retrieveObject(self,item):
        temp = item.data(QtCore.Qt.UserRole)
        return temp

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resizeFunction(self):
        ref = self.ui.listWidget_SelectedFiles.height() # Ref point for buttons to refer to
        self.ui.listWidget_SelectedFiles.setGeometry(QtCore.QRect(10, 10, self.width()-20, self.height()-150))
        self.ui.horizontalLayoutWidget.setGeometry(10, ref+20, self.width()-20, 40)


class mainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.openFitUi=fitFunctions()

        self.openFileUi = openFile()

        self.openFitSineUi = FitSine()
        self.openFitFockUi = FitFock()
        self.openFitFock_S_Ui = FitFock_S()
        self.openFitSqzVac_Ui = FitSqzVac()

        self.qmc = Qt5MplCanvas()
        self.ui.verticalLayout.addWidget(self.qmc)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(self.qmc, self))

        self.dataPlot_database=[]


        self.ui.actionOpen.triggered.connect(self.openFileDialog)
        self.ui.actionChoose_Functions.triggered.connect(self.openFitWindow)
        self.ui.actionSine.triggered.connect(self.openFitSine)
        self.ui.actionFock_distribution.triggered.connect(self.openFitFock)
        self.ui.actionFock_superposition.triggered.connect(self.openFitFock_S)
        self.ui.actionSqz_Vac.triggered.connect(self.openFitSqzVac)

        self.openFileUi.ui.pushButton_PlotFiles.clicked.connect(self.plotFiles)
        self.openFileUi.ui.pushButton_AddFiles.clicked.connect(self.openAddFileDialog)

        self.openFitSineUi.fitSignal.connect(self.fitSignal_clicked)
        self.openFitSineUi.fitSignalDone.connect(self.fitSignal_done)

        self.openFitFockUi.fitSignal.connect(self.fitSignal_clicked)
        self.openFitFockUi.fitSignalDone.connect(self.fitSignal_done)

        self.openFitFock_S_Ui.fitSignal.connect(self.fitSignal_clicked)
        self.openFitFock_S_Ui.fitSignalDone.connect(self.fitSignal_done)

        self.openFitSqzVac_Ui.fitSignal.connect(self.fitSignal_clicked)
        self.openFitSqzVac_Ui.fitSignalDone.connect(self.fitSignal_done)

        self.active_channels = []
        self.ui.checkSCPMT.toggled.connect(self.pickChn0)
        self.ui.checkCH5.toggled.connect(self.pickChn5)
        self.ui.checkCH7.toggled.connect(self.pickChn7)
        self.ui.checkCH9.toggled.connect(self.pickChn9)

        self.ui.pushPlotReset.clicked.connect(self.resetplot)

        self.resized.connect(self.resizeFunction)
        
        self.show()

    def pickChn0(self): 
        if self.ui.checkSCPMT.isChecked():
            if 0 not in self.active_channels:
                self.active_channels.append(0)
            else:
                pass
        else:
            if 0 in self.active_channels:
                self.active_channels.remove(0)
            else:
                pass
    def pickChn5(self): 
        if self.ui.checkCH5.isChecked():
            if 1 not in self.active_channels:
                self.active_channels.append(1)
            else:
                pass
        else:
            if 1 in self.active_channels:
                self.active_channels.remove(1)
            else:
                pass
    def pickChn7(self): 
        if self.ui.checkCH7.isChecked():
            if 2 not in self.active_channels:
                self.active_channels.append(2)
            else:
                pass
        else:
            if 2 in self.active_channels:
                self.active_channels.remove(2)
            else:
                pass
    def pickChn9(self): 
        if self.ui.checkCH9.isChecked():
            if 3 not in self.active_channels:
                self.active_channels.append(3)
            else:
                pass
        else:
            if 3 in self.active_channels:
                self.active_channels.remove(3)
            else:
                pass

    def resetplot(self):
        self.plotFiles()

    @pyqtSlot(int,str)
    def fitSignal_clicked(self,i,Fit_type):
        data_to_fit = self.openFileUi.retrieveSelectedObject()[i]
        if Fit_type=='FitSine':
            self.openFitSineUi.fit(data_to_fit)
        elif Fit_type=='FitFock':
            print('Choose '+ Fit_type +' as function to fit')
            self.openFitFockUi.fit(data_to_fit)
        elif Fit_type=='FitFock_S':
            print('Choose ' + Fit_type + ' as function to fit')
            self.openFitFock_S_Ui.fit(data_to_fit)

        elif Fit_type=='FitSqzVac':
            print('Choose ' + Fit_type + ' as function to fit')
            self.openFitSqzVac_Ui.fit(data_to_fit)

    @pyqtSlot(int)
    def fitSignal_done(self,i):
        data_to_fit = self.openFileUi.retrieveSelectedObject()[i]
        x, y = data_to_fit.get_fitdata()
        if self.qmc.thereisfit==True: #to check if there is fit plot and remove it
            self.qmc.axes.lines[-1].remove()
        else:
            self.qmc.thereisfit = True
        self.qmc.axes.plot(x, y,'-',color='black')
        self.qmc.draw()

    def openFitSine(self):
        self.openFitSineUi.comboxBox_addItem(self.openFileUi.retrieveSelectedObject())
        self.openFitSineUi.exec_()

    def openFitFock(self):
        self.openFitFockUi.comboxBox_addItem(self.openFileUi.retrieveSelectedObject())
        self.openFitFockUi.exec_()

    def openFitFock_S(self):
        self.openFitFock_S_Ui.comboxBox_addItem(self.openFileUi.retrieveSelectedObject())
        self.openFitFock_S_Ui.exec_()

    def openFitSqzVac(self):
        self.openFitSqzVac_Ui.comboxBox_addItem(self.openFileUi.retrieveSelectedObject())
        self.openFitSqzVac_Ui.exec_()

    def openFitWindow(self):
        self.openFitUi.exec_()

    def openFileDialog(self):
        self.openFileUi.exec_()
        #print('List of all dataPlo')
        #print(self.openFileUi.retrieveSelectedObject())

    def openAddFileDialog(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file','/home/ngchihuan/research/python/projects/read_data/testdata/')
        #fname = QFileDialog.getOpenFileNames(self, 'Open file','/mnt/dzmitrylab/experiment/')
        print(fname)
        for i,f in enumerate(fname[0]):
            item = QtWidgets.QListWidgetItem(f)
            temp = dataPlot(f)
            item.setData(QtCore.Qt.UserRole, temp) #Attached an object to each item in the QListWidgetItem
            self.openFileUi.ui.listWidget_SelectedFiles.addItem(item)

    def AddFileDefault(self):
        '''
        Add default data files for quick debugging
        Not done yet
        :return:
        '''
        for i,f in enumerate(fname[0]):
            item = QtWidgets.QListWidgetItem(f)
            temp = dataPlot(f)
            item.setData(QtCore.Qt.UserRole, temp) #Attached an object to each item in the QListWidgetItem
            self.openFileUi.ui.listWidget_SelectedFiles.addItem(item)

    def plotFiles(self):
        #selectedItems = self.openFileUi.ui.listWidget_SelectedFiles.selectedItems()
        selectedItems = self.openFileUi.retrieveSelectedObject()
        self.qmc.axes.clear()
        self.qmc.thereisfit = False
        for f in selectedItems:
            x, y1, yerr1, y2, yerr2 = f.getdata()
            xfit, yfit = f.get_fitdata()

            for i in self.active_channels:
                if i == 0:
                    self.qmc.plot(x, y1, 0, f.getFilePath())
                else:
                    if i == 1:
                        chn = 5
                    elif i == 2:
                        chn = 7
                    elif i == 3:
                        chn = 9
                    self.qmc.plot(x, y2[i-1], chn, f.getFilePath())
            #if (xfit != None) and (yfit != None):
                #self.qmc.plot(xfit, y1, f.getFilePath())
            self.qmc.draw()

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resizeFunction(self):
        self.ui.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, self.width()-10, self.height()-80))
        self.qmc.setGeometry(QtCore.QRect(0, 0, self.width()-20, self.height()-90))

        


class Qt5MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self, parent = None, hold = False):
        # plot definition
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.thereisfit=False
        

    def plot(self,x,y,chn,file_path):
        #self.axes.legend()
        head, tail = os.path.split(file_path)
        #print(head,tail)
        self.axes.plot(x,y,'-o',label=tail + ', Chn' + str(chn))
        self.axes.grid(b=True)
        self.axes.legend(loc='upper left')

if __name__=="__main__":
    app = QApplication(sys.argv)
    w=mainWindow()
    w.show()
    sys.exit(app.exec())
