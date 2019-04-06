import numpy as np

def sin_fit(x, p, arg1):
    [a, b, c] = p
    [d, e] = arg1
    return a * np.sin(b * x + c)