import nltk
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

import SOC_PMI_Short_Text_Similarity.try1 as try1
import SOC_PMI_Short_Text_Similarity.wn3 as wn3
import SOC_PMI_Short_Text_Similarity.wordSim as wordSim


def soc_similarity(S1, S2):
    tokenizer = RegexpTokenizer(r'\w+')
    S1 = tokenizer.tokenize(S1)
    S2 = tokenizer.tokenize(S2)

    ltz = WordNetLemmatizer()
    S1 = [ltz.lemmatize(word.lower()) for word in S1]
    S2 = [ltz.lemmatize(word.lower()) for word in S2]

    eng_stopwords = nltk.corpus.stopwords.words('english')
    S1_filtered = [word for word in S1 if word not in eng_stopwords]
    S2_filtered = [word for word in S2 if word not in eng_stopwords]

    score, common = wordSim.wordSim(S1_filtered, S2_filtered)
    S1_next = [word for word in S1_filtered if word not in common]
    S2_next = [word for word in S2_filtered if word not in common]

    h, w = len(S1_next), len(S2_next)

    Matrix1 = try1.matrix_of_lists(h, w)

    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix1[i][j] = try1.calling(S1_next[i], S2_next[j])

    Matrix2 = try1.matrix_of_lists(h, w)

    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix2[i][j] = wn3.returnWordSim(S1_next[i], S2_next[j])

    Matrix = try1.matrix_of_lists(h, w)
    # print("Final Matrix")
    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix[i][j] = (0.5 * Matrix1[i][j]) + (0.5 * Matrix2[i][j])

    def delete(matrix, i_in, j_in):
        for row in matrix:
            del row[j_in]
        matrix = [matrix[i1] for i1 in range(len(matrix)) if i1 != i_in]
        return matrix

    Pi = []
    while len(Matrix) > 0 and len(Matrix[-1]) > 0:
        # Search for maximum Element
        maxelement = 0
        maxi, maxj = 0, 0
        for i in range(len(Matrix)):
            for j in range(len(Matrix[i])):
                if Matrix[i][j] > maxelement:
                    maxelement = Matrix[i][j]
                    maxi = i
                    maxj = j
        Pi.append(Matrix[maxi][maxj])
        Matrix = delete(Matrix, maxi, maxj)

    Delta = 2.0
    try:
        similarity = ((Delta + sum(Pi)) * (len(S1_next) + len(S2_next))) / (2 * len(S1_next) * len(S2_next))
    except ZeroDivisionError:
        similarity = 0

    return similarity
