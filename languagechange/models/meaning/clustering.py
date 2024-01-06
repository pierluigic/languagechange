import numpy as np
from typing import Tuple
from languagechange.models.meaning.meaning import WordSenseInduction
from languagechange.models.representation.contextualized import ContextualizedEmbeddings


class ClusteringAlgorithm:
    def fit(self, x: np.array):
        if not isinstance(x, np.ndarray):
            raise ValueError('x must be np.array')

        self.labels_ = None

class Clustering(WordSenseInduction):
    def __init__(self, algorithm: ClusteringAlgorithm):
        super().__init__()
        self.algorithm = algorithm

    def labels(self, embs1: ContextualizedEmbeddings,
               embs2: ContextualizedEmbeddings) -> Tuple[ContextualizedEmbeddings,
                                                     ContextualizedEmbeddings]:
        labels = self.algorithm.labels_

        # noinspection PyUnresolvedReferences
        lab1 = labels[:embs1['embedding'].shape[0]]
        if 'cluster' in embs1.column_names:
            embs1 = embs1.remove_columns(['cluster'])
        embs1 = embs1.add_column("cluster", lab1)

        lab2 = labels[embs1['embedding'].shape[0]:]
        if 'cluster' in embs2.column_names:
            embs2 = embs2.remove_columns(['cluster'])
        embs2 = embs2.add_column("cluster", lab2)

        return embs1, embs2

    def fit(self, embs1: ContextualizedEmbeddings,
            embs2: ContextualizedEmbeddings) -> Tuple[ContextualizedEmbeddings,
                                                     ContextualizedEmbeddings]:
        # clustering embeddings as a whole
        embeddings = np.concatenate([embs1['embedding'], embs2['embedding']], axis=0)

        self.algorithm.fit(embeddings)

        return self.labels(embs1, embs2)

class IncrementalClustering(Clustering):
    def fit(self, embs1: ContextualizedEmbeddings,
            embs2: ContextualizedEmbeddings) -> Tuple[ContextualizedEmbeddings,
                                                     ContextualizedEmbeddings]:
        # clustering separately
        self.algorithm.fit(embs1['embedding'])
        self.algorithm.fit(embs2['embedding'])

        return self.labels(embs1, embs2)