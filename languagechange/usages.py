import enum
import pickle
from pathlib import Path
import os
from languagechange.utils import Time


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
    def __init__(self, text: str, offsets: str, time: Time = None, **args):
        self.text_ = text
        self.offsets = offsets
        self.time = time

    def text(self):
        return self.text_

    def start(self):
        return self.offsets[0]

    def end(self):
        return self.offsets[1]

    def time(self):
        return self.time

    def __getitem__(self,item):
        return self.text_[item]

    def __str__(self):
        return self.text_

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

    def time_axis(self):
        return [usage.time for usage in self]