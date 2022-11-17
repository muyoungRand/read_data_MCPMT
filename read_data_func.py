#!/usr/bin/python
from pylab import *
import csv
import ast
import numpy as np

def read_file(filename):
    """
    Returns:
    r -- raw data, shape of r (M,) where M is the number of scanning parameters.
    """
    with open(filename, 'rt') as file:
        d = [] # Scanned parameter
        h = [] # Histogram of counts -> Only works for SCPMT
        r = [] # Raw data
        t = [] # Time of experiment
        for row in csv.reader(file):
            data = []
            extra = []
            for item in row:
                try:
                    data.append(float(item)) # Scanned variable is a float
                except:
                    extra.append(ast.literal_eval(item)) # Other data are other python data types
            d.append(data)
            t.append(extra[0])
            h.append(extra[1])
            r.append(extra[2])

    return np.transpose(d), h, r, t


# Get timestamps from the first element of the timestamp list
# assumes that the data were scanned only once
def get_timestamps(timestamp):
    ts = []
    for time_list in timestamp:
        ts.append(time_list[0])
    return array(ts)


def get_nexp(pr):
    """
    Get number of experiments in experiment.
    Does so by counting how many 'a'/SCPMT measurements there are in the raw data.

    Also works for MCPMT, but better to leave as 'a' since SCPMT is always active regardless of MCPMT channel

    Args:
        pr: Raw data

    Returns:
        nexp (float): Number of experiments
    """
    nexp = []
    for item in pr:
        try:
            nexp.append(len(item['a'])) # Still works for MCPMT
        except KeyError:
            nexp.append(0)
    return nexp


def process_raw(raw):
    """
    Sorts raw data in terms of counters 'a', 'G5', 'G7', etc. and the associated raw counts per experiment

    Args:
        raw: Raw Data

    Returns:
        out: Dictionary of counter + raw counts
    """
    out = []
    for line in raw:
        d = dict()
        for key, val in line:
            try:
                d[key].append(val)
            except KeyError:
                d[key] = [val]
        out.append(d)
    return out


def get_x_y(filename, channels = [5, 7, 9]):
    """
    Find scanned variable (x) and thresholded results (y) from data file.
    NOTE: Does NOT work for multiple scanned variables.

    Args:
        filename (string): Path to data file
        channels (list, optional): MCPMT Channels to read from. Defaults to [5, 7, 9].

    Returns:
        (x, y, err_y): Scanned variable, thresholded result and calculated errors
    """
    data, hist, raw, timestamp = read_file(filename)

    raw = process_raw(raw)
    nexp = get_nexp(raw)

    x = data[0]  # x axis,

    # Extract threshold data
    y1 = data[3]  # SCPMT Counter 1
    
    y2_rev = []
    for i in channels:
        y2_rev.append(data[i + 27]) # MCPMT CH7 = Data 34

    # Calculate Errors
    nexp = nexp[0]
    err1 = sqrt(y1 * (1.0 - y1) / nexp)

    err2_rev = []
    for i in y2_rev:
        errr = sqrt(i * (1.0 - i) / nexp)
        err2_rev.append(errr)
   
    # Flip order.
    # MainWin saves STOP point as first data point, so flip to make START the first data point
    x = x[::-1]
    y1 = y1[::-1]
    err1 = err1[::-1]
    
    y2 = []
    err2 = []
    for i in y2_rev:
        y2.append(i[::-1])
    for j in err2_rev:
        err2.append(j[::-1])

    return (x, y1, err1, y2, err2)


def get_x_y_raw(filename, channel='a', bins=50, maxbin=50, density=True):
    """
    Retrieve true counts from the processed raw data
    NOTE: NOT fixed for MCPMT yet. Left for future work.

    Arguments:
    filename -- data file
    channel --  counter
    bins -- number of histogram bins
    maxbin -- maximum range of histogram
    density -- if true, h is a probability density function at the bins.

    Returns:
    x -- experimental scanning varaibles
    y -- mean of measurement results
    err -- std of y
    hbins -- bin edges
    h -- histogram of y
    hsum -- sum of histogram of y
    """

    data, hist, raw, timestamp = read_file(filename)
    print(raw)
    print(data)
    raw = process_raw(raw)
    print(raw)
    nexp = get_nexp(raw)
    x=[]
    #x = data[0]

    # x = x[::-1]
    y = []
    err = []
    h = []
    for row in raw:
        temp = row[channel]
        y.append(np.mean(temp))
        err.append(np.std(temp) / np.sqrt(nexp))
        h1, hbins = np.histogram(temp, bins, (0, maxbin), density=density)
        h.append(h1)
    hsum = np.stack(h, axis=0)
    hsum = np.sum(hsum, axis=0)
    return (x, y, err, hbins, h, hsum)

if __name__=="__main__":
    main()
