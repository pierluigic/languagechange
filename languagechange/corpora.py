import os
import gzip
import random
from languagechange.resource_manager import LanguageChange
from languagechange.usages import Target, TargetUsage, TargetUsageList
import re
from languagechange.utils import LiteralTime
from sortedcontainers import SortedKeyList
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Line:

    def __init__(self, raw_text=None, tokens=None, lemmas=None, pos_tags=None, fname=None):
        self._raw_text = raw_text
        self._tokens = tokens
        self._lemmas = lemmas
        self._pos_tags = pos_tags
        self._fname = fname

    def tokens(self):
        if not self._tokens == None:
            return self._tokens
        else:
            return self._lemmas

    def lemmas(self):
        return self._lemmas

    def pos_tags(self):
        return self._pos_tags

    def raw_text(self):
        if not self._raw_text == None:
            return self._raw_text
        else:
            if not self._tokens == None:
                return ' '.join(self._tokens)
            elif not self._lemmas == None:
                return ' '.join(self._lemmas)
            else:
                raise Exception('No valid data in Line')

    def __str__(self):
        return self._raw_text


class Corpus:

    def __init__(self, name, language=None, time=LiteralTime('no time specification'), **args):
        self.name = name
        self.language = language
        self.time = time


    def set_sentences_iterator(self, sentences):
        self.sentences_iterator = sentences


    def search(self, words, strategy='REGEX', search_func=None):

        for j,w in enumerate(words):
            if type(w) == str:
                words[j] = Target(w)

        if search_func == None:
            def search_func(word,line):
                offsets = []
                rex = re.compile(f'( |^)+{word}( |$)+',re.MULTILINE)
                for fi in re.finditer(rex, line):
                    s = line[fi.start():fi.end()].find(word)
                    offsets.append([fi.start()+s, fi.start()+s+len(word)])
                return offsets

        usage_dictionary = {}

        if strategy == 'REGEX':

            for word in words:
                usage_dictionary[word.target] = TargetUsageList()

            logging.info("Scanning the corpus..")
            n_usages = 0

            for line in self.line_iterator():
                for word in words:
                    for offsets in search_func(word.target, line.raw_text()):
                        usage_dictionary[word.target].append(TargetUsage(line.raw_text(), offsets, self.time))
                        n_usages = n_usages + 1

            logging.info(f"{n_usages} usages found.")
        else:

            if type(strategy) == str:
                strategy = set([s.strip().upper() for s in strategy.split('+')])
            elif type(strategy) == list:
                strategy = set([s.upper() for s in strategy])

            for word in words:
                word_form = word.target if 'INFLECTED' in strategy else word.lemma
                usage_dictionary[word_form] = TargetUsageList()

            logging.info("Scanning the corpus..")
            n_usages = 0

            for line in self.line_iterator():
                line_tokens = line.tokens() if 'INFLECTED' in strategy else line.lemmas()
                if line_tokens == None:
                    raise Exception(f"Some of the required features {strategy} are not available for Corpus {self.name}")
                for j,token in enumerate(line_tokens):
                    for word in words:
                        word_form = word.target if 'INFLECTED' in strategy else word.lemma
                        if word_form == token:
                            if (not 'POS' in strategy) or ('POS' in strategy and word_form.pos == line.pos[j]):
                                offsets = [0,0]
                                if not j == 0:
                                    offsets[0] = len(' '.join(line.tokens()[:j])) + 1
                                offsets[1] = offsets[0] + len(line.tokens()[j])
                                usage_dictionary[word_form].append(TargetUsage(' '.join(line.tokens()), offsets, self.time))
                                n_usages = n_usages + 1

            logging.info(f"{n_usages} usages found.")
        return usage_dictionary


    def folder_iterator(self, path):

        fnames = []

        for fname in os.listdir(path):

            if os.path.isdir(os.path.join(path,fname)):
                fnames = fnames + self.folder_iterator(os.path.join(path,fname))
            else:
                fnames.append(os.path.join(path,fname))

        return fnames


    def cast_to_Vertical(corpora, vertical_corpus):

        line_iterators = [corpus.line_iterator() for corpus in corpora]
        iterate = True

        with open(vertical_corpus.path,'w+') as f:

            while iterate:
                lines = []
                for iterator in line_iterator:
                    next_line = next(iterator)
                if not next_line == None:
                    vertical_lines = []
                    for j in range(len(lines[0])):
                        vertical_lines.append('{vertical_corpus.field_separator}'.join([lines[i][j] for i in range(len(lines))]))
                    for line in vertical_lines:
                        f.write(line+'\n')
                    f.write(vertical_corpus.sentence_separator)
                else:
                    iterate = False


    def save(self):
        lc = LanguageChange()
        path = lc.save_resource('corpus',f'{self.language} corpora',self.name)


class LinebyLineCorpus(Corpus):

    def __init__(self, path, **args):
        super().__init__(**args)
        self.path = path

        if 'is_sentence_tokenized' in args:
            self.is_sentence_tokenized = args['is_sentence_tokenized']
        else:
            self.is_sentence_tokenized = False

        if self.is_sentence_tokenized:
            if 'is_tokenized' in args:
                self.is_tokenized = args['is_tokenized']
        else:
            if 'is_tokenized' in args and args['is_tokenized']:
                self.is_sentence_tokenized = True
                self.is_tokenized = True
            else:
                self.is_sentence_tokenized = False
                self.is_tokenized = False

        if self.is_tokenized:
            if 'is_lemmatized' in args:
                self.is_lemmatized = args['is_lemmatized']
            if 'tokens_splitter' in args:
                self.tokens_splitter = args.tokens_splitter
            else:
                self.tokens_splitter = ' '
        else:
            if 'is_lemmatized' in args and args['is_lemmatized']:
                self.is_sentence_tokenized = True
                self.is_tokenized = True
                self.is_lemmatized = True
                if 'tokens_splitter' in args:
                    self.tokens_splitter = args.tokens_splitter
                else:
                    self.tokens_splitter = ' '
            else:
                self.is_lemmatized = False


    def line_iterator(self):
        
        if os.path.isdir(self.path):
            fnames = self.folder_iterator(self.path)
        else:
            fnames = [self.path]

        def get_data(line):
            line = line.replace('\n','')
            data = {}
            data['raw_text'] = line
            if self.is_lemmatized:
                data['lemmas'] = line.split(self.tokens_splitter)
            elif self.is_tokenized:
                data['tokens'] = line.split(self.tokens_splitter)
            return data

        for fname in fnames:

            if fname.endswith('.txt'):
                with open(fname,'r') as f:
                    for line in f:
                        data = get_data(line)
                        yield Line(fname=fname, **data)

            elif fname.endswith('.gz'):
                with gzip.open(fname, mode="rt") as f:
                    for line in f:
                        data = get_data(line)
                        yield Line(fname=fname, **data)

            else:
                raise Exception('Format not recognized')


class VerticalCorpus(Corpus):

    def __init__(self, path, sentence_separator='\n', field_separator='\t', field_map={'token':0, 'lemma':1, 'pos_tag':2}, **args):
        self.super(**args)
        self.path = path
        self.sentence_separator = sentence_separator
        self.field_separator = field_separator
        self.field_map = field_map


    def line_iterator(self):
        
        if os.path.isdir(self.path):
            fnames = self.folder_iterator(path)
        else:
            fnames = [self.path]

        def get_data(line):
            data = {}
            splitted_line = [vertical_line.split(self.field_separator) for vertical_line in line]
            raw_text = [vertical_line[self.field_map['token']] for vertical_line in splitted_line]
            data['raw_text'] = ' '.join(raw_text)
            data['tokens'] = raw_text
            if 'lemma' in self.field_map:
                lemma_text = [vertical_line[self.field_map['lemma']] for vertical_line in splitted_line]
                data['lemmas'] = lemma_text
            if 'pos_tag' in self.field_map:
                pos_text = [vertical_line[self.field_map['pos']] for vertical_line in splitted_line]     
            return data

        for fname in fnames:

            if fname.endswith('.txt'):
                with open(fname,'r') as f:
                    line = []
                    for vertical_line in f:
                        if vertical_line == self.sentence_separator:
                            data = get_data(line)
                            yield Line(fname=fname, **data)
                            line = []
                        else:
                            line.append(vertical_line)

            elif fname.endswith('.gz'):
                with gzip.open(fname, mode="rt") as f:
                    for vertical_line in f:
                        if vertical_line == self.sentence_separator:
                            data = get_data(line)
                            yield Line(fname=fname, **data)
                            line = []
                        else:
                            line.append(vertical_line)

            else:
                raise Exception('Format not recognized')



class HistoricalCorpus(SortedKeyList):

    def __init__(self, corpora:list[Corpus]):
        super().__init__(corpora, key= lambda x: x.time)

