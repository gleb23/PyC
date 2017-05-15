from pyc.bricks import Int, String, Bool, If, WhileLoop, ReturnExpression, SimpleType, AssignmentOperator, Function, FunctionCall, Block, \
    Sum,  ArrayMetaclass, AbstractArray
from pyc.builtins import builtins_map
from pyc.errs import UnexpectedIdentifierError, ExpressionError, UnknownIdentifierError, FunctionMustReturnSomethingError, EmptyBracketsAreNotAllowedError, ArrayMustHaveFixedSizeError, IdentifierAlreadyExistsError, NotArrayError, TypeMismatchError, IllegalArrayOperationError, EndOfFileReachedError, SameNameParameterError, WrongParamsFuncCallError, VariableCantBeVoidError, CompileError
from pyc.lexer import Lexer
from pyc import bricks

__author__ = 'gleb23'

# = 3
# if (a) {
#     int myprint(int a) {
# return a * a;
# }
# myprint(a);
# }

operator_priorities = [
    ['||'],
    ['&&'],
    ['!'],
    ['<', '<=', '>', '>=', '==', '!='],
    ['+', '-'],
    ['*', '/', '%'],
]

def searchIdentifier(current_block, identifier, only_this_scope=False):
    '''
    searches for identifier <code>identifier</code> in current scope or outer
    '''
    if current_block is None:
        return builtins_map.get(identifier)
    if current_block.context.functions.has_key(identifier):
        return current_block.context.functions[identifier]
    if current_block.context.variables.has_key(identifier):
        return current_block.context.variables[identifier]
    if only_this_scope:
        return searchIdentifier(None, identifier)
    else:
        return searchIdentifier(current_block.parent_block, identifier)

def split(reverse_expression_list, index, operator, bracket_state):
    operator.exp1 = build_expression_tree(reverse_expression_list[index + 1:], bracket_state)
    operator.exp2 = build_expression_tree(reverse_expression_list[:index], bracket_state)
    return operator

def build_expression_tree(reverse_expression_list, bracket_state = 0):
    if len(reverse_expression_list) == 1:
        val = reverse_expression_list[0][0]
        if isinstance(val, basestring) and val.isdigit():
            try:
                return Int(int(float(val)))
            except ValueError:
                assert False
        elif isinstance(val, basestring):
            return String(val[1:len(val)-1])
        elif isinstance(val, int):
            return Int(val)
        else:
            return val


    while True:
        for i in range(len(operator_priorities)):
            for j in range(len(operator_priorities[i])):
                try:
                    ind = reverse_expression_list.index((operator_priorities[i][j], bracket_state))
                    if reverse_expression_list[ind] == ('+', bracket_state):
                        op = Sum()
                    elif reverse_expression_list[ind] == ('-', bracket_state):
                        op = bricks.Minus()
                    elif reverse_expression_list[ind] == ('*', bracket_state):
                        op = bricks.Mult()
                    elif reverse_expression_list[ind] == ('/', bracket_state):
                        op = bricks.Div()
                    elif reverse_expression_list[ind] == ('%', bracket_state):
                        op = bricks.Mod()
                    elif reverse_expression_list[ind] == ('<', bracket_state):
                        op = bricks.CompOperator(less=True)
                    elif reverse_expression_list[ind] == ('<=', bracket_state):
                        op = bricks.CompOperator(less=True, equals=True)
                    elif reverse_expression_list[ind] == ('>', bracket_state):
                        op = bricks.CompOperator(more=True)
                    elif reverse_expression_list[ind] == ('>=', bracket_state):
                        op = bricks.CompOperator(more=True, equals=True)
                    elif reverse_expression_list[ind] == ('==', bracket_state):
                        op = bricks.CompOperator(equals=True)
                    elif reverse_expression_list[ind] == ('!=', bracket_state):
                        op = bricks.CompOperator(less=True, more=True)
                    elif reverse_expression_list[ind] == ('!', bracket_state):
                        op = bricks.Not()
                    elif reverse_expression_list[ind] == ('&&', bracket_state):
                        op = bricks.And()
                    elif reverse_expression_list[ind] == ('||', bracket_state):
                        op = bricks.Or()
                    else:
                        raise NotImplementedError
                    return split(reverse_expression_list, ind, op, bracket_state)
                except ValueError:
                    pass
        reverse_expression_list = reverse_expression_list[1:len(reverse_expression_list) -1]
        bracket_state += 1


class Subexpression:
    def __init__(self):
        self.expression_list = []
        self.bracket_state = 0
        self.expression_type = None

class CurrentDataSet(object):
    def __init__(self):
        self.current_block = None
        self.current_flow_object = None
        self.current_return_expression = None
        self.current_assignment = None
        self.current_identifier = None
        self.current_arithm_op = None
        self.current_variable = None #variable that was referenced last
        self.current_called_function = None # function that was called last
        self.var_type = None
        self.current_number = "" # number literal that was met last
        self.current_string_literal = ""
        self.current_function = None #function in which scope 'cursor' is
        self.subexpressions = []
        self.current_expression = None
        self.current_substate = None
        self.current_bool_value = None


class State(object):
    def process_opening_curly_bracket(self, data_set):
        raise UnexpectedIdentifierError('{')

    def process_closing_curly_bracket(self, data_set):
        raise UnexpectedIdentifierError('}')

    def process_opening_square_bracket(self, data_set):
        raise UnexpectedIdentifierError('[')

    def process_closing_square_bracket(self, data_set):
        raise UnexpectedIdentifierError(']')

    def process_opening_bracket(self, data_set):
        raise UnexpectedIdentifierError('(')

    def process_closing_bracket(self, data_set):
        raise UnexpectedIdentifierError(')')

    def process_comma(self, data_set):
        raise UnexpectedIdentifierError(',')

    def process_semicolon(self, data_set):
        raise UnexpectedIdentifierError(';')

    def process_if(self, data_set):
        raise UnexpectedIdentifierError('if')

    def process_else(self, data_set):
        raise UnexpectedIdentifierError('else')

    def process_while(self, data_set):
        raise UnexpectedIdentifierError('while')

    def process_return(self, data_set):
        raise UnexpectedIdentifierError('return')

    def process_identifier(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_basic_data_type(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_assignment(self, data_set):
        raise UnexpectedIdentifierError('=')

    def process_number(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_string_literal(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_print(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_arithmetic_operations(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_bool_value(self, data_set):
        raise UnexpectedIdentifierError(data_set.current_identifier)


################################################
###### EXPRESSION ###########################
################################################
class AfterExpressionOpenBracket(State):
    '''
    example
    ...
    a = (... <-
    ...

    '''

    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0,('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set):
        raise EmptyBracketsAreNotAllowedError()

    def process_identifier(self, data_set):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, bricks.AbstractArray):
            data_set.current_variable = type
            return AfterArrayAtStartState(), data_set
        elif isinstance(type, SimpleType):
            data_set.current_variable = type
            data_set.current_expression.expression_list\
                .insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            data_set.current_called_function = type
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_opening_curly_bracket(self, data_set):
        raise ExpressionError()

    def process_closing_curly_bracket(self, data_set):
        raise ExpressionError()

    def process_opening_square_bracket(self, data_set):
        raise ExpressionError()

    def process_closing_square_bracket(self, data_set):
        raise ExpressionError()

    def process_comma(self, data_set):
        raise ExpressionError()

    def process_semicolon(self, data_set):
        raise ExpressionError()

    def process_if(self, data_set):
        raise ExpressionError()

    def process_else(self, data_set):
        raise ExpressionError()

    def process_while(self, data_set):
        raise ExpressionError()

    def process_return(self, data_set):
        raise ExpressionError()

    def process_basic_data_type(self, data_set):
        raise ExpressionError()

    def process_assignment(self, data_set):
        raise ExpressionError()

    def process_print(self, data_set):
        raise ExpressionError()

    def process_arithmetic_operations(self, data_set):
        raise ExpressionError()


class AfterExpressionOperator(State):
    '''
    example
    ...
    a = (a +... <-
    ...

    '''

    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list\
                .insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_string_literal,data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_opening_curly_bracket(self, data_set):
        raise ExpressionError()

    def process_closing_curly_bracket(self, data_set):
        raise ExpressionError()

    def process_opening_square_bracket(self, data_set):
        raise ExpressionError()

    def process_closing_square_bracket(self, data_set):
        raise ExpressionError()

    def process_closing_bracket(self, data_set):
        raise ExpressionError()

    def process_comma(self, data_set):
        raise ExpressionError()

    def process_semicolon(self, data_set):
        raise ExpressionError()

    def process_if(self, data_set):
        raise ExpressionError()

    def process_else(self, data_set):
        raise ExpressionError()

    def process_while(self, data_set):
        raise ExpressionError()

    def process_return(self, data_set):
        raise ExpressionError()

    def process_basic_data_type(self, data_set):
        raise ExpressionError()

    def process_assignment(self, data_set):
        raise ExpressionError()

    def process_print(self, data_set):
        raise ExpressionError()

    def process_arithmetic_operations(self, data_set):
        raise ExpressionError()


class AfterExpressionOperand(State):
    '''
    example
    ...
    a = (4... <-
    ...

    '''
    def process_closing_bracket(self, data_set):
        if data_set.current_expression.bracket_state >0:
            data_set.current_expression.bracket_state -= 1
            data_set.current_expression.expression_list.insert(0, (')', data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'function_param':
                func_arg = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_expression = data_set.subexpressions[-1]
                data_set.current_expression.expression_list[0][0].args.append(func_arg)
                #check whether function call args are the same as in function
                func_name = data_set.current_expression.expression_list[0][0].function.name
                actual_params = data_set.current_expression.expression_list[0][0].args
                formal_params = data_set.current_expression.expression_list[0][0].function.params
                if len(actual_params) != len(formal_params):
                    raise WrongParamsFuncCallError(func_name)
                else:
                    for i in range(len(actual_params)):
                        if not issubclass(actual_params[i].get_type(), formal_params[i].get_type()):
                            raise WrongParamsFuncCallError(func_name)
                    else:
                        return AfterExpressionOperand(), data_set
            elif data_set.current_expression.expression_type == 'predicate':
                newBlock = Block(data_set.current_block)
                predicate = build_expression_tree(data_set.current_expression.expression_list)

                if data_set.current_block.instructions[-1].__class__ == If:
                    case = (predicate, newBlock)
                    data_set.current_block.instructions[-1].case_list.append(case)
                elif data_set.current_block.instructions[-1].__class__ == WhileLoop:
                    data_set.current_block.instructions[-1].condition = predicate
                    data_set.current_block.instructions[-1].body = newBlock
                else:
                    assert False

                data_set.subexpressions.pop()
                data_set.current_block = newBlock
                return AfterIfWhileCondition(), data_set


            else: #array_index_at_start, array_index
                return UnexpectedIdentifierError(')')
        else:
            return UnexpectedIdentifierError(')')

    def process_closing_square_bracket(self, data_set):
        if data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'array_index':
                array_index = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_expression = data_set.subexpressions[-1]
                data_set.current_expression.expression_list[0][0].index = array_index

                if data_set.subexpressions[-1].expression_type == 'array_element_at_start':
                    data_set.current_variable = data_set.subexpressions[-1].expression_list[0][0]
                    data_set.subexpressions = []
                    data_set.current_expression = None
                    return AfterSVariableAtStartState(), data_set
                else:
                    return AfterExpressionOperand(), data_set
            else:
                raise UnexpectedIdentifierError(']')
        else:
            raise UnexpectedIdentifierError(']')

    def process_comma(self, data_set):
        # end of argument expression
        if data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'function_param':
                func_arg = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.subexpressions[-1].expression_list[0][0].args.append(func_arg)
                data_set.current_expression = Subexpression()
                data_set.subexpressions.append(data_set.current_expression)
                data_set.current_expression.expression_type = 'function_param'
                return AfterFunctionCallOpenBracketState(), data_set
            else:
                raise UnexpectedIdentifierError(',')
        else:
            raise UnexpectedIdentifierError(',')

    def process_semicolon(self, data_set):
        if data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'return_expression':
                return_expression = build_expression_tree(data_set.current_expression.expression_list)
                exp_type = return_expression.get_type()
                return_type = data_set.current_function.returnType
                if exp_type != return_type:
                    raise TypeMismatchError(exp_type, return_type)
                data_set.subexpressions.pop()
                data_set.current_block.instructions[-1].exp = return_expression
                return InitialState(), data_set
            elif data_set.current_expression.expression_type == 'assignment_value':
                assignment_value = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                del(data_set.current_expression)
                data_set.current_block.instructions[-1].exp = assignment_value  # last inst is assignment op
                return InitialState(), data_set
            elif data_set.current_expression.expression_type == 'print_expression':
                assignment_value = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_block.instructions[-1].value = assignment_value
                return InitialState(), data_set
            else: #array index,
                raise UnexpectedIdentifierError(';')
        else:
            raise UnexpectedIdentifierError(';')

    def process_arithmetic_operations(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_arithm_op, data_set.current_expression.bracket_state))
        return AfterExpressionOperator(), data_set



    ###################################################
######### FUNCTION CALL #########################
##################################################
class AfterFunctionCallOpenBracketState(State):
    '''
    example
    ...
    a = (a + myfunc(... <-
    ...

    '''
    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set):
        # function has no parameters
        # check whether this coinside with func declaration should be later
        data_set.subexpressions.pop()
        data_set.current_expression = data_set.subexpressions[-1]
        if not data_set.current_called_function.params: # if param list is empty
            return AfterExpressionOperand(), data_set
        else:
            raise WrongParamsFuncCallError(data_set.current_called_function.name)

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list.insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list.insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterFunctionCallNameState(State):
    def process_opening_bracket(self, data_set):
        function_call = FunctionCall()
        function_call.function = data_set.current_called_function
        data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
        data_set.current_expression = Subexpression()
        data_set.subexpressions.append(data_set.current_expression)
        data_set.current_expression.expression_type = "function_param"
        return AfterFunctionCallOpenBracketState(), data_set


###################################################
##################  FLOW #########################
##################################################

class AfterElseState(State):
    def process_if(self, data_set):
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'predicate'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterIfWhileState(), data_set

    def process_opening_curly_bracket(self, data_set):
        block = Block(data_set.current_block)
        data_set.current_block.instructions[-1].else_branch = block
        data_set.current_block = block
        return InitialState(), data_set


class InitialState(State):
    '''
    example
    ...
    int a = 3;
    <-
    ...

    '''
    def process_opening_curly_bracket(self, data_set):
        newBlock = Block(data_set.current_block)
        data_set.current_block.instructions.append(newBlock)
        data_set.current_block = newBlock
        return InitialState(), data_set

    def process_closing_curly_bracket(self, data_set):
        data_set.current_block = data_set.current_block.parent_block
        if data_set.current_block is None:
            raise UnexpectedIdentifierError('}')
        return InitialState(), data_set

    def process_if(self, data_set):
        data_set.current_block.instructions.append(If())
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'predicate'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterIfWhileState(), data_set

    def process_else(self, data_set):
        if data_set.current_block.instructions and data_set.current_block.instructions[-1].__class__ == If:
            return AfterElseState(), data_set
        else:
            raise UnexpectedIdentifierError('else')

    def process_while(self, data_set):
        current_while_loop = WhileLoop()
        data_set.current_block.instructions.append(current_while_loop)
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'predicate'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterIfWhileState(), data_set

    def process_return(self, data_set):
        data_set.current_block.instructions.append(ReturnExpression())
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'return_expression'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterReturnWordState(), data_set


    def process_identifier(self, data_set):
    # this identifier is earlier declared: it must be function or variable in the
        # current scope or higher
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError(data_set.current_identifier)
        if isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            return AfterSVariableAtStartState(), data_set
        elif isinstance(mapped_to_id, bricks.AbstractArray):
            # assignment
            data_set.current_variable = mapped_to_id
            data_set.current_expression = Subexpression()
            data_set.current_expression.expression_type = 'array_element_at_start'
            data_set.subexpressions.append(data_set.current_expression)
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, Function):
            # e.g. m(); is considered as int anonymous = m()
            #
            data_set.current_called_function = mapped_to_id

            data_set.current_assignment = AssignmentOperator()
            data_set.current_assignment.variable = data_set.current_called_function.returnType()
            data_set.current_block.instructions.append(data_set.current_assignment)
            data_set.current_expression = Subexpression()
            data_set.current_expression.expression_type = 'assignment_value'
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_called_function = mapped_to_id

            return AfterFunctionCallNameState(), data_set

    def process_basic_data_type(self, data_set):
        data_set.current_variable = eval("bricks." + data_set.var_type.capitalize()+'()')
        return AfterSTypeInDeclState(), data_set

    def process_print(self, data_set):
        printOperator = bricks.PrintOperator()
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'print_expression'
        data_set.subexpressions.append(data_set.current_expression)
        data_set.current_block.instructions.append(printOperator)
        return AfterReturnWordState(), data_set     #TODO change this confusing state. all right here


class AfterReturnWordState(State):
    '''
    example
    ...
    return ... <-
    ...

    '''
    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_semicolon(self, data_set):
        raise FunctionMustReturnSomethingError(';')

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list.insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterIfWhileState(State):
    def process_opening_bracket(self, data_set):
        return AfterIfWhileOpenBracketState(), data_set


class AfterIfWhileOpenBracketState(State):
    '''
    example
    ...
    a = 3;
    if (... <-
    ...

    '''
    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set):
        # function has no parameters
        # check whether this coinside with func declaration should be later
        raise EmptyBracketsAreNotAllowedError()

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list\
                .insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.current_expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterIfWhileCondition(State):
    '''
    example
    ...
    int = 3;
    if (a)...<-
    ...
    '''
    def process_opening_curly_bracket(self, data_set):
        # newBlock = Block(data_set.current_block)
        # data_set.current_block.instructions[-1].body = newBlock
        # data_set.current_block = newBlock
        return InitialState(), data_set


###################################################
#############  ASSIGNMENT #########################
##################################################

class AfterAssignmentSign(State):
    '''
    example
    ...
    int b = 5;
    b =...<-
    ...

    '''

    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0,('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set


    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list.insert(0, (mapped_to_id, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_bool_value(self, data_set):
        bool_var = Bool(data_set.current_bool_value)
        data_set.current_expression.expression_list.insert(0, (bool_var, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

class AfterSVariableAtStartState(State):
    '''
    example
    ...
    int b = 5;
    b ...<-
    ...

    '''

    def process_opening_square_bracket(self, data_set):
        return NotArrayError(), data_set

    def process_assignment(self, data_set):
        data_set.current_assignment = AssignmentOperator()
        data_set.current_assignment.variable = data_set.current_variable
        data_set.current_block.instructions.append(data_set.current_assignment)
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'assignment_value'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterAssignmentSign(), data_set

#####################################
###########      Arrays #############
######################################


class AfterArrayAtStartState(State):
    '''

    example:
    int[6] arr;
    ...
    arr <-
    ...

    '''
    def process_opening_square_bracket(self, data_set):
        if not data_set.current_expression:
            data_set.current_expression.expression_type = 'array_element_at_start'
            data_set.current_expression.bracket_state = 0
            data_set.current_expression.expression_list = []

        array_element = bricks.ArrayElement()
        array_element.array = data_set.current_variable
        data_set.current_expression.expression_list.insert(0, (array_element, data_set.current_expression.bracket_state))
        data_set.current_expression = Subexpression()
        data_set.subexpressions.append(data_set.current_expression)
        data_set.current_expression.expression_type = "array_index"
        return AfterArrayOpeningBracketState(), data_set

    def process_semicolon(self, data_set):
        if data_set.current_expression.expression_type == 'return_expression':
            data_set.current_expression.expression_list.\
                insert(0, (data_set.current_variable,
                           data_set.current_expression.bracket_state))
            return_expression = build_expression_tree(data_set.current_expression.expression_list)
            if issubclass(return_expression.get_type(), data_set.current_function.returnType):
                raise TypeMismatchError(return_expression.get_type(), data_set.current_function.returnType) #XXX here we had some troubles
            data_set.subexpressions.pop()
            data_set.current_block.instructions[-1].exp = return_expression
            return InitialState(), data_set
        else:
            raise IllegalArrayOperationError

class AfterArrayOpeningBracketState(State):
    '''

    example:
    int[6] arr;
    ...
    arr[ <-
    ...

    '''
    # def process_number(self, data_set):
    #     data_set.current_variable = data_set.current_block.context.variables[data_set.current_identifier]\
    #         .get(data_set.current_number)
    #     return AfterArrayIndexState(), data_set

    def process_opening_bracket(self, data_set):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if mapped_to_id is None:
            raise UnknownIdentifierError()
        if isinstance(mapped_to_id, AbstractArray):
            data_set.current_variable = mapped_to_id
            return AfterArrayAtStartState(), data_set
        elif isinstance(mapped_to_id, SimpleType):
            data_set.current_variable = mapped_to_id
            data_set.current_expression.expression_list\
                .insert(0, (data_set.current_variable, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(mapped_to_id, Function):
            data_set.current_called_function = mapped_to_id
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set):
        data_set.expression_list.insert(0, (data_set.current_string_literal, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

class AfterArrayIndexState(State):
    '''
    #TODO probably change to AfterOperandState
    example:
    int[6] arr;
    ...
    arr[99 <-
    ...

    '''
    def process_closing_square_bracket(self, data_set):
        return AfterSVariableAtStartState(), data_set


###################################################
##################  DECLARATIONS #########################
##################################################


class AfterArrayDeclOpenSquareBracket(State):
    '''
    example
    ...
    int a = 3
    int[...<-
    ...
    '''
    def process_closing_square_bracket(self, data_set):
        raise ArrayMustHaveFixedSizeError(data_set.current_identifier)

    def process_identifier(self, data_set):
        #TODO implement checking whether identifier is constant
        raise NotImplemented()

    def process_number(self, data_set):
        return AfterArrayDeclSizeState(), data_set

    def process_string_literal(self, data_set):
        raise ArrayMustHaveFixedSizeError(data_set.current_identifier)

class AfterArrayDeclSizeState(State):
    '''
    example
    ...
    int a = 3
    int[8...<-
    ...
    '''
    def process_closing_square_bracket(self, data_set):
        return AfterArrayDeclClosingSquareBracket(), data_set

class AfterArrayDeclClosingSquareBracket(State):
    '''
    example
    ...
    int a = 3
    int[8]...<-
    ...
    '''
    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier, only_this_scope=True)
        if mapped_to_id is None:
            return AfterNameInDeclState(), data_set
        else:
            raise IdentifierAlreadyExistsError()


class AfterFuncArrayCloseBracketState(State):
    def process_comma(self, data_set):
        return AfterFuncDeclOpenBracketState(), data_set

    def process_identifier(self, data_set):
        data_set.current_function.block.context.variables[data_set.current_identifier] = data_set.current_variable
        return AfterFuncParamDeclState(), data_set


class AfterFuncArraySizeState(State):
    def process_closing_square_bracket(self, data_set):
        return AfterFuncArrayCloseBracketState(), data_set


class AfterFuncArrayOpenBracketState(State):
    '''
    example
    ...
    int b = 5;
    int func(int a[ ...<-
    ...
    '''
    def process_number(self, data_set):
        data_set.current_variable = ArrayMetaclass(data_set.current_variable.__class__, data_set.current_number)()
        data_set.current_function.params.append(data_set.current_variable)
        return AfterFuncArraySizeState(), data_set


class AfterFuncParamDeclState(object):
    '''
    example
    ...
    int b = 5;
    int func(int a ...<-
    ...

    '''
    def process_comma(self, data_set):
        return AfterFuncDeclOpenBracketState(), data_set

    def process_closing_bracket(self, data_set):
        return AfterIfWhileCondition(), data_set


class AfterFuncSTypeParamState(State):
    '''
    example
    ...
    int b = 5;
    int func(int ...<-
    ...

    '''
    def process_opening_square_bracket(self, data_set):
        return AfterFuncArrayOpenBracketState(), data_set

    def process_identifier(self, data_set):
        if not searchIdentifier(data_set.current_function.block, data_set.current_identifier, True):
            data_set.current_function.params.append(data_set.current_variable)
            data_set.current_function.block.context.variables[data_set.current_identifier] = data_set.current_variable
            return AfterFuncParamDeclState(), data_set
        else:
            raise SameNameParameterError(data_set.current_identifier)



class AfterFuncDeclOpenBracketState(State):
    '''
    example
    ...
    int b = 5;
    int func( ...<-
    ...

    '''
    def process_basic_data_type(self, data_set):
        data_set.current_variable = eval("bricks." + data_set.var_type.capitalize()+'()')
        return AfterFuncSTypeParamState(), data_set

    def process_closing_bracket(self, data_set): #lem
        # data_set.current_block.context.functions[data_set.current_function.name] = data_set.current_function
        # data_set.current_function.block = Block(data_set.current_block)
        # data_set.current_block = data_set.current_function.block
        # data_set.current_substate = 'function'
        return AfterIfWhileCondition(), data_set


class AfterNameInDeclState(State):
    '''
    example
    ...
    int b = 5;
    int[8] y ...<-
    ...

    '''

    def process_opening_bracket(self, data_set):
        # it's function that returns an array decl
        data_set.current_function = Function()
        data_set.current_block.context.functions[data_set.current_function.name] = data_set.current_function
        data_set.current_function.name = data_set.current_identifier
        data_set.current_function.returnType \
            = ArrayMetaclass(data_set.current_variable.__class__, data_set.current_number)
        data_set.current_function.block = Block(data_set.current_block)
        data_set.current_block = data_set.current_function.block
        return AfterFuncDeclOpenBracketState(), data_set

    def process_semicolon(self, data_set):
        #it's array decl
        data_set.current_variable = eval("bricks." + data_set.var_type.capitalize()+'()')
        data_set.current_variable = bricks.ArrayMetaclass(data_set.current_variable.__class__, data_set.current_number)()
        data_set.current_block.context.variables[data_set.current_identifier] = data_set.current_variable
        return InitialState(), data_set

    def process_assignment(self, data_set):
        raise  NotImplementedError


class AfterNameInSTypeDeclState(State):
    '''
    example
    ...
    int b = 5;
    int c ...<-
    ...

    '''

    def process_opening_bracket(self, data_set):
        # function declaration that returns simple type
        data_set.current_function = Function()
        data_set.current_block.context.functions[data_set.current_identifier] = data_set.current_function
        data_set.current_function.name = data_set.current_identifier
        data_set.current_function.returnType = data_set.current_variable.__class__
        data_set.current_function.block = Block(data_set.current_block)
        data_set.current_block = data_set.current_function.block
        data_set.current_substate = 'function'
        return AfterFuncDeclOpenBracketState(), data_set

    def process_semicolon(self, data_set):
        if data_set.current_variable.get_type() == bricks.Void:
            raise VariableCantBeVoidError()
        else:
            data_set.current_block.context.variables[data_set.current_identifier] = data_set.current_variable
            return InitialState(), data_set

    def process_assignment(self, data_set):
        data_set.current_block.context.variables[data_set.current_identifier] = data_set.current_variable
        data_set.current_assignment = AssignmentOperator()
        data_set.current_assignment.variable = data_set.current_variable
        data_set.current_block.instructions.append(data_set.current_assignment)

        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'assignment_value'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterAssignmentSign(), data_set


class AfterSTypeInDeclState(State):
    '''
    example
    ...
    int b = 5;
    int ...<-
    ...

    '''
    def process_opening_square_bracket(self, data_set):
        return AfterArrayDeclOpenSquareBracket(), data_set

    def process_identifier(self, data_set):
        mapped_to_id = searchIdentifier(data_set.current_block, data_set.current_identifier, only_this_scope=True)
        if mapped_to_id is None:
            return AfterNameInSTypeDeclState(), data_set
        else:
            raise IdentifierAlreadyExistsError()


class Syntan(object):
    '''
    # RESTRICTIONS
    # array size declaration - only number, not constant
    # the same id for function and variable not possible
    # type_checking !!! when 'compiling'
    # do not embrace one operand with brackets
    '''
    basic_data_types = ['int', 'bool', 'string', 'void']

    def __init__(self, source):
        self.source = source

    def parse(self):
        mainFunction = Function()
        lexer = Lexer(self.source)
        curDataSet = CurrentDataSet()
        curDataSet.current_block = mainFunction.block
        state = InitialState()

        while lexer.next_available():
            new_token, position = lexer.next_token()

            if new_token == '{':
                process = state.process_opening_curly_bracket
            elif new_token == '}':
                process = state.process_closing_curly_bracket
            elif new_token == '[':
                process = state.process_opening_square_bracket
            elif new_token == ']':
                process = state.process_closing_square_bracket
            elif new_token == '(':
                process = state.process_opening_bracket
            elif new_token == ')':
                process = state.process_closing_bracket
            elif new_token == ',':
                process = state.process_comma
            elif new_token == ';':
                process = state.process_semicolon
            #reserved words
            elif new_token == 'if':
                process = state.process_if
            elif new_token == 'else':
                process = state.process_else
            elif new_token == 'while':
                process = state.process_while
            elif new_token == 'return':
                process = state.process_return
            elif new_token == 'print':
                process = state.process_print
            # arithmetic operations
            elif new_token in ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=', '!', '&&', '||']:
                process = state.process_arithmetic_operations
                curDataSet.current_arithm_op = new_token
            elif new_token in self.basic_data_types:
                curDataSet.var_type = new_token
                process = state.process_basic_data_type
            elif new_token == '=':
                process = state.process_assignment
            elif new_token.startswith("//") or new_token.startswith("/*"):
                continue
            elif new_token.startswith('"') and new_token.endswith('"'):
                curDataSet.current_string_literal = new_token
                process = state.process_string_literal
            elif new_token.isdigit():
                curDataSet.current_number = int(new_token)
                process = state.process_number
            elif new_token in ['false', 'true']:
                curDataSet.current_bool_value = True if new_token == 'true' else False
                process = state.process_bool_value
            else:
                curDataSet.current_identifier = new_token
                process = state.process_identifier

            try:
                state, curDataSet = process(curDataSet)
            except UnexpectedIdentifierError, ex:
                ex.wrongSymbol = new_token
                ex.position = position
                raise ex
            except UnknownIdentifierError, ex:
                ex.value = new_token
                ex.position = position
                raise ex
            except CompileError, ex:
                ex.position = position
                raise ex
        if isinstance(state, InitialState) and not curDataSet.current_block.parent_block:
            return mainFunction
        else:
            raise EndOfFileReachedError()



#s = Syntan(source)
# try:
# print s.parse()
# except UnknownIdentifierError, e:
#     print '!!! %s' %e

# my_list = ['a', '+', Function(), '+', 'c']
# print build_expression_tree(my_list)