from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

import try1
import wn3
import wordSim


def soc_similarity(S1, S2):
    tokenizer = RegexpTokenizer(r'\w+')
    S1 = tokenizer.tokenize(S1)
    S2 = tokenizer.tokenize(S2)

    ltz = WordNetLemmatizer()
    S1 = [ltz.lemmatize(word.lower()) for word in S1]
    S2 = [ltz.lemmatize(word.lower()) for word in S2]

    # print(S1, S2
    # tokenizer = RegexpTokenizer(r'\w+')
    # S1 = tokenizer.tokenize(S1)
    # S2 = tokenizer.tokenize(S2)
    S1_filtered = [word for word in S1 if word not in stopwords.words('english')]
    S2_filtered = [word for word in S2 if word not in stopwords.words('english')]
    # print(S1, S2)
    # End of Step 1

    # Start of Step 2
    score, common = wordSim.wordSim(S1_filtered, S2_filtered)
    S1_next = [word for word in S1_filtered if word not in common]
    S2_next = [word for word in S2_filtered if word not in common]
    # print("Common", common)
    # print("Paragraph", S1_next, S2_next)
    h, w = len(S1_next), len(S2_next)
    # Matrix1 = [[0.0 for x in range(w)] for x in range(h)]
    Matrix1 = try1.matrix_of_lists(h, w)
    # print(S2_next)
    for i in range(len(Matrix1)):
        pass
        # print(S1_next[i], Matrix1[i])
    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix1[i][j] = try1.calling(S1_next[i], S2_next[j])
    # print(S2_next)
    for i in range(len(Matrix1)):
        pass
        # print(S1_next[i], Matrix1[i])
    # End of Step 3

    # Begining of Step 4
    # Matrix2 = [[0.0 for x in range(w)] for x in range(h)]
    Matrix2 = try1.matrix_of_lists(h, w)
    # print("SOCPMI")
    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix2[i][j] = wn3.returnWordSim(S1_next[i], S2_next[j])
    # print(S2_next)
    for i in range(len(Matrix2)):
        pass
        # print(S1_next[i], Matrix2[i])
    # End of Step 4

    # Begining of Step 5
    # Matrix = [[0.0 for x in range(w)] for x in range(h)]
    Matrix = try1.matrix_of_lists(h, w)
    # print("Final Matrix")
    for i in range(len(S1_next)):
        for j in range(len(S2_next)):
            Matrix[i][j] = (0.5 * Matrix1[i][j]) + (0.5 * Matrix2[i][j])
    # print(S2_next)
    for i in range(len(Matrix)):
        pass
        # print(S1_next[i], Matrix[i])
        # Looping to find Pi

    def delete(matrix, i_in, j_in):
        for row in matrix:
            del row[j_in]
        matrix = [matrix[i1] for i1 in range(len(matrix)) if i1 != i_in]
        return matrix

    i = 0
    Pi = []
    while len(Matrix) > 0 and len(Matrix[i]) > 0:
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
        # print("Matrix")
        for i in range(len(Matrix)):
            pass
            # print(Matrix[i])
        # print("Pi", Pi)

    # End of Step 5

    # Begining of Step 6
    Delta = 2.0
    try:
        similarity = ((Delta + sum(Pi)) * (len(S1_next) + len(S2_next))) / (2 * len(S1_next) * len(S2_next))
    except ZeroDivisionError:
        similarity = 0
    # print("Similarity Score", similarity)

    return similarity
