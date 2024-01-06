from scipy.spatial.distance import cdist, cosine
import numpy as np

class ChangeModel():

    def __init__(self):
        pass


class BinaryChange(ChangeModel):

    def __init__(self):
        pass

    def predict(self):
        pass


class GradedChange(ChangeModel):

    def __init__(self):
        pass

    def compute_scores(vectors_list):
        pass


class Threshold(BinaryChange):

    def __init__(self):
        pass

    def set_threshold(self, threshold):
        self.threshold = threshold


class AutomaticThrehold(Threshold):

    def __init__(self):
        pass

    def compute_threshold(self, scores, func = lambda x: np.mean(x)):
        self.threshold = func(scores)


class OptimalThrehold(Threshold):

    def __init__(self):
        pass

    def compute_threshold(self, scores, vrange=np.arange(0.,1.), evaluator=None):
        best_score = None
        best_threshold = None

        for v in vrange:
            labels = np.array(scores < v, dtype=int)
            score = evaluator(labels)
            if score > best_score or best_score == None:
                best_score = score
                best_threshold = v

        self.threshold = best_threshold


class APD(GradedChange):

    def __init__(self):
        pass

    def compute_scores(embeddings1, embeddings2, metric='cosine'):

        return np.mean(cdist(embeddings1, embeddings2, metric=metric))


class PRT(GradedChange):

    def __init__(self):
        pass

    def compute_scores(embeddings1, embeddings2, metric='cosine'):

        return cosine(embeddings1.mean(axis=0), embeddings2.mean(axis=0))


class PJSD(GradedChange):

    def __init__(self):
        pass

    def compute_scores(embeddings1, embeddings2, metric='cosine'):
        pass


class WIDID(GradedChange):

    def __init__(self):
        pass

    def compute_scores(embeddings1, embeddings2, metric='cosine'):
        pass