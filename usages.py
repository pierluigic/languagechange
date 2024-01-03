class Target:
    def __init__(self, target : str):
        self.target = target

    def set_lemma(self, lemma: str):
        self.lemma = lemma

    def __str__(self):
        return self.target

    def __hash__(self):
        return hash(self.target)

class TargetUsage(Target):
    def __init__(self, context: str, target: str, offsets: str, pos: str=None):
        super().__init__(target)

        self.context = context
        self.offsets = offsets
        self.pos = pos

    @property
    def token(self):
        start, end = [int(i) for i in self.offsets.split(':')]
        return self.context[start:end]

    @property
    def start(self):
        start, end = [int(i) for i in self.offsets.split(':')]
        return start

    @property
    def end(self):
        start, end = [int(i) for i in self.offsets.split(':')]
        return end