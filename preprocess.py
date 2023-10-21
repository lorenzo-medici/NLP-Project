# This file contains big preprocessing functions needed by the similarity
#   calculators, or common preprocessing steps between methods
import spacy
import nltk
from nltk import WordNetLemmatizer
from nltk.tokenize import word_tokenize

try:
    nltk.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_sm")

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
# spacy_named_entities_removal is used to remove named entities (ex: New York, UK) from sentence
def preprocess_sentence(sentence, wordnet_lemmization=False, return_word_tag_type=False, spacy_named_entities_removal = False):
    eng_stopwords = nltk.corpus.stopwords.words('english')

    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    words = nltk.pos_tag(
        [word.lower() for word in word_tokenize(sentence) if word.isalpha() and word not in eng_stopwords])

    words = [(w[0], tag_dict.get(w[1][0].upper(), wordnet.NOUN)) for w in words]

    if spacy_named_entities_removal:
        doc = nlp(sentence)
        words = [ent.text for ent in doc if not ent.ent_type_]
    
    if wordnet_lemmization:
        wnl = WordNetLemmatizer()
        words = [(wnl.lemmatize(w[0], pos=w[1]), w[1]) for w in words]

    if return_word_tag_type:
        return words
    

    else:
        return [w[0] for w in words]

#function simply returns sets hyponyms and hypernyms of set token
def get_hypernyms_hyponyms(token):
    hypernyms = set()
    hyponyms = set()
    synsets = wordnet.synsets(token.text)
    for synset in synsets:
        for hypernym in synset.hypernyms():
            hypernyms.add(hypernym)
        for hyponym in synset.hyponyms():
            hyponyms.add(hyponym)
    
    return hypernyms, hyponyms