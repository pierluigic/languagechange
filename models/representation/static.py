from .representation import StaticModel


class PPMI(StaticModel):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass


class SVD(StaticModel):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass


class RandomIndexing(StaticModel):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass