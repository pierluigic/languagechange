import subprocess
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Union
from languagechange.usages import TargetUsage
from languagechange.corpora import LinebyLineCorpus
from LSCDetection.modules.utils_ import Space
import os
env = os.environ.copy()

class RepresentationModel(ABC):

    @abstractmethod
    def encode(self, *args, **kwargs):
        pass

# todo
class StaticModel(RepresentationModel, dict):

    def __init__(self, matrix_path=None, format='w2v'):
        self.space = None
        self.matrix_path = matrix_path
        self.format = format

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def load(self):
        self.space = Space(self.matrix_path, format=self.format)


    def __getitem__(self, k):
        if self.space == None:
            raise Exception('Space is not loaded')
        return self.space.matrix[self.space.row2id[k]].todense()

    def matrix(self):
        if self.space == None:
            raise Exception('Space is not loaded')
        return self.space.matrix

    def row2word(self):
        if self.space == None:
            raise Exception('Space is not loaded')
        return self.space.id2row

class CountModel(StaticModel):

    def __init__(self, corpus:LinebyLineCorpus, window_size:int, savepath:str):
        super(CountModel,self).__init__()
        self.corpus = corpus
        self.window_size = window_size
        self.savepath = savepath
        self.format = 'npz'
        self.matrix_path = os.path.join(self.savepath)

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.count", self.corpus.path, self.savepath, str(self.window_size)])


class PPMI(CountModel):

    def __init__(self, count_model:CountModel, shifting_parameter:int, smoothing_parameter:int, savepath:str):
        super(PPMI,self).__init__(self,count_model.window_size, count_model.savepath)
        self.count_model = count_model
        self.shifting_parameter = shifting_parameter
        self.smoothing_parameter = smoothing_parameter
        self.savepath = savepath
        self.matrix_path = os.path.join(self.savepath)
        self.align_strategies = {'OP', 'SRV', 'WI'}

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.ppmi", self.count_model.matrix_path, self.savepath, str(self.shifting_parameter), str(self.smoothing_parameter)])

class SVD(StaticModel):

    def __init__(self, count_model:CountModel, dimensionality:int, gamma:float, savepath:str):
        super(SVD,self).__init__()
        self.count_model = count_model
        self.dimensionality = dimensionality
        self.gamma = gamma
        self.savepath = savepath
        self.matrix_path = os.path.join(self.savepath)
        self.format = 'w2v'
        self.align_strategies = {'OP', 'SRV', 'WI'}

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.svd", self.count_model.matrix_path, self.savepath, str(self.dimensionality), str(self.gamma)])


class RandomIndexing(StaticModel):

    def __init__(self):
        super(RandomIndexing,self).__init__()
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.ri", corpus.path, self.savepath, self.window_size])


