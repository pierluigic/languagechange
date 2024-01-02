from languagechange import LanguageChange
import utils
from corpora import LinebyLineCorpus
from usages import Word
import os

class Benchmark():

    def __init__(self):
        pass

    def set_target_words(self):
        pass


class SemEval2020Task1(Benchmark):

    def __init__(self, language):
        lc = LanguageChange()
        lc.resources_dir
        self.language = language
        self.home_path = lc.get_resource('benchmarks','SemEval 2020 Task 1',self.language,'semeval')
        self.load()

    def load(self):
        self.corpus1_lemma = LinebyLineCorpus(os.path.join(self.home_path,'corpus1','lemma'))
        self.corpus2_lemma = LinebyLineCorpus(os.path.join(self.home_path,'corpus2','lemma'))
        self.corpus1_token = LinebyLineCorpus(os.path.join(self.home_path,'corpus1','token'))
        self.corpus2_token = LinebyLineCorpus(os.path.join(self.home_path,'corpus2','token'))
        self.binary_task = {}
        self.graded_task = {}

        with open(os.path.join(self.home_path,'truth','binary.txt')) as f:
            for line in f:
                word, label = line.split()
                word = Word(word)
                self.binary_task[word] = int(label)

        with open(os.path.join(self.home_path,'truth','graded.txt')) as f:
            for line in f:
                word, score = line.split()
                word = Word(word)
                self.graded_task[word] = float(score)



class DWUG(Benchmark):

    def __init__(self):
        pass


    def get_usage_graph(self, word):
        pass


    def get_word_usages(self, word):
        pass


benchmark = SemEval2020Task1('EN')