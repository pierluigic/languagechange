

class Usage():

    def __init__(self, sentence, word, offsets)
        self.sentence = sentence
        self.word = word
        self.offsets = offsets


class Word():

    def __init__(self, word):
        self.word = word

    def set_pos(pos):
        self.pos = pos

    def set_lemma(lemma):
        self.lemma = lemma

    def __str__(self):
        return word

    def __hash__(self):
        return hash(self.word)
