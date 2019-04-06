#!/usr/bin/python
from pylab import *
import csv
import ast
import numpy as np
def read_file2(filename):
    """
    Returns:
    r -- raw data, shape of r (M,) where M is the number of scanning parameters.
    """
    with open(filename, 'rt') as file:
        d = []
        h = []
        r = []
        t = []
        for row in csv.reader(file):
            data = []
            extra = []
            for item in row:
                try:
                    data.append(float(item))
                except:
                    extra.append(ast.literal_eval(item))
            d.append(data)
            t.append(extra[0])
            h.append(extra[1])
            r.append(extra[2])

    #return array(map(list, map(None, *d))), h, r, t
    return np.transpose(d),h,r,t

def process_raw(raw):
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


# Get timestamps from the first element of the timestamp list
# assumes that the data were scanned only once
def get_timestamps(timestamp):
    ts = []
    for time_list in timestamp:
        ts.append(time_list[0])
    return array(ts)


def get_nexp(pr):
    nexp = []
    for item in pr:
        try:
            nexp.append(len(item['a']))
        except KeyError:
            nexp.append(0)
    return nexp


def process_raw(raw):
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


def get_x_y(filename):
    data, hist, raw, timestamp = read_file2(filename)
    timestamp = get_timestamps(timestamp)
    raw = process_raw(raw)
    nexp = get_nexp(raw)
    if len(data) == 20:  # We scan two parameters
        x = data[0]  # x axis
        y1 = data[4]  # counter 1
        y2 = data[6]  # counter 3
    else:  # we scan only one parameter
        x = data[0]  # x axis,
        y1 = data[3]  # counter 1
        y2 = data[5]  # counter 3
    # Counter 'a' mean is [12]
    # Counter 'b' mean is [13]
    # Counter 'c' mean is [14]
    print('nexp ',nexp)
    nexp=nexp[0]
    err1 = sqrt(y1 * (1.0 - y1) / nexp)
    err2 = sqrt(y2 * (1.0 - y2) / nexp)
    x = x[::-1]
    y1 = y1[::-1]
    err1 = err1[::-1]
    print('shape of x ', np.shape(x))
    print('x ',x)
    print('shape of y1 ',np.shape(y1))
    print('y1 ', y1)
    return (x, y1, err1, y2, err2)


def get_x_y_raw(filename, channel='a', bins=50, maxbin=50, density=True):
    """
    Retrieve true counts from the processed raw data

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

    data, hist, raw, timestamp = read_file2(filename)
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
