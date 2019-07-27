from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from fit_func import *
from fit_sine_ui import *
from fit_fock_population_ui import Ui_fit_fock
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
class Fit(QDialog):
    fitSignal = pyqtSignal(int,str)
    fitSignalDone = pyqtSignal(int)
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)

        self.currentIndex=0
        self.ui.fitButton.clicked.connect(self.fitButton_emit)

        self.ui.comboBox_chooseFile.currentIndexChanged.connect(self.selectionChange)
        self.type='general'

    def fitButton_emit(self):
        self.fitSignal.emit(self.currentIndex,self.type)

    def comboxBox_addItem(self, filelist):
        self.filelist = filelist
        self.ui.comboBox_chooseFile.clear()
        for f in self.filelist:
            self.ui.comboBox_chooseFile.addItem(str(f.getFilePath()))

    def selectionChange(self, i):
        print('current index ', i)
        self.currentIndex = i
        print(self.ui.comboBox_chooseFile.currentText())

class FitSine(Fit):
    def __init__(self):
        super().__init__(Ui_fit_sine())
        self.type='FitSine'

    def getValue_aSpinBox_1(self):
        return(self.ui.aSpinBox_1.value())

    def getValue_aSpinBox_2(self):
        return(self.ui.aSpinBox_2.value())

    def getValue_phaseSpinBox_1(self):
        return(self.ui.phaseSpinBox_1.value())

    def getValue_phaseSpinBox_2(self):
        return(self.ui.phaseSpinBox_2.value())

    def getValue_TpiSpinBox_1(self):
        return(self.ui.TpiSpinBox_1.value())

    def getValue_TpiSpinBox_2(self):
        return(self.ui.TpiSpinBox_2.value())

    def fit(self, dataFile):
        # data is an object of dataPlot
        p0 = [self.getValue_aSpinBox_1(), self.getValue_TpiSpinBox_1(), self.getValue_phaseSpinBox_1()]
        data = dataFile.getdata()
        x = data[0]
        y = data[1]
        yerr = data[2]
        res = fit_sinesquare_no_offset(x, y, yerr, p0, None)
        xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)
        yfit = sinesquare_no_offset(xfit, res[0], None)

        #print(dataFile.getFilePath())
        print(res)
        dataFile.set_fitdata(xfit, yfit)
        self.fitSignalDone.emit(self.currentIndex)

        self.ui.aSpinBox_1.setValue(res[0][0])
        self.ui.aSpinBox_2.setValue(res[-1][0])
        self.ui.TpiSpinBox_1.setValue(res[0][1])
        self.ui.TpiSpinBox_2.setValue(res[-1][1])
        self.ui.phaseSpinBox_1.setValue(res[0][2])
        self.ui.phaseSpinBox_2.setValue(res[-1][2])
        return None

class FitFock(Fit):
    def __init__(self):
        super().__init__(Ui_fit_fock())
        self.type='FitFock'
        self.qmc = Qt5MplCanvas()
        self.ui.verticalLayout_3.addWidget(self.qmc)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea,              NavigationToolbar(self.qmc, self))


    def fit(self, dataFile):
        # data is an object of dataPlot
        #p0 = [self.getValue_aSpinBox_1(), self.getValue_TpiSpinBox_1(), self.getValue_phaseSpinBox_1()]
        data = dataFile.getdata()
        x = data[0]
        y = data[1]
        yerr = data[2]

        #print(dataFile.getFilePath())


        self.max_n_fit = int(self.ui.SpinBox_Nmax.value())

        self.omega = np.pi/self.ui.SpinBox_Omega_1.value()
        self.gamma = self.ui.SpinBox_gamma_1.value()*10**-4
        self.rsb = self.ui.checkBox_RSB.isChecked()
        self.n_target = int(self.ui.SpinBox_Ntarget.value())
        self.p_target = self.ui.SpinBox_Ptarget_1.value()
        self.weights = generate_weight(self.max_n_fit, self.n_target, self.p_target)

        self.res = fit_sum_multi_sine(x, y, self.max_n_fit, self.weights, self.omega, self.gamma,rsb=self.rsb)
        self.fit_weights = self.res[0]
        self.fit_n_target = np.argmax(self.fit_weights)
        xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)
        yfit = sum_multi_sine(xfit, np.concatenate((self.fit_weights, self.res[1], self.res[-2]), axis=None), self.rsb)
        print(self.res)
        dataFile.set_fitdata(xfit, yfit)
        self.fitSignalDone.emit(self.currentIndex)



        '''
        if rsb == True:
            print('RSB time evo')
            phonon = np.arange(0, max_n_fit, 1)
        else:
            phonon = np.arange(0, max_n_fit, 1)
        print(phonon)
        nbar = np.dot(res[0], phonon)
        '''
        self.ui.SpinBox_Omega_1.setValue(np.pi/self.res[1])
        self.ui.SpinBox_Omega_2.setValue(np.pi*self.res[3]/self.res[1]**2)
        self.ui.SpinBox_gamma_1.setValue(self.res[4]*10**4)

        self.ui.SpinBox_Ntarget.setValue(self.fit_n_target)
        #print(self.res[0][self.fit_n_target])
        self.ui.SpinBox_Ptarget_1.setValue(self.fit_weights[self.fit_n_target])
        self.ui.textFitResult.setText("")
        self.ui.textFitResult.append('Population fit: '+str(list(np.around(self.res[0],4)))[1:-1])
        self.ui.textFitResult.append('\n')
        self.ui.textFitResult.append("Population fit error: "+str(list(np.around(self.res[2],4)))[1:-1])

        self.plotFockDistribution()
        #dataFile.set_fitdata(xfit, yfit)
        #self.fitSignalDone.emit(self.currentIndex)

        #self.setValue_aSpinBox_1(res[0][0])
        #self.setValue_aSpinBox_2(res[-1][0])
        #self.setValue_TpiSpinBox_1(res[0][1])
        #self.setValue_TpiSpinBox_2(res[-1][1])
        #self.setValue_phaseSpinBox_1(res[0][2])
        #self.setValue_phaseSpinBox_2(res[-1][2])
        return None

    def plotFockDistribution(self):
        self.qmc.axes.clear()
        self.max_n_fit = int(self.ui.SpinBox_Nmax.value())
        self.phonon=np.arange(0,self.max_n_fit,1)
        self.qmc.barplot(self.phonon, self.res[0], self.res[2])
        self.qmc.draw()

class Qt5MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # plot definition
        self.fig = Figure(figsize=(1,2))
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.thereisfit=False


    def plot(self,x,y,file_path):
        #self.axes.legend()
        head, tail = os.path.split(file_path)
        print(head,tail)
        self.axes.plot(x,y,'-o',label=tail)
        self.axes.grid(b=True)
        self.axes.legend(loc='upper left')

    def barplot(self,x,y,yerr):
        self.axes.set_ylim(0, 1)
        self.axes.set_xticks(x)
        self.axes.bar(x,y,yerr=yerr)