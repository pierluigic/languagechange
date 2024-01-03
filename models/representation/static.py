from .representation import StaticEmbedding

class PPMI(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass


class SVD(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass


class RandomIndexing(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass