'''
A collection of popular functions to fit. 
Should be frequently updated and used somewhere else too.

'''
import numpy as np
from scipy.optimize import curve_fit
import math
def sine_no_offset(x,p,arg1):
    [a, b, phase] = p
    return a*np.sin(b*x+phase)

def sinesquare_no_offset(x,p,arg1):
    [a, b, phase] = p
    return a*(np.sin(2*np.pi/(b*4)*x+phase))**2

def fit_sinesquare_no_offset(t,y,yerr,p,arg1):
    p0 = p
    res = fit_leastsq(p0, t, y, None, sinesquare_no_offset, 0)
    p_fit = res[0]
    p_fit_err = res[-1]
    return p_fit, p_fit_err

def fit_sine_no_offset(t,y,yerr,p,arg1):
    p0 = p
    res = fit_leastsq(p0, t, y, None, sine_no_offset, 0)
    p_fit = res[0]
    p_fit_err = res[-1]
    return p_fit, p_fit_err

def fit_squeezed_vac(t,y,yerr,p0,ntotal,gamma,bounds=[-np.inf,np.inf]):
    bounds=[0,[1,np.inf,np.inf]]
    res= fit_leastsq(p0,t,y,yerr,squeezed_vac_func,[ntotal,gamma],bounds=bounds)
    return res

def squeezed_vac_func(x, p0, arg1=[100, 7E-5]):
    # Should fit with gamma and n_total as fitting parameters. will give inf convariance matrix
    # It is recommended to use large n_total. otherwise, Pe(t=0) != 0
    [a, r, Tpi] = p0
    [n_total, gamma] = arg1
    evenlist = []
    for n in range(0, n_total):
        if n % 2 == 0:
            evenlist.append(n)
    sqz_array = np.array(
        [np.tanh(r) ** (n) / np.cosh(r) * (math.factorial(n)) / ((math.factorial(int(n / 2))) ** 2 * 2 ** (n)) \
         * np.cos(np.sqrt(n + 1) * x * np.pi / Tpi) * np.exp(- np.sqrt(n + 1) * gamma * x) for n in evenlist])

    return (a / 2.0) * (1 - np.sum(sqz_array, axis=0))

def sum_multi_sine(t, p, rsb=True):
    '''
    max_n_fit here is defined to be the number of Fock states involved in the fitting. max_n_fit=3 means fitting into 0,1,2
    p is a list/tuple that contains something like the following (p0,p1,p2..,p_max_n_fit-1,gamma,omega
    arg1 is True if rsb is chosen
            False if bsb is chosen
    '''

    res = np.zeros_like(t)
    max_n_fit = int(np.size(p) - 2)

    a = list(p[:max_n_fit])
    a[-1] = 1 - np.sum(a[:-1])
    # Omega_0=p[-1]

    Omega_0 = p[max_n_fit]
    gamma = p[max_n_fit + 1]
    if rsb == True:
        Omega = Omega_0 * np.sqrt(
            np.linspace(0, max_n_fit - 1, max_n_fit))  # 15/4 modified to start from 0 to include population of 0
    else:
        Omega = Omega_0 * np.sqrt(np.linspace(1, max_n_fit - 1, max_n_fit))
    for i in range(max_n_fit):
        res = res + a[i] * np.cos(Omega[i] * t) * np.exp(-gamma * (i + 2) ** (0.7) * t)
    res = 1.0 / 2 - res / 2.0
    return res


def sum_multi_sine_offset(t, p, arg1=[0.0,True]):
    '''
    max_n_fit here is defined to be the number of Fock states involved in the fitting. max_n_fit=3 means fitting into 0,1,2
    p is a list/tuple that contains something like the following (p0,p1,p2..,p_max_n_fit-1,gamma,omega,offset)
    arg1 is True if rsb is chosen
            False if bsb is chosen
    '''
    offset = arg1[0]
    rsb=arg1[1]
    res = np.zeros_like(t)
    max_n_fit = int(np.size(p) - 2)

    a = list(p[:max_n_fit])
    a[-1] = 1 - np.sum(a[:-1])
    # Omega_0=p[-1]

    Omega_0 = p[max_n_fit]
    gamma = p[max_n_fit + 1]
    if rsb == True:
        Omega = Omega_0 * np.sqrt(
            np.linspace(0, max_n_fit - 1, max_n_fit))  # 15/4 modified to start from 0 to include population of 0
    else:
        Omega = Omega_0 * np.sqrt(np.linspace(1, max_n_fit - 1, max_n_fit))
    for i in range(max_n_fit):
        res = res + a[i] * np.cos(Omega[i] * t) * np.exp(-gamma * (i + 2) ** (0.7) * t)
    res = 1 / 2.0 - res / 2.0 + offset
    return res

def sum_multi_sine_fixed_gamma(t, p, rsb=True,gamma=1E-4):
    '''
    max_n_fit here is defined to be the number of Fock states involved in the fitting. max_n_fit=3 means fitting into 0,1,2
    p is a list/tuple that contains something like the following (p0,p1,p2..,p_max_n_fit-1,gamma,omega
    arg1 is True if rsb is chosen
            False if bsb is chosen
    '''

    res = np.zeros_like(t)
    max_n_fit = int(np.size(p) - 2)
    failcond = 0
    a = list(p[:max_n_fit])
    for i in a:
        if i<0:
            failcond=1
    if np.sum(a[:-1])>1 or failcond==1:
        return 1e15
    else:
        a[-1] = 1 - np.sum(a[:-1])
        # Omega_0=p[-1]

        Omega_0 = p[-1]
        gamma = gamma
        if rsb == True:
            Omega = Omega_0 * np.sqrt(
                np.linspace(0, max_n_fit - 1, max_n_fit))  # 15/4 modified to start from 0 to include population of 0
        else:
            Omega = Omega_0 * np.sqrt(np.linspace(1, max_n_fit - 1, max_n_fit))
        for i in range(max_n_fit):
            res = res + a[i] * np.cos(Omega[i] * t) * np.exp(-gamma * (i + 2) ** (0.7) * t)
        res = 1 / 2.0 - res / 2.0
        return res

def fit_sum_multi_sine(t, y, max_n_fit, weights, Omega_0, gamma, rsb=True,gamma_fixed=False,\
                       customized_bound_population=None):
    '''
    Fitting of a data to a sum of weighted sine functions
    The angular frequencies of the sine functions is initialied to be a sqrt of geometric serires of Omega_0
    The weights are initialized to be a uniform normalized set

    Arguments:

        t: x axis of data
        y: y axis of data
        max_n_fit: maximum number of the elements of the sum
        Omega_0: Nominal Angular freq
        gamma: exponential damping. Gamma_n=gamma*(n+1)**0.7
    Returns: A tuple of (weight_fit,Omega_fit,weight_error,Omega_error,res)
        weight_fit: returned fit of weights
        Omega_fit: returned fit of Omega
        weight_error: error of fitted weights
        Omega_error: error of fitted Omega
        res: retunred of fitleast_sq


    '''
    # weight=np.ones(max_n_fit)/max_n_fit

    upper_bounds = []
    lower_bounds = []
    if gamma_fixed==False:

        #Set up bounds

        if customized_bound_population==None:
            for i in range(max_n_fit):
                upper_bounds.append(1.0)
                lower_bounds.append(0.0)
        else:
            customized_upper_bounds = customized_bound_population[1]
            customized_lower_bounds = customized_bound_population[0]
            for i in range(max_n_fit):
                upper_bounds.append(customized_upper_bounds[i])
                lower_bounds.append(customized_lower_bounds[i])

        upper_bounds.append(Omega_0 * 1.05)
        upper_bounds.append(gamma * 1.2)

        lower_bounds.append(Omega_0 * 0.95)
        lower_bounds.append(gamma * 0.8)

        bounds = (lower_bounds, upper_bounds)

        p0 = np.concatenate((weights, Omega_0, gamma), axis=None)
        res = fit_leastsq(p0, t, y, None, sum_multi_sine, rsb, bounds=bounds)
        gamma_fit = res[0][-1]
        weight_fit = res[0][:max_n_fit]
        weight_fit[-1] = 1 - np.sum(weight_fit[:-1])
        Omega_fit = res[0][-2]
        weight_error = res[-1][:max_n_fit]
        Omega_error = res[-1][-2]
    else:
        # Set up bounds
        if customized_bound_population == None:
            for i in range(max_n_fit):
                upper_bounds.append(1.0)
                lower_bounds.append(0.0)
        else:
            customized_upper_bounds = customized_bound_population[1]
            customized_lower_bounds = customized_bound_population[0]
            for i in range(max_n_fit):
                upper_bounds.append(customized_upper_bounds[i])
                lower_bounds.append(customized_lower_bounds[i])

        upper_bounds.append(Omega_0 * 1.05)


        lower_bounds.append(Omega_0 * 0.95)

        bounds = (lower_bounds, upper_bounds)



        p0 = np.concatenate((weights, Omega_0), axis=None)
        res = fit_leastsq(p0, t, y, None, sum_multi_sine_fixed_gamma, (rsb, gamma), bounds=bounds)
        gamma_fit = gamma
        weight_fit = res[0][:max_n_fit]
        weight_fit[-1] = 1 - np.sum(weight_fit[:-1])
        Omega_fit = res[0][-1]
        weight_error = res[-1][:max_n_fit]
        Omega_error = res[-1][-1]
    print('upper_bounds is ', upper_bounds)
    print('lower_bounds is ', lower_bounds)
    print('Omega fit ', np.round(Omega_fit, 3))
    print('gamma fit ', gamma_fit)
    print('Error Omega', np.round(Omega_error,3))
    print('Pi time fit', np.round(np.pi / Omega_fit,3))
    print('Weights', np.round(weight_fit, 3))
    print('Errors of weights', np.round(weight_error, 3))

    return (weight_fit, Omega_fit, weight_error, Omega_error, gamma_fit, res)

def fit_sum_multi_sine_offset(t, y, max_n_fit, weights, Omega_0, gamma,offset=0.0,\
                                   rsb=True,gamma_fixed=False,\
                       customized_bound_population=None):
    '''
    Fitting of a data to a sum of weighted sine functions
    The angular frequencies of the sine functions is initialied to be a sqrt of geometric serires of Omega_0
    The weights are initialized to be a uniform normalized set

    Arguments:

        t: x axis of data
        y: y axis of data
        max_n_fit: maximum number of the elements of the sum
        Omega_0: Nominal Angular freq
        gamma: exponential damping. Gamma_n=gamma*(n+1)**0.7
    Returns: A tuple of (weight_fit,Omega_fit,weight_error,Omega_error,res)
        weight_fit: returned fit of weights
        Omega_fit: returned fit of Omega
        weight_error: error of fitted weights
        Omega_error: error of fitted Omega
        res: retunred of fitleast_sq


    '''
    # weight=np.ones(max_n_fit)/max_n_fit


    upper_bounds = []
    lower_bounds = []
    if gamma_fixed==False:

        #Set up bounds

        if customized_bound_population==None:
            for i in range(max_n_fit):
                upper_bounds.append(1.0)
                lower_bounds.append(0.0)
        else:
            customized_upper_bounds = customized_bound_population[1]
            customized_lower_bounds = customized_bound_population[0]
            for i in range(max_n_fit):
                upper_bounds.append(customized_upper_bounds[i])
                lower_bounds.append(customized_lower_bounds[i])

        upper_bounds.append(Omega_0 * 1.05)
        upper_bounds.append(gamma * 1.2)

        lower_bounds.append(Omega_0 * 0.95)
        lower_bounds.append(gamma * 0.8)

        bounds = (lower_bounds, upper_bounds)

        p0 = np.concatenate((weights, Omega_0, gamma), axis=None)
        res = fit_leastsq(p0, t, y, None, sum_multi_sine_offset, [offset,rsb], bounds=bounds)
        gamma_fit = res[0][-1]
        weight_fit = res[0][:max_n_fit]
        weight_fit[-1] = 1 - np.sum(weight_fit[:-1])
        Omega_fit = res[0][-2]
        weight_error = res[-1][:max_n_fit]
        Omega_error = res[-1][-2]
    else:
        # Set up bounds
        if customized_bound_population == None:
            for i in range(max_n_fit):
                upper_bounds.append(1.0)
                lower_bounds.append(0.0)
        else:
            customized_upper_bounds = customized_bound_population[1]
            customized_lower_bounds = customized_bound_population[0]
            for i in range(max_n_fit):
                upper_bounds.append(customized_upper_bounds[i])
                lower_bounds.append(customized_lower_bounds[i])

        upper_bounds.append(Omega_0 * 1.05)


        lower_bounds.append(Omega_0 * 0.95)

        bounds = (lower_bounds, upper_bounds)



        p0 = np.concatenate((weights, Omega_0), axis=None)
        res = fit_leastsq(p0, t, y, None, sum_multi_sine_offset, [offset,rsb], bounds=bounds)
        gamma_fit = gamma
        weight_fit = res[0][:max_n_fit]
        weight_fit[-1] = 1 - np.sum(weight_fit[:-1])
        Omega_fit = res[0][-1]
        weight_error = res[-1][:max_n_fit]
        Omega_error = res[-1][-1]
    print('upper_bounds is ', upper_bounds)
    print('lower_bounds is ', lower_bounds)
    print('Omega fit ', np.round(Omega_fit, 3))
    print('gamma fit ', gamma_fit)
    print('Error Omega', np.round(Omega_error,3))
    print('Pi time fit', np.round(np.pi / Omega_fit,3))
    print('Weights', np.round(weight_fit, 3))
    print('Errors of weights', np.round(weight_error, 3))

    return (weight_fit, Omega_fit, weight_error, Omega_error, gamma_fit, res)

def generate_weight(numfit, targetmode, target_height):
    weights = np.zeros((numfit,))
    for i in range(numfit):
        weights[i] = (1 - target_height) / (numfit - 1)
    weights[targetmode] = target_height

    return weights

def fit_leastsq(p0, x, y, yerr, function, arg1, bounds=(-np.inf, np.inf)):
    """
    Perform leastsq fit with an input function that accepts input as (x,p,arg1),
    where x is the input data, p is the fitting parameters and arg1 is the fixed
    parameters

    Argument:
    p0 -- fitting parameters
    x --  xdata
    y --  ydata
    yerr -- uncertainty of ydata
    function -- function for fitting  (x,p,arg1)
    arg1 -- argument for function

    Returns:
    A tuple of (pfit, pcov,redchi,perr)

    pfit: fitting result from curve_fit
    pcov: covariance matrix from curve fit
    redchi: calculated reduced chi square
    perr: error of fitting parameters

    """
    func_fit = lambda x, *p: function(x, p, arg1)  # *p to accept
    N = len(x)  # number of data points
    n = len(p0)  # number of fitting parameters

    if type(yerr) == type(x):

        pfit, pcov = curve_fit(func_fit, x, y, p0, sigma=yerr, bounds=bounds)

    else:
        # fit with no errors of y,not good!
        # print("No yerr")
        yerr = np.ones(np.shape(x))
        pfit, pcov = curve_fit(func_fit, x, y, p0, bounds=bounds)
    perr = []
    for i in range(len(pfit)):
        try:
            perr.append(np.absolute(pcov[i][i]) ** 0.5)
        except:
            # if pcov[i][i] is inf, ignore and forcefully take it as 1E7. not good!
            perr.append(1E3)

    # Calculation of reduce chi square
    # a simple way: Residual variance = reduced chi square = s_sq = sum[(f(x)-y)^2]/(N-n),
    # where N is number of data points and n is the number of fitting parameters

    yfit = function(x, pfit, arg1)
    temp = ((y - yfit) ** 2)
    redchi = np.sum(temp / yerr ** 2) / (N - n)
    # print(np.sum(y**2/yerr**2)/(N-n)    )
    perr = np.sqrt(np.diag(pcov))
    return pfit, pcov, redchi, perr

if __name__=="__main__":
    #from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    from read_data_func import *
    #tar_path='../test_data/r1op bsb delay scan after sbc'
    tar_path = '../test_data/psi_g tomo state 4 phase_correction 130'
    x,y,_,_,_=get_x_y(tar_path)
    max_n_fit=3
    weights=[0.012 ,0.981, 0.007]
    Omega_0=0.046
    gamma=1E-4
    offset=0.15
    rsb = True
    res = fit_sum_multi_sine_offset_deve(x, y, max_n_fit, weights, Omega_0, gamma, offset=offset, rsb=True,\
                                         gamma_fixed=False, \
                                   customized_bound_population=None)
    xfit = np.linspace(np.min(x), np.max(x), np.size(x) * 10)

    fit_weights = res[0]
    Omega_fit=res[1]
    gamma_fit=res[-2]
    yfit = sum_multi_sine_offset(xfit,np.concatenate((fit_weights, Omega_fit, gamma_fit),\
                                                     axis=None), [offset,rsb])
    #print(y)
    plt.plot(x,y)
    plt.plot(xfit,yfit)

    '''
    res2=fit_sum_multi_sine(x, y, max_n_fit, weights, Omega_0, gamma, rsb=rsb,\
                                         gamma_fixed=False, \
                                   customized_bound_population=None)
    print(res2)
    fit_weights2 = res2[0]
    Omega_fit2 = res2[1]
    gamma_fit2 = res2[-2]
    yfit2 = sum_multi_sine(xfit, np.concatenate(([0.012 ,0.981, 0.007], 0.046, gamma_fit2), \
                                                      axis=None), rsb)
    yfit3=sum_multi_sine(xfit, np.concatenate(([0.012 ,0.981, 0.007], res2[1],res2[-2]),\
                                        axis=None), rsb)
    #plt.plot(xfit, yfit2)
    plt.plot(xfit, yfit3)
    '''
    plt.show()