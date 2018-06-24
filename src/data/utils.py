from sklearn.preprocessing import normalize
import numpy as np


def display_scores(vectorizer, tfidf_result):
    datanormalized = (normalize(tfidf_result.sum(axis=0), norm='l1') * 100)

    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(datanormalized).ravel())

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    salida = [item[0] for item in sorted_scores if item[1] > 0]
    return salida[:7]
