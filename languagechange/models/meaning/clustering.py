import numpy as np
from typing import Tuple
from languagechange.models.representation.contextualized import ContextualizedEmbeddings


class ClusteringResults():
    def __init__(self, labels):
        self.cluster2instances = {}
        for j,l in enumerate(labels):
            if not l in self.cluster2instances:
                cluster2istances[l] = []
            self.cluster2instances[l].append(j)

    def get_cluster_instances(self, cluster_id):
        return self.cluster2instances[cluster_id]


class Clustering():
    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm

    def get_cluster_results(self, embeddings:np.array):
        self.labels = self.algorithm.fit_predict(embeddings)
        return ClusteringResults(self.labels)



class IncrementalClustering(Clustering):
    def fit(self, embs1: ContextualizedEmbeddings,
            embs2: ContextualizedEmbeddings) -> Tuple[ContextualizedEmbeddings,
                                                     ContextualizedEmbeddings]:
        # clustering separately
        self.algorithm.fit(embs1['embedding'])
        self.algorithm.fit(embs2['embedding'])

        return self.labels(embs1, embs2)
