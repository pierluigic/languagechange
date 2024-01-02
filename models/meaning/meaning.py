import subprocess
import WordTransformer

class MeaningModel():

    def __init__(self):
        pass

    def embeddings(self):
        pass


class StaticEmbedding(MeaningModel):

    def __init__(self):
        pass

    def embeddings(self):
        subprocess.run(["python", "other.py"])


    def apply_weight_schema(self, strategy=None):
        if strategy == None:
            raise "You have to define a reduce strategy."
        elif strategy == 'PPMI':
            subprocess.run(["python", "other.py"])
        else:
            raise "Reduce strategy not available. Available reduce strategies are: PPMI."

    def reduce(self, strategy=None):
        if strategy == None:
            raise "You have to define a reduce strategy."
        elif strategy == 'SVD':
            subprocess.run(["python", "other.py"])
        else:
            raise "Reduce strategy not available. Available reduce strategies are: SVD."


    def align(self, strategy=None):
        if strategy == None:
            raise "You have to define a reduce strategy."
        elif strategy == 'SVD':
            subprocess.run(["python", "other.py"])
        else:
            raise "Reduce strategy not available. Available reduce strategies are: SVD."


class CountModel(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass


class PPMI(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass

class SVD(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass

class SGNS(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass


class RandomIndexing(StaticEmbedding):

    def __init__(self):
        self.align_strategies = {'OP','SRV','WI'}
        pass


class ContextualizedEmbedding(MeaningModel):

    def __init__(self):
        pass


class XL_LEXEME(ContextualizedEmbedding):

    def __init__(self):
        pass

    def embeddings(self, ):
        