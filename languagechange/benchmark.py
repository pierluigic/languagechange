from languagechange.resource_manager import LanguageChange
from languagechange.corpora import LinebyLineCorpus
from languagechange.usages import Target, TargetUsageList, DWUGUsage
from languagechange.utils import NumericalTime, LiteralTime
import webbrowser
import os
import pickle


class Benchmark():

    def __init__(self):
        pass


class SemEval2020Task1(Benchmark):

    def __init__(self, language):
        lc = LanguageChange()
        self.language = language
        home_path = lc.get_resource('benchmarks', 'SemEval 2020 Task 1', self.language, 'no-version')
        semeval_folder = os.listdir(home_path)[0]
        self.home_path = os.path.join(home_path,semeval_folder)
        self.load()


    def load(self):
        self.corpus1_lemma = LinebyLineCorpus(os.path.join(self.home_path, 'corpus1', 'lemma'), name='corpus1_lemma', language=self.language, time=NumericalTime(1), is_lemmatized=True)
        self.corpus2_lemma = LinebyLineCorpus(os.path.join(self.home_path, 'corpus2', 'lemma'), name='corpus2_lemma', language=self.language, time=NumericalTime(2), is_lemmatized=True)
        self.corpus1_token = LinebyLineCorpus(os.path.join(self.home_path, 'corpus1', 'token'), name='corpus1_token', language=self.language, time=NumericalTime(1), is_tokenized=True)
        self.corpus2_token = LinebyLineCorpus(os.path.join(self.home_path, 'corpus2', 'token'), name='corpus2_token', language=self.language, time=NumericalTime(2), is_tokenized=True)
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

    def __init__(self, path=None, language=None, version=None):
        lc = LanguageChange()
        if not language == None and not version == None:
            self.language = language
            home_path = lc.get_resource('benchmarks', 'DWUG', self.language, version)
            dwug_folder = os.listdir(home_path)[0]
            self.home_path = os.path.join(home_path,dwug_folder)
        else:
            if not path == None and os.path.exists(path):
                self.home_path = path
            else:
                raise Exception('The path is None or does not exists.')       
        self.load()

    def load(self, config=None):
        self.target_words = os.listdir(os.path.join(self.home_path,'data'))
        self.stats_groupings = {}
        self.stats = {}

        stats_path = None
        if not config == None:
            stats_path = os.path.join(self.home_path,'stats',config)
        elif os.path.exists(os.path.join(self.home_path,'stats','opt')):
            stats_path = os.path.join(self.home_path,'stats','opt')
        else:
            stats_path = os.path.join(self.home_path,'stats')

        with open(os.path.join(stats_path,'stats_groupings.csv')) as f:
            keys = []
            for j,line in enumerate(f):
                line = line.replace('\n','').split('\t')
                if j > 0:
                    values = line
                    D = {keys[j]:values[j] for j in range(1,len(values))}
                    self.stats_groupings[values[0]] = D
                else:
                    keys = line

        with open(os.path.join(stats_path,'stats.csv')) as f:
            keys = []
            for j,line in enumerate(f):
                line = line.replace('\n','').split('\t')
                if j > 0:
                    values = line
                    D = {keys[j]:values[j] for j in range(1,len(values))}
                    self.stats[values[0]] = D
                else:
                    keys = line

        self.binary_task = {}
        self.graded_task = {}
        self.binary_gain_task = {}
        self.bianry_loss_task = {}

        for lemma in self.stats_groupings:

            word = Target(lemma)
            word.set_lemma(lemma)
            self.binary_task[word] = int(self.stats_groupings[lemma]['change_binary'])
            self.graded_task[word] = float(self.stats_groupings[lemma]['change_graded'])
            self.binary_gain_task[word] = int(self.stats_groupings[lemma]['change_binary_gain'])
            self.bianry_loss_task[word] = int(self.stats_groupings[lemma]['change_binary_loss'])


    def get_usage_graph(self, word):
        with open(os.path.join(self.home_path,'graphs','opt',word),'rb') as f:
            return pickle.load(f)

    def show_usage_graph(self, word, config=None):
        def run_from_ipython():
            try:
                __IPYTHON__
                return True
            except NameError:
                return False

        def search_plot_path(path):
            if 'weight' in os.listdir(path):
                return path
            else:
                return search_plot_path(os.path.join(path,os.listdir(path)[0]))

        plot_path = None

        if config == None:
            path = search_plot_path(os.path.join(self.home_path,'plots'))
            plot_path = os.path.join(path,'weight','full')   
        else:
            plot_path = os.path.join(self.home_path,'plots',config,'weight','full') 


        if not run_from_ipython():
            webbrowser.open(os.path.join(plot_path,f'{word}.html'))
        else:
            from IPython.display import display, HTML
            with open(os.path.join(plot_path,f'{word}.html')) as f:
                html = f.read()
                display(HTML(html))

    def get_word_usages(self, word, group='all'):
        group = str(group)
        usages = TargetUsageList()
        with open(os.path.join(self.home_path,'data',word,'uses.csv')) as f:
            keys = []
            for j,line in enumerate(f):
                line = line.replace('\n','').split('\t')
                if j > 0:
                    values = line
                    D = {keys[j]:values[j] for j in range(len(values))}
                    if group == 'all' or D['grouping'] == group:
                        D['text'] = D['context']
                        D['target'] = Target(D['lemma'])
                        D['target'].set_lemma(D['lemma'])
                        D['target'].set_pos(D['pos'])
                        D['offsets'] = [int(i) for i in D['indexes_target_token'].split(':')]
                        D['time'] = LiteralTime(D['date'])
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
                    D['time'] = LiteralTime(D['date'])
                    usages.append(DWUGUsage(**D))
                else:
                    keys = line
        return usages

    def get_stats(self):
        return self.stats

    def get_stats_groupings(self):
        return self.get_stats_groupings
        