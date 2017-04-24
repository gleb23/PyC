import copy

from src.errs import IndexOutOfBoundsError, TypeMismatchError
from src import errs


__author__ = 'gleb23'


class AbstractType(object):
    def __init__(self):
        super(AbstractType, self).__init__()

    def get_type(self):
        return self.__class__

    def to_Bool(self):
        raise NotImplementedError

    def to_Int(self):
        raise NotImplementedError

class Void(AbstractType):
    def __init__(self):
        super(Void, self).__init__()

    def get_type(self):
        return self.__class__

    def to_Bool(self):
        raise TypeMismatchError(Void, Bool)

    def to_Int(self):
        raise TypeMismatchError(Void, Int)

    def execute(self):
        return self


class SimpleType(AbstractType):
    def __init__(self, value):
        super(SimpleType, self).__init__()
        self.value = value

    def getx(self):
        return self._value

    def execute(self):
        return self


class Int(SimpleType):
    def __init__(self, value=0):
        super(Int, self).__init__(value)
        #self.value = property(SimpleType.getx, self.setx)
    def setx(self, value):
        if isinstance(value, int):
            SimpleType._value = value
        else:
            raise TypeError

    def to_Bool(self):
        return Bool(self.value != 0)

    def to_Int(self):
        return self

    def __str__(self):
        return "int"


class Bool(SimpleType):
    def __init__(self, value = False):
        super(Bool, self).__init__(value)
        #self.value = property(SimpleType.getx, self.setx)

    def setx(self, value):
        try:
            SimpleType._value = bool(value)
        except ValueError:
            raise TypeError

    def to_Bool(self):
        return self

    def to_Int(self):
        if self.value:
            return Int(1)
        else:
            return Int(0)

    def __str__(self):
        return "bool"


class String(SimpleType):
    def __init__(self, value = ""):
        super(String, self).__init__(value)
        self._x = None
        #self.value = property(SimpleType.getx, self.setx)

    def setx(self, value):
        if isinstance(value, basestring):
            SimpleType._value = value
        else:
            raise TypeError()

    def to_Bool(self):
        return Bool(self.value != "")

    def __str__(self):
        return "string"


class AbstractArray(AbstractType):
    pass

################### ARRAY


def init(self):
        self.buffer = []
        for i in range(ArrayMetaclass.size):
            self.buffer.append(ArrayMetaclass.base_type())


def get(self, ind):
    if ind >= 0 and ind < len(self.buffer):
        return self.buffer[ind]
    raise IndexOutOfBoundsError(ind)


def set(self, ind, value):
    if ind > 0 and ind < len(self.buffer):
        self.buffer[ind] = value
    raise IndexOutOfBoundsError(ind)


def __str__(self):
    return 'base: ' + str(ArrayMetaclass.base) + ' size: ' + 'str(self.buffer.size)'


class ArrayMetaclass(type):
    def __new__(cls, base_type, size):
        cls.base_type = base_type
        cls.size = size
        return type("SizedArray", (AbstractArray,), {'base_type': base_type, 'size': size,
                                              '__init__': init, 'get': get, 'set': set})

################ ARRAY


class Expression(object):
    def __init__(self):
        super(Expression, self).__init__()
        # self.parent_expression = None
        # self.bracket_state = 0

    def execute(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError


class FunctionCall(Expression):
    def __init__(self, function = None):
        super(FunctionCall, self).__init__()
        self.function = function
        self.args = []

    def execute(self):
        self.function = copy.deepcopy(self.function) #different context
        for i in range(len(self.function.params)):
            self.function.params[i].value = self.args[i].execute().value #by value
        return self.function.execute()

    def get_type(self):
        return self.function.returnType

    def __str__(self):
        s = 'Function call(function: ' + str(self.function) + ';'
        for arg in self.args:
            s += (str(arg) + ', ')
        s += ')'
        return s


class ReturnExpression(Expression):
    def __init__(self, exp = None):
        self.exp = exp

    def execute(self):
        return self.exp.execute()

    def get_type(self):
        return self.exp.get_type()

    def __str__(self):
        return 'Return expression(' + self.exp + ')'


class ArrayElement(Expression):
    def __init__(self, array=None, index=None):
        self.array = array
        self.index = index

    def execute(self):
        return self.array.get(self.index.execute().value).execute()

    def get_type(self):
        return self.array.__class__.base_type


class BinaryOperator(Expression):
    def __init__(self):
        super(BinaryOperator, self).__init__()
        self.exp1 = None
        self.exp2 = None

    def get_type(self):
        raise NotImplementedError


class Not(Expression):
    def __init__(self):
        super(Not, self).__init__()
        self.exp1 = None

    def execute(self):
        a = self.exp1.execute()
        if a.get_type() == String or a.get_type() == Void or issubclass(a.get_type(), AbstractArray):
            raise TypeMismatchError(a.get_type())
        else:
            return Bool(not a.to_Bool().value)

    def get_type(self):
        a = self.exp1.get_type()
        if a == Void or a == String or issubclass(a, AbstractArray):
            raise TypeMismatchError(a)
        else: # INT or BOOL
            return Bool


class And(BinaryOperator):
    def __init__(self):
        super(And, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if a.get_type() == String or b.get_type() == String:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif a.get_type() == Void or b.get_type() == Void:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif issubclass(a.get_type(), AbstractArray) or issubclass(b.get_type(), AbstractArray):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            return Bool(a.to_Bool().value and b.to_Bool().value)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Bool


class Or(BinaryOperator):
    def __init__(self):
        super(Or, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if a.get_type() == String or b.get_type() == String:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif a.get_type() == Void or b.get_type() == Void:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif issubclass(a.get_type(), AbstractArray) or issubclass(b.get_type(), AbstractArray):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            return Bool(a.to_Bool().value or b.to_Bool().value)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Bool


class Sum(BinaryOperator):
    def __init__(self):
        super(Sum, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if a.get_type() == String and b.get_type() == String:
            return String(a + b)
        elif a.get_type() == String or b.get_type() == String:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif a.get_type() == Void and b.get_type() == Void:
            raise TypeMismatchError(b.get_type(), a.get_type())
        elif issubclass(a.get_type(), AbstractArray) or issubclass(b.get_type(), AbstractArray):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            return Int(a.to_Int().value + b.to_Int().value)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String and b == String:
            return a
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Int

    def __str__(self):
        return '(' + str(self.exp1) + '+' + str(self.exp2) + ')'


class Minus(BinaryOperator):
    def __init__(self):
        super(Minus, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            return Int(a.to_Int().value - b.to_Int().value)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Int

    def __str__(self):
        return '(' + str(self.exp1) + '-' + str(self.exp2) + ')'


class Mult(BinaryOperator):
    def __init__(self):
        super(Mult, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            return Int(a.to_Int().value * b.to_Int().value)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Int

    def __str__(self):
        return '(' + str(self.exp1) + '*' + str(self.exp2) + ')'


class Div(BinaryOperator):
    def __init__(self):
        super(Div, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            try:
                return Int(a.to_Int().value / b.to_Int().value)
            except ZeroDivisionError:
                raise errs.ZeroDivisionError()

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Int

    def __str__(self):
        return '(' + str(self.exp1) + '/' + str(self.exp2) + ')'

class Mod(BinaryOperator):
    def __init__(self):
        super(Mod, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            try:
                return Int(a.to_Int().value % b.to_Int().value)
            except ZeroDivisionError:
                raise errs.ZeroDivisionError()

    def get_type(self): #DRY ?
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif a == String or b == String:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else: # INT or BOOL
            return Int

    def __str__(self):
        return '(' + str(self.exp1) + '%' + str(self.exp2) + ')'

class CompOperator(BinaryOperator):
    def __init__(self, less=False, equals=False, more=False):
        super(CompOperator, self).__init__()
        self.less = less
        self.equals = equals
        self.more = more

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatchError(b.get_type(), a.get_type())
        else:
            if self.less:
                if a.to_Int().value < b.to_Int().value:
                    return Bool(True)
            if self.equals:
                if a.to_Int().value == b.to_Int().value:
                    return Bool(True)
            if self.more:
                if a.to_Int().value > b.to_Int().value:
                    return Bool(True)
            return Bool(False)

    def get_type(self):
        a = self.exp1.get_type()
        b = self.exp2.get_type()
        if a == String or b == String:
            raise TypeMismatchError(b, a)
        elif a == Void or b == Void:
            raise TypeMismatchError(b, a)
        elif issubclass(a, AbstractArray) or issubclass(b, AbstractArray):
            raise TypeMismatchError(b, a)
        else:
            return Bool

    def __str__(self):
        return '(' + str(self.exp1) \
               + '|less|' if self.less else ''\
                                            + '|equals|' if self.equals else ''\
                                                                             + '|more|' if self.more else ''\
                                                                                                          + str(self.exp2) + ')'


# FLOW

class Instruction(object):
    pass

class Block(Instruction):
    def __init__(self, parent_block):
        super(Block, self).__init__()
        self.context = Context()
        self.instructions = []
        self.parent_block = parent_block

    def execute(self):
        for instruction in self.instructions:
            res = instruction.execute()
            if res.get_type() != Void:
                return res
        return Void()

    # def __str__(self):
    #     s = 'Block {\n'
    #     s += 'Context:\n'
    #     s += str(self.context)
    #     s += '\n'
    #     for instr in self.instructions:
    #         s += str(instr)
    #         s += '\n'
    #     s += '}'
    #     return s

class WhileLoop(Instruction):
    def __init__(self, condition=None, body=None):
        super(WhileLoop, self).__init__()
        self.condition = condition
        self.body = body

    def execute(self):
        while self.condition.execute().to_Bool().value:
            res = self.body.execute()
            if res.get_type() != Void:
                return res
        return Void()

    def __str__(self):
        s = 'While {\n'
        s += 'CONDITION: '
        s += str(self.condition)
        s += str(self.body)
        s += '}'
        return s

class If(Instruction):
    def __init__(self, case_list=None, else_branch=None):
        super(If, self).__init__()
        if case_list is None:
            self.case_list = []
        else:
            self.case_list = case_list
        self.else_branch = else_branch

    def execute(self):
        for case in self.case_list:
            if case[0].execute().to_Bool().value:
                return case[1].execute()
        if self.else_branch:
            return self.else_branch.execute()
        return Void()

class Context(object):
    def __init__(self):
        self.constants = {}
        self.variables = {}
        self.functions = {}

    def __str__(self):
        s = 'Context:{'
        s += '\nConstants: '
        for con in self.constants.keys():
            s += (con + " : " + str(self.constants[con]))
        s += '\nVariables: '
        for v in self.variables.keys():
            s += (v + " : " + str(self.variables[v]))
        s += '\nFunctions: '
        for f in self.functions.keys():
            s += (f + " : " + str(self.functions[f]))
        s += '\n}'
        return s


class Function(object):
    def __init__(self, name=None, parent_block=None, params=None, return_type=None):
        self.name = name
        if params is None:
            self.params = []
        else:
            self.params = params
        self.returnType = return_type
        self.block = Block(parent_block)

    def execute(self):
        for param in self.params:
            assert param is not None
        return self.block.execute()

    # def __str__(self):
    #     s = "Function {\n"
    #     s += ("Name: " + str(self.name) + "\n")
    #     s += ("Returns: " + str(self.returnType) + "\n")
    #     for param in self.params:
    #         s += str(param) + " "
    #     s += "\n"
    #     s += str(self.block)
    #     s += "}"
    #     return s


class AssignmentOperator(Instruction):
    def __init__(self):
        super(AssignmentOperator, self).__init__()
        self.variable = None
        self.exp = None

    def execute(self):
        a = self.variable.execute()
        b = self.exp.execute()
        if a.get_type() == String and b.get_type() == String:
            a.value = b.value
        elif a.get_type() == String or b.get_type() == String:
            raise TypeMismatchError(self.exp.get_type(), self.variable.get_type())
        elif a.get_type() == Int:
            a.value = b.to_Int().value
        elif a.get_type() == Bool:
            a.value = b.to_Bool().value
        elif a.get_type() == Void:
            pass
        return Void()


class PrintOperator(Instruction):
    def __init__(self):
        super(PrintOperator, self).__init__()
        self.value = None

    def execute(self):
        a = self.value.execute()
        if a.get_type() == Void:
            raise TypeMismatchError(a.get_type())
        else:
            print a.value
        return Void()
