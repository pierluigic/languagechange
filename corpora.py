import os
import gzip
import random
from languagechange import LanguageChange

class Line():

    def __init__(self, sentence, fname):
        self.sentence = sentence
        self.fname = fname

    def iter_tokens(self, tokenizer):
        pass


class Corpus():

    def __init__(self, name, language, is_tokenized=False, is_sentence_tokenized=False):
        self.name = name
        self.language = language
        self.is_tokenized = is_tokenized
        self.is_sentence_tokenized = is_sentence_tokenized


    def set_sentences_iterator(self, sentences):
        self.sentences_iterator = sentences


    def search(self, words, strategy=None, regex=None):

        if strategy == None:
            raise "You have to define a search strategy."
        else:
            if type(strategy) == str:
                strategy = set([s.strip().upper() for s in strategy.split('+')])
            elif type(strategy) == list:
                strategy = set([s.upper() for s in strategy])

        if 'POS' in strategy:
            if 'INFLECTED' in strategy:
                pass
            elif 'LEMMA' in strategy:
                pass
            else:
                raise "Strategy have to be INFLECTED or LEMMA."
        else:
            if 'INFLECTED' in strategy:
                pass
            elif 'LEMMA' in strategy:
                pass
            else:
                raise "Strategy have to be INFLECTED or LEMMA."

    def save(self):
        lc = LanguageChange()
        path = lc.save_resource('corpus',f'{self.language} corpora',self.name)


class LinebyLineCorpus(Corpus):

    def __init__(self, path, **args):
        self.super(**args)
        self.path = path

    def folder_iterator(self, path):

        fnames = []

        for fname in os.listdir(path):

            if os.isdir(os.path.join(path,fname)):
                folders = folders + self.folder_iterator(os.path.join(path,fname))
            else:
                folders.append(os.path.join(path,fname))

    def line_iterator(self):
        
        if os.isdir(self.path):
            fnames = self.folder_iterator(path)
        else:
            fnames = [self.path]

        for fname in fnames:

            if fname.endswith('.txt'):
                with open(fname,'r') as f:
                    for line in f:
                        yield Line(line,fname)

            elif fname.endswith('.gz'):
                with gzip.open(fname, mode="rt") as f:
                    for line in f:
                        yield Line(line,fname)

            else:
                raise 'Format not recognized'
