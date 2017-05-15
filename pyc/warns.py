__author__ = 'hlib'

class Warning(object):
    def __init(self, position):
        self.position = position

class InstructionHasNoEffectWarning(Warning):
    def __init__(self, position):
        super(InstructionHasNoEffectWarning, self).__init(position)
