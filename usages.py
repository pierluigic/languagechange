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
    def __init__(self, context: str, target: str, offsets: str):
        super().__init__(target)

        self.context = context
        self.offsets = offsets

    def set_pos(self, pos: str=None):
        self.pos = pos
