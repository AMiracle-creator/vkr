import pandas as pd


def read_dataset(path):
    dataset = pd.read_csv(path, delimiter=',')
    # dataset = dataset.head(5)
    # dataset = dataset.values.tolist()

    return dataset