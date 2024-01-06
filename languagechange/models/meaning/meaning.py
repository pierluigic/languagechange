from abc import ABC

class MeaningModel(ABC):

    def __init__(self):
        pass

class WordSenseInduction(MeaningModel):
    pass

# todo
class SGNS(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass