import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from read_data_ui import *
from open_file_ui import *
from fit_functions_ui import *
from PyQt5.QtCore import *

from read_data_func import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os

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

        (self.x, self.y1, self.yerr1, self.y2, self.yerr2, self.y5, self.yerr5, self.y7, self.yerr7, self.y8, self. yerr9) = (None, None, None, None, None, None, None, None, None, None, None, None, None)

        self.ifProcessedData = False
        self.fitdata_x = None
        self.fitdata_y = None

    def set_fitdata(self, x, y):
        self.fitdata_x = x
        self.fitdata_y = y

    def get_fitdata(self):
        return (self.fitdata_x, self.fitdata_y)

    def getdata(self):
        print('If processed data ', self.ifProcessedData)

        if self.ifProcessedData == False:
            (self.x, self.y1, self.yerr1, self.y2, self.yerr2, self.y5, self.yerr5, self.y7, self.yerr7, self.y8, self. yerr9) = self.read_data()

        return (self.x, self.y1, self.yerr1, self.y2, self.yerr2, self.y5, self.yerr5, self.y7, self.yerr7, self.y8, self. yerr9)

    def read_data(self):
        '''
        Process raw data
        Replace get_x_y by another processing_data script.

        :return:
            (x,y1,err1,y2,err2):    five self-explained columns data
        '''
        print('Processing File', str(self.file_path))

        (x, y1, err1, y2, err2, y5, err5, y7, err7, y9, err9) = get_x_y(self.file_path)

        return (x, y1, err1, y2, err2, y5, err5, y7, err7, y9, err9)

    def getFilePath(self):
        return self.file_path

class openFile(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FileWindow()
        self.ui.setupUi(self)
        #self.ui.pushButton_AddFiles.clicked.connect(self.openFileDialog)
        self.ui.pushButton_RemoveFiles.clicked.connect(self.removeFile)

        self.ui.listWidget_SelectedFiles.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.ui.listWidget_SelectedFiles.setFocusPolicy(Qt.StrongFocus)
        #self.ui.listWidget_SelectedFiles.itemClicked.connect(self.addItemtoQueuePlot)

    def openFileDialog(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file','/home/ngchihuan/research/python/projects/read_data/test/data/')
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home/')
        #fname = QFileDialog.getOpenFileNames(self, 'Open file','/mnt/dzmitrylab/experiment/')
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



class mainWindow(QMainWindow):

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


        self.show()

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
            self.qmc.plot(x, y1, f.getFilePath())
            #if (xfit != None) and (yfit != None):
                #self.qmc.plot(xfit, y1, f.getFilePath())
            self.qmc.draw()


class Qt5MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # plot definition
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.thereisfit=False


    def plot(self,x,y,file_path):
        #self.axes.legend()
        head, tail = os.path.split(file_path)
        #print(head,tail)
        self.axes.plot(x,y,'-o',label=tail)
        self.axes.grid(b=True)
        self.axes.legend(loc='upper left')

if __name__=="__main__":
    app = QApplication(sys.argv)
    w=mainWindow()
    w.show()
    sys.exit(app.exec())
