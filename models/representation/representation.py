import subprocess
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Union
from languagechange.usages import TargetUsage

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
class StaticEmbedding(RepresentationModel, ABC):

    @abstractmethod
    def encode(self):
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

# todo
class CountModel(RepresentationModel):

    def __init__(self):
        pass