from languagechange import LanguageChange
from corpora import LinebyLineCorpus
from usages import Target, TargetUsageList, DWUGUsage
import webbrowser
import os


class Benchmark():

    def __init__(self):
        pass

    def set_target_words(self):
        pass


class SemEval2020Task1(Benchmark):

    def __init__(self, language):
        lc = LanguageChange()
        self.language = language
        home_path = lc.get_resource('benchmarks', 'SemEval 2020 Task 1', self.language, 'semeval')
        semeval_folder = os.listdir(home_path)[0]
        self.home_path = os.path.join(home_path,semeval_folder)
        self.load()


    def load(self):
        self.corpus1_lemma = LinebyLineCorpus(os.path.join(self.home_path, 'corpus1', 'lemma'), name='corpus1_lemma', language=self.language, is_lemmatized=True)
        self.corpus2_lemma = LinebyLineCorpus(os.path.join(self.home_path, 'corpus2', 'lemma'), name='corpus2_lemma', language=self.language, is_lemmatized=True)
        self.corpus1_token = LinebyLineCorpus(os.path.join(self.home_path, 'corpus1', 'token'), name='corpus1_token', language=self.language, is_tokenized=True)
        self.corpus2_token = LinebyLineCorpus(os.path.join(self.home_path, 'corpus2', 'token'), name='corpus2_token', language=self.language, is_tokenized=True)
        self.binary_task = {}
        self.graded_task = {}

        with open(os.path.join(self.home_path, 'truth', 'binary.txt')) as f:
            for line in f:
                word, label = line.split()
                word = Target(word)
                self.binary_task[word] = int(label)

        with open(os.path.join(self.home_path, 'truth', 'graded.txt')) as f:
            for line in f:
                word, score = line.split()
                word = Target(word)
                self.graded_task[word] = float(score)


class DWUG(Benchmark):

    def __init__(self, language, version):
        lc = LanguageChange()
        lc.download_ui()
        self.language = language
        home_path = lc.get_resource('benchmarks', 'DWUG', self.language, version)
        dwug_folder = os.listdir(home_path)[0]
        self.home_path = os.path.join(home_path,dwug_folder)
        self.load()

    def load(self):
        self.target_words = os.listdir(os.path.join(self.home_path,'data'))

    def get_usage_graph(self, word):
        pass

    def show_usage_graph(self, word):
        def run_from_ipython():
            try:
                __IPYTHON__
                return True
            except NameError:
                return False

        if not run_from_ipython():
            webbrowser.open(os.path.join(self.home_path,'plots','opt','weight','full',f'{word}.html'))
        else:
            from IPython.display import display, HTML
            display(HTML('<h1>Hello, world!</h1>'))

    def get_word_usages(self, word):
        usages = TargetUsageList()
        with open(os.path.join(self.home_path,'data',word,'uses.csv')) as f:
            keys = []
            for j,line in enumerate(f):
                line = line.replace('\n','').split('\t')
                if j > 0:
                    values = line
                    D = {keys[j]:values[j] for j in range(len(values))}
                    D['text'] = D['context']
                    D['target'] = Target(D['lemma'])
                    D['target'].set_lemma(D['lemma'])
                    D['target'].set_pos(D['pos'])
                    D['offsets'] = [int(i) for i in D['indexes_target_token'].split(':')]
                    usages.append(DWUGUsage(**D))
                else:
                    keys = line
        return usages

    def get_word_annotations(self, word):
        usages = TargetUsageList()
        with open(os.path.join(self.home_path,'data',word,'uses.csv')) as f:
            keys = []
            for j,line in enumerate(f):
                line = line.replace('\n','').split('\t')
                if j > 0:
                    values = line
                    D = {keys[j]:values[j] for j in range(len(values))}
                    D['text'] = D['context']
                    D['target'] = Target(D['lemma'])
                    D['target'].set_lemma(D['lemma'])
                    D['target'].set_pos(D['pos'])
                    D['offsets'] = [int(i) for i in D['indexes_target_token'].split(':')]
                    usages.append(DWUGUsage(**D))
                else:
                    keys = line
        return usages

    def get_stats(self):
        pass

"""
benchmark = SemEval2020Task1('EN')
objects = benchmark.corpus1_lemma.search([Target('attack_nn')], strategy='REGEX')
objects['attack_nn'].save('usages','attack_nn')

usages_attack = TargetUsageList.load('usages','attack_nn')

for target in benchmark.binary_task:
    print(target, benchmark.binary_task[target])
"""


dwug_en = DWUG('EN', '2.0.1')
print(dwug_en.target_words)

dwug_en.get_word_usages('attack_nn')