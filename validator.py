# This file contains the validation steps. It will import the dataset
#   and use the four similarity methods on each pair of sentences
#   outputting the Pearson coefficient for each method
# It will use both the dataset loader and the similarity function files

from scipy.stats import pearsonr

from dataset_loader import get_dataset
from similarity_calculators import *


def validator():
    ds = get_dataset()
    human_scores = ds["X"]

    methods = [method_1_wordnet, method_2_wupalmer, method_3_hypernyms, method_4_library]

    for m in methods:
        m_scores = [m(row['Sentence1'], row['Sentence2']) for i, row in ds.iterrows()]

        corr, _ = pearsonr(m_scores, human_scores)

        print(f"Method {methods.index(m) + 1}:\nPearson coefficient: {corr:.6f}\n")


if __name__ == "__main__":
    validator()
