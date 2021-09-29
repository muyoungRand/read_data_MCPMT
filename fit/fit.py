from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from fit_func import *
from fit_sine_ui import *
from fit_fock_population_ui import Ui_fit_fock
from fit_squeeze_ui import Ui_fit_sqzvac
from fit_superposition_fock_population_ui import Ui_fit_fock_s
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


class FitSqzVac(Fit):
    def __init__(self):
        super().__init__(Ui_fit_sqzvac())
        self.type='FitSqzVac'

    def getValue_aSpinBox_1(self):
        return (self.ui.aSpinBox_1.value())

    def getValue_aSpinBox_2(self):
        return (self.ui.aSpinBox_2.value())

    def getValue_rSpinBox_1(self):
        return (self.ui.rSpinBox_1.value())

    def getValue_rSpinBox_2(self):
        return (self.ui.rSpinBox_2.value())

    def getValue_nSpinBox(self):
        return (self.ui.nSpinBox.value())

    def getValue_TpiSpinBox_1(self):
        return(self.ui.TpiSpinBox_1.value())

    def getValue_TpiSpinBox_2(self):
        return(self.ui.TpiSpinBox_2.value())

    def getValue_gammaSpinBox_1(self):
        return(self.ui.gammaSpinBox_1.value())

    def getValue_gammaSpinBox_2(self):
        return(self.ui.gammaSpinBox_2.value())

    def fit(self,dataFile):
        p0 = [self.getValue_aSpinBox_1(), self.getValue_rSpinBox_1() ,self.getValue_TpiSpinBox_1()]
        data = dataFile.getdata()
        ntotal = self.getValue_nSpinBox()
        gamma = self.getValue_gammaSpinBox_1()*10**-4
        x = data[0]
        y = data[1]
        yerr = data[2]
        #res = fit_sinesquare_no_offset(x, y, yerr, p0, None)
        res = fit_squeezed_vac(x,y,yerr,p0,ntotal,gamma)
        xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)
        yfit = squeezed_vac_func(xfit, res[0], arg1 = [ntotal,gamma])

        #print(dataFile.getFilePath())
        #print(res)
        dataFile.set_fitdata(xfit, yfit)
        self.fitSignalDone.emit(self.currentIndex)

        self.ui.aSpinBox_1.setValue(res[0][0])
        self.ui.aSpinBox_2.setValue(res[-1][0])

        self.ui.rSpinBox_1.setValue(res[0][1])
        self.ui.rSpinBox_2.setValue(res[-1][1])

        self.ui.TpiSpinBox_1.setValue(res[0][2])
        self.ui.TpiSpinBox_2.setValue(res[-1][2])

        return None

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
        #print(res)
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

        self.max_n_fit = int(self.ui.SpinBox_Nmax.value())

        self.omega = np.pi/self.ui.SpinBox_Omega_1.value()
        self.gamma = self.ui.SpinBox_gamma_1.value()*10**-4
        self.rsb = self.ui.checkBox_RSB.isChecked()
        self.n_target = int(self.ui.SpinBox_Ntarget.value())
        self.p_target = self.ui.SpinBox_Ptarget_1.value()
        self.weights = generate_weight(self.max_n_fit, self.n_target, self.p_target)
        self.if_gamma_fixed = self.ui.checkBox_gamma.isChecked()
        self.res = fit_sum_multi_sine(x, y, self.max_n_fit, self.weights, self.omega, self.gamma,rsb=self.rsb,\
                                      gamma_fixed=self.if_gamma_fixed)
        self.fit_weights = self.res[0]
        self.fit_n_target = np.argmax(self.fit_weights)
        xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)
        yfit = sum_multi_sine(xfit, np.concatenate((self.fit_weights, self.res[1], self.res[-2]), axis=None), self.rsb)
        #print(self.res)
        dataFile.set_fitdata(xfit, yfit)
        self.fitSignalDone.emit(self.currentIndex)

        self.ui.SpinBox_Omega_1.setValue(np.pi/self.res[1])
        self.ui.SpinBox_Omega_2.setValue(np.pi*self.res[3]/self.res[1]**2)
        self.ui.SpinBox_gamma_1.setValue(self.res[4]*10**4)

        self.ui.SpinBox_Ntarget.setValue(self.fit_n_target)
        #print(self.res[0][self.fit_n_target])
        self.ui.SpinBox_Ptarget_1.setValue(self.fit_weights[self.fit_n_target])
        self.ui.textFitResult.setText("")
        self.ui.textFitResult.append('Population fit: '+'\n'+str(list(np.around(self.res[0]*100,3)))[1:-1])
        self.ui.textFitResult.append('\n')
        self.ui.textFitResult.append("Population fit error: "+'\n'+str(list(np.around(self.res[2]*100,3)))[1:-1])

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

class FitFock_S(Fit):
    '''
     Fitting superposition of Fock states
    '''
    def __init__(self):
        super().__init__(Ui_fit_fock_s())
        self.type='FitFock_S'
        self.qmc = Qt5MplCanvas()
        self.ui.verticalLayout_3.addWidget(self.qmc)

    def fit(self, dataFile,printdebug=True):
        # data is an object of dataPlot
        #p0 = [self.getValue_aSpinBox_1(), self.getValue_TpiSpinBox_1(), self.getValue_phaseSpinBox_1()]
        data = dataFile.getdata()
        x = data[0]
        y = data[1]
        yerr = data[2]

        self.max_n_fit = int(self.ui.SpinBox_Nmax.value())

        self.omega = np.pi/self.ui.SpinBox_Omega_1.value()
        self.gamma = self.ui.SpinBox_gamma_1.value()*10**-4
        self.rsb = self.ui.checkBox_RSB.isChecked()

        self.pinit_0 = self.ui.SpinBox_init_0.value()
        self.pinit_1 = self.ui.SpinBox_init_1.value()
        self.pinit_2 = self.ui.SpinBox_init_2.value()
        self.pinit_3 = self.ui.SpinBox_init_3.value()
        self.pinit_4 = self.ui.SpinBox_init_4.value()
        self.pinit_5 = self.ui.SpinBox_init_5.value()
        self.pinit_6 = self.ui.SpinBox_init_6.value()

        self.pmin_0 = self.ui.SpinBox_min_0.value()
        self.pmin_1 = self.ui.SpinBox_min_1.value()
        self.pmin_2 = self.ui.SpinBox_min_2.value()
        self.pmin_3 = self.ui.SpinBox_min_3.value()
        self.pmin_4 = self.ui.SpinBox_min_4.value()
        self.pmin_5 = self.ui.SpinBox_min_5.value()
        self.pmin_6 = self.ui.SpinBox_min_6.value()

        self.pmax_0 = self.ui.SpinBox_max_0.value()
        self.pmax_1 = self.ui.SpinBox_max_1.value()
        self.pmax_2 = self.ui.SpinBox_max_2.value()
        self.pmax_3 = self.ui.SpinBox_max_3.value()
        self.pmax_4 = self.ui.SpinBox_max_4.value()
        self.pmax_5 = self.ui.SpinBox_max_5.value()
        self.pmax_6 = self.ui.SpinBox_max_6.value()

        self.offset = self.ui.SpinBox_offset.value()

        self.weights_total = [self.pinit_0,self.pinit_1,self.pinit_2,\
                              self.pinit_3,self.pinit_4,self.pinit_5,\
                              self.pinit_6]

        self.lower_bounds_total = [self.pmin_0, self.pmin_1, self.pmin_2, \
                                   self.pmin_3, self.pmin_4, self.pmin_5, \
                                   self.pmin_6]

        self.upper_bounds_total = [self.pmax_0, self.pmax_1, self.pmax_2, \
                                   self.pmax_3, self.pmax_4, self.pmax_5, \
                                   self.pmax_6]

        self.weights = self.weights_total[:int(self.max_n_fit)]
        self.lower_bounds = self.lower_bounds_total[:int(self.max_n_fit)]
        self.upper_bounds = self.upper_bounds_total[:int(self.max_n_fit)]
        self.bounds=(self.lower_bounds,self.upper_bounds)
        #self.weights = generate_weight(self.max_n_fit, self.n_target, self.p_target)
        self.if_gamma_fixed = self.ui.checkBox_gamma.isChecked()
        #self.res = fit_sum_multi_sine(x, y, self.max_n_fit, self.weights, self.omega, self.gamma,rsb=self.rsb,\
                                      #gamma_fixed=self.if_gamma_fixed,\
                                      #customized_bound_population = self.bounds)
        self.res = fit_sum_multi_sine_offset(x, y, self.max_n_fit, self.weights, self.omega, self.gamma, offset=self.offset,\
                                             rsb=self.rsb, \
                                      gamma_fixed=self.if_gamma_fixed, \
                                      customized_bound_population=self.bounds)
        if printdebug==True:
            print('init weights',self.weights)
            print(self.res)
        self.fit_weights = self.res[0]
        self.fit_n_target = np.argmax(self.fit_weights)
        xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)

        #yfit = sum_multi_sine(xfit, np.concatenate((self.fit_weights, self.res[1], self.res[-2]), axis=None), self.rsb)
        yfit = sum_multi_sine_offset(xfit, np.concatenate((self.fit_weights, self.res[1], self.res[-2]), axis=None),\
                                     [self.offset,self.rsb])
        print(yfit)
        #print(self.res)
        dataFile.set_fitdata(xfit, yfit)
        self.fitSignalDone.emit(self.currentIndex)

        self.ui.SpinBox_Omega_1.setValue(np.pi/self.res[1])
        self.ui.SpinBox_Omega_2.setValue(np.pi*self.res[3]/self.res[1]**2)
        self.ui.SpinBox_gamma_1.setValue(self.res[4]*10**4)

        #self.ui.SpinBox_Ntarget.setValue(self.fit_n_target)
        #print(self.res[0][self.fit_n_target])
        #self.ui.SpinBox_Ptarget_1.setValue(self.fit_weights[self.fit_n_target])
        self.ui.textFitResult.setText("")
        self.ui.textFitResult.append('Population fit: '+'\n'+str(list(np.around(self.res[0]*100,3)))[1:-1])
        self.ui.textFitResult.append('\n')
        self.ui.textFitResult.append("Population fit error: "+'\n'+str(list(np.around(self.res[2]*100,3)))[1:-1])

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