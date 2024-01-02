
class Line():

    def __init__(self, sentence, fname):
        self.sentence = sentence
        self.fname = fname


class Corpus():

    def __init__(self):
        pass


    def set_sentences_iterator(self, sentences):
        self.sentences_iterator = sentences


    def search(self, words, strategy=None, regex=None):

        if strategy == None:
            raise "You have to define a search strategy."
        else:
            if type(strategy) == str:
                strategy = set([s.strip for s in strategy.split('+')])
            elif type(strategy) == list:
                strategy = set(strategy)

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


class LinebyLineCorpus(Corpus):

    def __init__(self, path):
        self.path = path

    def folder_iterator(self):


    def line_iterator(self):
        
        if self.path