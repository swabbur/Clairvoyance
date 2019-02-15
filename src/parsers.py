import pandas as pd
import scipy as sp


def from_csv(path):

    data_frame = pd.read_csv(path)
    data = data_frame.to_numpy()

    identifiers = data[:, 0]
    ratings = data[:, 1:].astype(sp.float64)

    return identifiers, ratings
