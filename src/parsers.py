import pandas as pd


def from_csv(path):

    data_frame = pd.read_csv(path)
    data = data_frame.to_numpy()

    identifiers = data[:, 0].astype(str)
    ratings = data[:, 1:].astype(float)

    return identifiers, ratings
