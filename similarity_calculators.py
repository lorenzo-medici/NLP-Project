# This file contains the functions that calculate the similarity
#   in the four different methods we need
# Eventual utility functions or common function between methods
#   should be placed in preprocess.py (unlikely that we'll need
#   to put something there)

# All methods get two strings as parameters, each method will take
#   care of the preprocessing (e.g. stopword removal, lemmatization)

from sklearn.feature_extraction.text import TfidfVectorizer

from SOC_PMI_Short_Text_Similarity.main import soc_similarity
from preprocess import word_similarity, preprocess_sentence, get_hypernyms_hyponyms


def method_1_wordnet(S1, S2):
    S1 = preprocess_sentence(S1, wordnet_lemmization=True)
    S2 = preprocess_sentence(S2, wordnet_lemmization=True)

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
    else:
        # happens when no word is found in the dictionary, so similarity
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
    else:
        # same reasoning used for S1
        Sim_score2 = 0

    Sim = (Sim_score1 + Sim_score2) / 2

    return round(Sim, 2)


def method_2_wupalmer(S1, S2):
    S1 = preprocess_sentence(S1, wordnet_lemmization=True, spacy_named_entities_removal = True)
    S2 = preprocess_sentence(S2, wordnet_lemmization=True, spacy_named_entities_removal = True)

    total_similarity = 0.0
    count = 0

    for noun1 in S1:
        for noun2 in S2:
            similarity = noun1.wup_similarity(noun2)
            if similarity is not None:
                total_similarity += similarity
                count += 1
    
    if count > 0:
        Sim = total_similarity / count
        return round(Sim,2)
    else:
        return 0.0

# work yet to be done: not sure what the final expression is
# but this functions takes nouns and verbs from both snetences
# gets their hyponyms and hypernyms and gets their union and intersection
# the max should be very simple to implement once i know what max am i looking for
def method_3_hypernyms(S1, S2):
    S1 = preprocess_sentence(S1, wordnet_lemmization=True, return_word_tag_type=True)
    S2 = preprocess_sentence(S2, wordnet_lemmization=True, return_word_tag_type=True)

    for noun1 in S1:       
        if noun1[1] == "N":
            hypernyms1, hyponyms1 = get_hypernyms_hyponyms(noun1)
            for noun2 in S2:
                if noun2[1] == "N":
                    hypernyms2, hyponyms2 = get_hypernyms_hyponyms(noun1)
                    hypernyms_union_length = len(hypernyms1.union(hypernyms2))
                    hypernyms_intersection_length = len(hypernyms1.intersection(hypernyms2))
                    value = hypernyms_intersection_length / hypernyms_union_length
        elif noun1[1] == "V":
            hypernyms1, hyponyms1 = get_hypernyms_hyponyms(noun1)
            for noun2 in S2:
                if noun2[1] == "V":
                    hypernyms2, hyponyms2 = get_hypernyms_hyponyms(noun1)
                    hypernyms_union_length = len(hyponyms1.union(hyponyms2))
                    hypernyms_intersection_length = len(hyponyms1.intersection(hyponyms2))
                    value = hypernyms_intersection_length / hypernyms_union_length
    return value


def method_4_library(S1, S2):
    return soc_similarity(S1, S2)
