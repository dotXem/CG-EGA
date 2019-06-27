import numpy as np
from cg_ega import CG_EGA


def main():
    y_true, y_pred = np.load("example.npy")
    freq = 5

    cg_ega = CG_EGA(y_true, y_pred, freq)
    print("AP, BE, EP:", cg_ega.reduced())
    cg_ega.plot(day=0)


if __name__ == "__main__":
    main()
