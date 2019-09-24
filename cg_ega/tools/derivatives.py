import numpy as np

def derivatives(y, freq):
    """
    Compute the derivative of the signal y, (y[i] - y[i-1]) / (t[i] - t[i-1]).
    :param y: signal, either true or predicted glucose values;
    :return: the derivatives and its associated signal (every sample has a corresponding derivative)
    """
    dy = np.reshape(np.diff(y, axis=1), (-1, 1)) / freq
    y = np.reshape(y[:, 1:], (-1, 1))
    return dy, y