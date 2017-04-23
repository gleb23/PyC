__author__ = 'gleb23'

class CompileError(BaseException):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        if self.position:
            return "\nLine %d, symbol %d" %(self.position[0], self.position[1])
        else:
            return ""


class VariableCantBeVoidError(CompileError):      #TODO add array operations, check array same names, as params
    def __init__(self, position=None):
        super(VariableCantBeVoidError, self).__init__(position)

    def __str__(self):
        return 'VariableCantBeVoidError: %s' %super(VariableCantBeVoidError, self).__str__()


class UnexpectedIdentifierError(CompileError):
    def __init__(self, wrongSymbol=None, possible_symbols = None, position=None):
        super(UnexpectedIdentifierError, self).__init__(position)
        self.wrongSymbol = wrongSymbol
        self.possible_symbols = possible_symbols

    def __str__(self):
        return 'Unexpected identifier \'%s\'%s, %s' \
               %(str(self.wrongSymbol),
                 ', possible symbols:' + str(self.possible_symbols) if self.possible_symbols else "",
                 super(UnexpectedIdentifierError, self).__str__())


class SameNameParameterError(CompileError):
    def __init__(self, name=None, position=None):
        super(SameNameParameterError, self).__init__(position)
        self.name = name

    def __str__(self):
        return 'SameNameParameterError: ' + self.name + super(SameNameParameterError, self).__str__()


class ExpressionError(CompileError):
    def __init__(self, position=None):
        super(ExpressionError, self).__init__(position)

    def __str__(self):
        return 'ExpressionError ' + str(self.value) + super(ExpressionError, self).__str__()


class UnknownIdentifierError(CompileError):
    def __init__(self, value=None, position=None):
        super(UnknownIdentifierError, self).__init__(position)
        self.value = value

    def __str__(self):
        return 'Unknown identifier ' + str(self.value) + super(UnknownIdentifierError, self).__str__()


class FunctionMustReturnSomethingError(CompileError):
    def __init__(self, func_name=None, position=None):
        super(FunctionMustReturnSomethingError, self).__init__(position)
        self.func_name = func_name

    def __str__(self):
        return 'Function %s must return something! %s' %(self.func_name, super(FunctionMustReturnSomethingError, self).__str__())


class EmptyBracketsAreNotAllowedError(CompileError):
    def __init__(self, position=None):
        super(EmptyBracketsAreNotAllowedError, self).__init__(position)

    def __str__(self):
        return 'Empty brackets are not allowed! ' + super(EmptyBracketsAreNotAllowedError, self).__str__()

class ArrayMustHaveFixedSizeError(CompileError):
    def __init__(self, position=None):
        super(ArrayMustHaveFixedSizeError, self).__init__(position)

    def __str__(self):
        return 'Array must have fixed size! ' + super(ArrayMustHaveFixedSizeError, self).__str__()


class IdentifierAlreadyExistsError(CompileError):
    def __init__(self, identifier=None, position=None):
        super(IdentifierAlreadyExistsError, self).__init__(position)
        self.identifier = identifier

    def __str__(self):
        return 'Identifier already exists: ' + str(self.identifier) + super(IdentifierAlreadyExistsError, self).__str__()


class TypeMismatchError(CompileError):
    def __init__(self, found, required=None, position=None):
        super(TypeMismatchError, self).__init__(position)
        self.found = found
        self.required = required

    def __str__(self):
        return 'TypeMismatchError: found %s, required %s, %s '\
               %(self.found,
                 self.required if self.required else 'everything',
                 super(TypeMismatchError, self).__str__())


class WrongParamsFuncCallError(CompileError):
    def __init__(self, func_name=None, position=None):
        super(WrongParamsFuncCallError, self).__init__(position)
        self.func_name = func_name

    def __str__(self):
        return 'Wrong parameters function call: %s, %s' %(self.func_name, super(WrongParamsFuncCallError, self).__str__())


class NotArrayError(CompileError):
    def __init__(self, position=None):
        super(NotArrayError, self).__init__(position)

    def __str__(self):
        return 'NotArrayError! ' + super(NotArrayError, self).__str__()


class IllegalArrayOperationError(CompileError):
    def __init__(self, position=None):
        super(IllegalArrayOperationError, self).__init__(position)

    def __str__(self):
        return 'IllegalArrayOperationError! ' + super(IllegalArrayOperationError, self).__str__()


class EndOfFileReachedError(CompileError):
    def __init__(self, position=None):
        super(EndOfFileReachedError, self).__init__(position)

    def __str__(self):
        return "End of file reached error! " + super(EndOfFileReachedError, self).__str__()


class RuntimeErr(BaseException):
    def __str__(self):
        return 'Runtime error!\n'

class VariableNotInitializedError(RuntimeErr):
    def __str__(self):
        return super(VariableNotInitializedError, self).__str__() + 'Variable not initialized: ' + self.variable

class IndexOutOfBoundsError(RuntimeErr):
    def __init__(self, index=None):
        self.index = index

    def __str__(self):
        return super(IndexOutOfBoundsError, self).__str__() + 'IndexOutOfBoundsError: %s' %(self.index)

class ClassCastError(RuntimeErr):
    def __str__(self):
        return super(ClassCastError, self).__str__() + 'ClassCastError!'

class ZeroDivisionError(RuntimeErr):
    def __str__(self):
        return super(ZeroDivisionError, self).__str__() + 'ZeroDivisionError!'