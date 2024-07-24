import subprocess
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Union
from languagechange.usages import TargetUsage
from languagechange.corpora import LinebyLineCorpus
from LSCDetection.modules.utils_ import Space
from languagechange.models.representation.static import StaticModel
import os


class OrthogonalProcrustes():
    def __init__(self, savepath1:str, savepath2:str):
        self.savepath1 = savepath1
        self.savepath2 = savepath2


    def align(self, model1:StaticModel, model2:StaticModel):
        subprocess.run(["python3", "-m", "LSCDetection.alignment.map_embeddings", 
            "--normalize", "unit",
            "--init_identical",
            "--orthogonal",
            model1.matrix_path,
            model2.matrix_path,
            self.savepath1,
            self.savepath2])