import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog, QApplication, QFileDialog

from read_data_ui import *
from open_file_ui import *
from fit_functions_ui import *

from read_data_func import *
#from fit_functions import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os
class dataStore():
    def __init__(self,filename):
        self.filename = filename


class fitFunctions(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Fit_Window()
        self.ui.setupUi(self)
        #for i in
        #self.ui.listWidget_showFunctions.addItem()

class fitSine():
    def __init__(self):
        super().__init__()
        self.ui = Ui_fit_sine()
        self.ui.setupUi(self)
        #for i in
        #self.ui.listWidget_showFunctions.addItem()

class openFile(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FileWindow()
        self.ui.setupUi(self)
        #self.show()
        self.ui.pushButton_AddFiles.clicked.connect(self.openFileDialog)
        self.ui.pushButton_RemoveFiles.clicked.connect(self.removeFile)

        self.ui.listWidget_SelectedFiles.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.ui.listWidget_SelectedFiles.itemClicked.connect(self.addItemtoQueuePlot)

    def openFileDialog(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file','/home/ngchihuan/research/python/projects/read_data/')
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

    def addItemtoQueuePlot(self):
        items = self.ui.listWidget_SelectedFiles.selectedItems()
        self.selectedFiles = []
        for i in range(len(items)):
            self.selectedFiles.append(str(self.ui.listWidget_SelectedFiles.selectedItems()[i].text()))



class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.openFileDialog)
        self.ui.actionChoose_Functions.triggered.connect(self.openFitWindow)

        self.openFitUi=fitFunctions()
        #self.fitSineUi = fitSine()
        #self.fitSineUi.comboBox_chooseFile.

        self.openFileUi = openFile()
        self.openFileUi.ui.pushButton_PlotFiles.clicked.connect(self.plotFiles)

        self.qmc = Qt5MplCanvas()
        self.ui.verticalLayout.addWidget(self.qmc)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(self.qmc, self))


        self.show()

    def openFitWindow(self):
        self.openFitUi.exec_()

    def openFileDialog(self):

        self.openFileUi.exec_()




    def plotFiles(self):
        print(self.openFileUi.selectedFiles)
        self.plotData(self.openFileUi.selectedFiles)
        #self.dataplot.plot(y)

    def plotData(self,file_list):
        self.qmc.axes.clear()
        for file_path in file_list:
            data, hist, raw, timestamp = read_file2(file_path)  # read data
            #data=list(data)
            pr = process_raw(raw)  # process raw data into more convenient form
            nexp = get_nexp(pr)  # calculate number of experiments per point from raw data
            ts = get_timestamps(timestamp)

            # print len(data)

            # d = sort(data, 0)

            if len(data) == 20:  # We scan two parameters
                x = data[0]  # x axis
                y1 = data[4]  # counter 1
                y2 = data[6]  # counter 3
            else:  # we scan only one parameter
                x = data[0]  # x axis,
                y1 = data[3]  # counter 1
                y2 = data[5]  # counter 3

            err1 = sqrt(y1 * (1.0 - y1) / nexp)
            err2 = sqrt(y2 * (1.0 - y2) / nexp)
            #ylabel('P(bright)')

            #Plot by using Canvas
            # create an axis
            self.qmc.plot(x, y1,file_path)
            self.qmc.draw()

class Qt5MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # plot definition
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)



    def plot(self,x,y,file_path):
        #self.axes.legend()
        head, tail = os.path.split(file_path)
        print(head,tail)
        self.axes.plot(x,y,'-o',label=tail)
        self.axes.grid(b=True)
        self.axes.legend(loc='upper left')

if __name__=="__main__":
    app = QApplication(sys.argv)
    w=mainWindow()
    w.show()
    sys.exit(app.exec())
