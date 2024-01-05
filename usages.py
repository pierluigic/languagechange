import enum
import pickle
from pathlib import Path
import os


class POS(enum.Enum):
   NOUN = 1
   VERB = 2
   ADJECTIVE = 3
   ADVERB = 4

class Target:
    def __init__(self, target : str):
        self.target = target

    def set_lemma(self, lemma: str):
        self.lemma = lemma

    def set_pos(self, pos:POS):
        self.pos = pos

    def __str__(self):
        return self.target

    def __hash__(self):
        return hash(self.target)

class TargetUsage:
    def __init__(self, text: str, offsets: str, **args):
        self.text = text
        self.offsets = offsets

    @property
    def start(self):
        return self.offsets[0]

    @property
    def end(self):
        return self.offsets[1]

    def __getitem__(self,item):
        return self.text[item]

    def __str__(self):
        return self.text

class DWUGUsage(TargetUsage):

    def __init__(self, target, date, grouping, identifier, description,  **args):
        super().__init__(**args)
        self.target = target
        self.date = date
        self.grouping = grouping
        self.identifier = identifier
        self.description = description


class TargetUsageList(list):

    def save(self, path, target):
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(path,target), 'wb+') as f:
            pickle.dump(self,f)

    def load(path, target):
        with open(os.path.join(path,target),'rb') as f:
            return pickle.load(f)
