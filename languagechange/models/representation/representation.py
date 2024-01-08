import subprocess
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Union
from languagechange.usages import TargetUsage
from languagechange.corpora import LinebyLineCorpus


class RepresentationModel(ABC):

    @abstractmethod
    def encode(self, *args, **kwargs):
        pass

class ContextualizedEmbedding(RepresentationModel, ABC):

    @abstractmethod
    def __init__(self,
                 device: str = 'cuda',
                 n_extra_tokens: int = 0,
                 *args, **kwargs):

        if not device in ['cuda', 'cpu']:
            raise ValueError("Device must be in ['cuda', 'cpu']")
        if not isinstance(n_extra_tokens, int):
            raise ValueError("batch_size must be an integer")

        self._n_extra_tokens = n_extra_tokens
        self._device = device

    @abstractmethod
    def encode(self, target_usages: Union[TargetUsage, List[TargetUsage]],
               batch_size: int = 8) -> np.array:

        if not isinstance(batch_size, int):
            raise ValueError("batch_size must be an integer")

        if not (isinstance(target_usages, TargetUsage) or isinstance(target_usages, list)):
            raise ValueError("target_usages must be Union[dict, List[dict]]")

# todo
class StaticModel(RepresentationModel, ABC):

    @abstractmethod
    def encode(self):
        pass


class CountModel(StaticModel):

    def __init__(self, corpus:LinebyLineCorpus, window_size:int, savepath:str):
        self.corpus = corpus
        self.window_size = window_size
        self.savepath = savepath
        self.matrix_path = os.path.join(self.savepath)

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.count", self.corpus.path, self.savepath, self.window_size])


class PPMI(StaticModel):

    def __init__(self, count_model:CountModel, shifting_parameter:int, smoothing_parameter:int, savepath:str)):
        self.count_model = count_model
        self.shifting_parameter = shifting_parameter
        self.smoothing_parameter = smoothing_parameter
        self.savepath = savepath
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass

    def encode(self):
        subprocess.run(["python3", "-m", "LSCDetection.representations.ppmi", self.count_model.matrix_path, self.shifting_parameter, self.smoothing_parameter])

class SVD(StaticModel):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass

    def encode(self, corpus: LinebyLineCorpus):
        subprocess.run(["python3", "-m", "LSCDetection.representations.svd", corpus.path, self.savepath, self.window_size])


class RandomIndexing(StaticModel):

    def __init__(self):
        self.align_strategies = {'OP', 'SRV', 'WI'}
        pass

    def encode(self, corpus: LinebyLineCorpus):
        subprocess.run(["python3", "-m", "LSCDetection.representations.ri", corpus.path, self.savepath, self.window_size])