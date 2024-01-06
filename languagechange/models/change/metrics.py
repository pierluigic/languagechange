import numpy as np
from languagechange.models.representation.contextualized import ContextualizedEmbeddings
from collections import Counter
from scipy.spatial.distance import cdist, cosine
from sklearn.metrics import DistanceMetric
from scipy.spatial.distance import jensenshannon

def apd(x: np.array, y:np.array, metric: str = 'cosine') -> float:
    return np.mean(cdist(x, y, metric=metric))

def APD(embs1: ContextualizedEmbeddings, embs2: ContextualizedEmbeddings, metric='cosine') -> float:
    return apd(cdist(embs1['embedding'], embs2['embedding'], metric=metric))

def DistanceBetweenWordPrototypes(embs1: ContextualizedEmbeddings, embs2: ContextualizedEmbeddings, metric='cosine') -> float:
    dist = DistanceMetric.get_metric(metric)
    distances = dist.pairwise([embs1['embedding'].mean(axis=0)], [embs2['embedding'].mean(axis=0)])
    return distances[0, 0]


def check_clustering(func):
    def onCall(embs1, embs2):
        if not ('cluster' in embs1.column_names and 'cluster' in embs2.column_names):
            raise AssertionError("You need to perform clustering before")
        return func(embs1, embs2)
    return onCall

@check_clustering
def JensenShannonDivergence(embs1: ContextualizedEmbeddings, embs2: ContextualizedEmbeddings) -> float:
    labels = np.concatenate([embs1['label'], embs2['label']], axis=1)
    labels = np.unique(labels)

    # time-specific distributions
    p = Counter(embs1['label'])
    p = np.array([p[label] for label in labels]) / embs1.num_rows
    q = Counter(embs2['label'])
    q = np.array([q[label] for label in labels]) / embs2.num_rows

    return jensenshannon(p, q)

@check_clustering
def AveragePairwiseDistanceBetweenSensePrototypes(embs1: ContextualizedEmbeddings, embs2: ContextualizedEmbeddings, metric: str = 'canberra') -> float:
    # cluster centroids
    mu_embs1 = np.array([embs1['embedding'][embs1['label'] == label].mean(axis=0) for label in np.unique(embs1['label'])])
    mu_embs2 = np.array([embs2['embedding'][embs2['label'] == label].mean(axis=0) for label in np.unique(embs2['label'])])
    return apd(mu_embs1, mu_embs2, metric=metric)