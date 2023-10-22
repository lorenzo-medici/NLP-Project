# This file contains big preprocessing functions needed by the similarity
#   calculators, or common preprocessing steps between methods
import nltk
import spacy
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

try:
    nltk.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')

if not spacy.util.is_package('en_core_web_sm'):
    print('need download')
    spacy.cli.download('en_core_web_sm')

nlp = spacy.load("en_core_web_sm")


# computes word similarity between most common synset of each word
def word_similarity(w1, w2):
    S1 = wordnet.synsets(w1)
    S2 = wordnet.synsets(w2)
    if len(S1) > 0 and len(S2) > 0:
        similarity = S1[0].wup_similarity(S2[0])
        if similarity:
            return round(similarity, 2)
    return 0


# Call it on a sentence to tokenize it and remove stopwords
# You can use the additional parameter to perform lemmization using wordnet
# return_word_tag_type is used to return a list of tuples with (word, pos_tag). pos_tag is
#   a simplified subset contained in tag_dict. You can use comparisons such as "== wordnet.NOUN"
#   on this field
# spacy_named_entities_removal is used to remove named entities (ex: New York, UK) from sentence
def preprocess_sentence(sentence, wordnet_lemmization=False, return_word_tag_type=False,
                        spacy_named_entities_removal=False):
    eng_stopwords = nltk.corpus.stopwords.words('english')

    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    if spacy_named_entities_removal:
        doc = nlp(sentence)
        sentence = ' '.join([ent.text for ent in doc if not ent.ent_type_])

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


def get_hypernyms(token):
    syns = wordnet.synsets(token)

    if syns:
        hypers = syns[0].hypernyms()
    else:
        hypers = []

    return set(hypers)


def get_hyponyms(token):
    syns = wordnet.synsets(token)

    if syns:
        hypos = syns[0].hyponyms()
    else:
        hypos = []

    return set(hypos)
