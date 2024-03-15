from numbers import Number

class Time:
    def __init__(self):
        pass

class LiteralTime(Time):
    def __init__(self, time: str):
        self.time = time

class NumericalTime(Time):
    def __init__(self, time: Number):
        self.time = time

class TimeInterval(Time):
    def __init__(self, start: Time, end:Time):
        self.start = start
        self.end = end
        if type(self.start).__name__ == type(self.end).__name__:
            if type(self.start.time) == NumericalTime:
                self.duration = self.end.time - self.start.time
        else:
            raise Exception('start and end points have to be of the same type')