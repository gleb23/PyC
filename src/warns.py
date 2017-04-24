__author__ = 'gleb23'

class Warning(object):
    def __init(self, position):
        self.position = position

class InstructionHasNoEffectWarning(Warning):
    def __init__(self, position):
        super(InstructionHasNoEffectWarning, self).__init(position)
