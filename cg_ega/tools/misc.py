import numpy as np

def _any(l, axis=1):
    return np.reshape(np.any(np.concatenate(l, axis=axis), axis=axis), (-1, 1))


def _all(l, axis=1):
    return np.reshape(np.all(np.concatenate(l, axis=axis), axis=axis), (-1, 1))