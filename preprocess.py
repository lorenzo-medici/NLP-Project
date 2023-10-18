# This file contains big preprocessing functions needed by the similarity
#   calculators, or common preprocessing steps between methods
import nltk
from nltk import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('stopwords')

from nltk.corpus import wordnet


def word_similarity(P, R):
    if len(R) > len(P):
        P, R = R, P
    common = {}
    count = 1
    for i in P:
        if i in R:
            common.setdefault(i, [])
            common[i].append(count)
            count += 1

    # print common, P
    count = 1
    for i in R:
        if i in common:
            common[i].append(count)
            count += 1
    # print common, P
    sumi = 0.0
    for i in common:
        sumi += abs(common[i][0] - common[i][1])
    # print sumi
    # Calculating Similiarity
    if len(common) == 0:
        return 0
    try:
        if len(common) % 2 == 0:
            return 1 - (2 * sumi / float(len(common) ** 2))
        elif len(common) % 2 != 0 and len(common) > 1:
            return 1 - (2 * sumi / (float(len(common) ** 2) - 1))
        elif len(common) % 2 != 0 and len(common) == 1:
            return 1
    except ZeroDivisionError:
        return 0


# Call it on a sentence to tokenize it and remove stopwords
# You can use the additional parameter to perform lemmization using wordnet
# return_word_tag_type is used to return a list of tuples with (word, pos_tag). pos_tag is
#   a simplified subset contained in tag_dict. You can use comparisons such as "== wordnet.NOUN"
#   on this field
def preprocess_sentence(sentence, wordnet_lemmization=False, return_word_tag_type=False):
    eng_stopwords = nltk.corpus.stopwords.words('english')

    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    words = nltk.pos_tag(
        [word.lower() for word in word_tokenize(sentence) if word.isalpha() and word not in eng_stopwords])

    words = [(w[0], tag_dict.get(w[1][0].upper(), wordnet.NOUN)) for w in words]

    if wordnet_lemmization:
        wnl = WordNetLemmatizer()
        words = [(wnl.lemmatize(w[0], pos=w[1]), w[1]) for w in words]

    if return_word_tag_type:
        return words
    else:
        return [w[0] for w in words]
