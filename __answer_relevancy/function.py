import numpy as np

def npsumdot(x, y):
    return np.sum(x*y, axis=1)

def npsumdot_3d(x, y):
    return np.sum(x*y, axis=2)

