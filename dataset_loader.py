# this file loads the dataset STSS-131
# It will be imported by the validator script
# import in other files with
# "from dataset_loader import get_dataset"

import pandas as pd

_stss_131 = None


def get_dataset():
    global _stss_131

    if _stss_131 is None:
        _stss_131 = pd.read_csv("stss-131.csv", sep=';')

    return _stss_131
