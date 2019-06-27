import numpy as np
from tools.derivatives import derivatives
from tools.misc import _all, _any


class R_EGA():
    """
        The Rate-Error Grid Analysis (P-EGA) gives an estimation of the clinical acceptability of the glucose
        predictions based on their rate-of-change-accuracy (the accuracy of the predicted variations).
        Every prediction is given a mark from {"A", "B", "uC", "lC", "uD", "lD", "uE", "lE"}

        The implementation is taken from "Evaluating the accuracy of continuous glucose-monitoring sensors: continuous
        glucose-error grid analysis illustrated by TheraSense Freestyle Navigator data.", Kovatchev et al., 2004.
    """

    def __init__(self, y_true, y_pred, freq):
        """
        Instantiate the P-EGA object.
        :param y_true: ground truth of shape (1,-1)
        :param y_pred: predictions of shape (1, -1)
        :param freq: prediction frequency in minutes (e.g., 5)
        """

        self.freq = freq
        self.dy_true, self.y_true = derivatives(y_true, self.freq)
        self.dy_pred, self.y_pred = derivatives(y_pred, self.freq)

    def full(self):
        """
            Full version of the R-EGA, which consists of an array giving for every prediction (row), its mark vector
            (column). There are 8 columns representing the mark A, B, uC, lC, uD, lD, uE, and lE.

            :return: numy array of shape (number of predictions, 8)
        """
        y_true, dy_true, y_pred, dy_pred = self.y_true, self.dy_true, self.y_pred, self.dy_pred

        A = _any([
            _all([  # upper and lower
                np.greater_equal(dy_pred, dy_true - 1),
                np.less_equal(dy_pred, dy_true + 1)
            ]),
            _all([  # left
                np.less_equal(dy_pred, dy_true / 2),
                np.greater_equal(dy_pred, dy_true * 2)
            ]),
            _all([  # right
                np.less_equal(dy_pred, dy_true * 2),
                np.greater_equal(dy_pred, dy_true / 2)
            ])
        ])

        B = _all([
            np.equal(A, False),  # not in A but satisfies the cond below
            _any([
                _all([
                    np.less_equal(dy_pred, -1),
                    np.less_equal(dy_true, -1)
                ]),
                _all([
                    np.less_equal(dy_pred, dy_true + 2),
                    np.greater_equal(dy_pred, dy_true - 2)
                ]),
                _all([
                    np.greater_equal(dy_pred, 1),
                    np.greater_equal(dy_true, 1)
                ])
            ])
        ])

        uC = _all([
            np.less(dy_true, 1),
            np.greater_equal(dy_true, -1),
            np.greater(dy_pred, dy_true + 2)
        ])

        lC = _all([
            np.less_equal(dy_true, 1),
            np.greater(dy_true, -1),
            np.less(dy_pred, dy_true - 2)
        ])

        uD = _all([
            np.less_equal(dy_pred, 1),
            np.greater_equal(dy_pred, -1),
            np.greater(dy_pred, dy_true + 2)
        ])

        lD = _all([
            np.less_equal(dy_pred, 1),
            np.greater_equal(dy_pred, -1),
            np.less(dy_pred, dy_true - 2)
        ])

        uE = _all([
            np.greater(dy_pred, 1),
            np.less(dy_true, -1)
        ])

        lE = _all([
            np.less(dy_pred, -1),
            np.greater(dy_true, 1)
        ])

        return np.concatenate([A, B, uC, lC, uD, lD, uE, lE], axis=1)
