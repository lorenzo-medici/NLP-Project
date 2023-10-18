# This file contains the functions that calculate the similarity
#   in the four different methods we need
# Eventual utility functions or common function between methods
#   should be placed in preprocess.py (unlikely that we'll need
#   to put something there)

# All methods get two list of tokens as parameters, with all necessary
#   preprocessing (e.g. stopwords, lemmization, ect.) already done

from sklearn.feature_extraction.text import TfidfVectorizer

from SOC_PMI_Short_Text_Similarity.main import soc_similarity
from preprocess import word_similarity


def method_1_wordnet(S1, S2):
    tf = TfidfVectorizer(use_idf=True)
    tf.fit_transform([' '.join(S1), ' '.join(S2)])

    Idf = dict(zip(tf.get_feature_names_out(), tf.idf_))

    Sim_score1 = 0
    Sim_score2 = 0

    for w1 in S1:
        Max = 0
        for w2 in S2:
            score = word_similarity(w1, w2)
            Max = max(Max, score)

        Sim_score1 += Max * Idf.get(w1, 0)

    w1_idf_sum = sum([Idf.get(w1, 0) for w1 in S1])
    if w1_idf_sum != 0:
        Sim_score1 /= w1_idf_sum
    else:  # happens when no word is found in the dictionary, so similarity
        # is at best very low and at worst completely useless
        Sim_score1 = 0

    for w2 in S2:
        Max = 0
        for w1 in S1:
            score = word_similarity(w1, w2)
            Max = max(Max, score)
        Sim_score2 += Max * Idf.get(w2, 0)

    w2_idf_sum = sum([Idf.get(w2, 0) for w2 in S2])
    if w2_idf_sum != 0:
        Sim_score2 /= w2_idf_sum
    else:  # same reasoning used for s1q
        Sim_score2 = 0

    Sim = (Sim_score1 + Sim_score2) / 2

    return round(Sim, 2)


def method_4_library(S1, S2):
    return soc_similarity(S1, S2)
