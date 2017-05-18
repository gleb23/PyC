import logging
logging.basicConfig(level=logging.DEBUG)


STRING_LITERAL_SYMBOL = '"'

IGNORABLE_SYMBOLS = [' ', '\n']

# delimiters that are returned as tokens and consist of one sign only
SINGLE_CHAR_LEXEMES = ['{', '}', ')', '(', '[', ']', '\'', ',', ';']

# delimiters that are returned as tokens and consist of either one or two signs
# mapped values are the ones that can follow key values
DOUBLE_CHAR_LEXEMES = {'<': ['='], '>': ['='], '=': ['='], '!': ['='],
                          '+': ['+', '='], '-': ['-', '='], '/': ['/', '*', '='],
                          '%': ['='], '*': ['='], '|': ['|'], '&': ['&']}

#
COMMENT_SYMBOLS = [('/*', '*/'), ('//', '\n')]


def is_ignorable_delimiter(symbol):
    return symbol in IGNORABLE_SYMBOLS


def can_be_only_1_char_lexeme(symbol):
    return symbol in SINGLE_CHAR_LEXEMES


def is_valid_double_symbol_lexeme(lexeme):
    return lexeme[0] in DOUBLE_CHAR_LEXEMES and \
           lexeme[1] in DOUBLE_CHAR_LEXEMES[lexeme[0]]


def can_be_1_or_2_char_lexeme_beginning(symbol):
    return symbol in DOUBLE_CHAR_LEXEMES


def is_valid_symbol(lexeme):
    return lexeme.isalpha() or lexeme.isdigit


def is_comment_beginning(lexeme):
    return lexeme in [x for x, y in COMMENT_SYMBOLS]


def is_first_comment_closing_symbol(symbol, comment_beginning_lexeme):
    for x, y in COMMENT_SYMBOLS:
        if x == comment_beginning_lexeme and symbol == y[0]:
            return True
    return False


def is_comment_closing_sequence(sequence, comment_beginning_lexeme):
    for x, y in COMMENT_SYMBOLS:
        if x == comment_beginning_lexeme and sequence == y:
            return True
    return False


def scan(source):
    state_machine = StateMachine()
    context = Context()
    for current_symbol in source:
        lexemes = state_machine.process_symbol(current_symbol, context)
        for lexeme in lexemes:
            yield lexeme, (0,0) # position returned is a stub so far
    last_output = state_machine.terminate(context)
    if last_output is not None:
        yield last_output, (0,0) # position returned is a stub so far


class Context(object):
    def __init__(self):
        self.buffer = []
        self.comment_beginning_lexeme = ""


class StateMachine:
    def __init__(self):
        self.state = StateFactory.get_init_state()

    def process_symbol(self, symbol, context):
        lexemes, new_state = self.state.process_symbol(symbol, context)
        if new_state is not None:
            self.state = new_state
        logging.debug("{0} => {1} [{2} Buffer = {3}]"
                      .format(symbol, lexemes, self.state.__class__, context.buffer))
        return lexemes

    def terminate(self, context):
        return None if len(context.buffer) == 0 else "".join(context.buffer)


class State:
    def __init__(self):
        pass

    def process_symbol(self, symbol, context):
        raise TypeError


class InitState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        if is_ignorable_delimiter(symbol):
            return [], None
        if can_be_only_1_char_lexeme(symbol):
            return [symbol], None
        elif can_be_1_or_2_char_lexeme_beginning(symbol):
            context.buffer = [symbol]
            return [], StateFactory.get_waiting_for_second_symbol_state()
        elif STRING_LITERAL_SYMBOL == symbol:
            context.buffer = [symbol]
            return [], StateFactory.get_string_literal_state()
        elif is_valid_symbol(symbol):
            context.buffer = [symbol]
            return [], StateFactory.get_waiting_for_delimiters_state()
        else:
            raise ValueError("Unexpected symbol: {0}".format(symbol))


class WaitingForSecondSymbolState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        double_symbol_lexeme = context.buffer[0] + symbol
        if is_ignorable_delimiter(symbol):
            to_return = context.buffer
            context.buffer = []
            return to_return, StateFactory.get_init_state()
        elif is_valid_double_symbol_lexeme(double_symbol_lexeme):
            context.buffer = []
            if is_comment_beginning(double_symbol_lexeme):
                context.comment_beginning_lexeme = double_symbol_lexeme
                return [], StateFactory.get_comment_state()
            else:
                return [double_symbol_lexeme], StateFactory.get_init_state()
        elif can_be_only_1_char_lexeme(symbol):
            return [context.buffer[0], symbol], StateFactory.get_init_state()
        elif STRING_LITERAL_SYMBOL == symbol:
            to_return = context.buffer
            context.buffer = [symbol]
            return to_return, StateFactory.get_string_literal_state()
        elif is_valid_symbol(symbol):
            to_return = context.buffer
            context.buffer = [symbol]
            return to_return, StateFactory.get_waiting_for_delimiters_state()
        else:
            raise ValueError


class CommentState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        if is_comment_closing_sequence(symbol, context.comment_beginning_lexeme):
            return [], StateFactory.get_init_state()
        elif is_first_comment_closing_symbol(symbol, context.comment_beginning_lexeme):
            context.buffer = [symbol]
            return [], StateFactory.waiting_for_second_comment_closing_symbol()
        else:
            return [], None


class WaitingForSecondCommentClosingSymbolState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        if is_comment_closing_sequence("".join(context.buffer) + symbol, context.comment_beginning_lexeme):
            context.buffer = []
            return [], StateFactory.get_init_state()
        else:
            context.buffer = []
            return [], StateFactory.get_comment_state()


class WaitingForDelimitersState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        if is_ignorable_delimiter(symbol):
            to_return = "".join(context.buffer)
            context.buffer = []
            return [to_return], StateFactory.get_init_state()
        if can_be_only_1_char_lexeme(symbol):
            to_return = "".join(context.buffer)
            context.buffer = []
            return [to_return, symbol], StateFactory.get_init_state()
        elif can_be_1_or_2_char_lexeme_beginning(symbol):
            to_return = "".join(context.buffer)
            context.buffer = [symbol]
            return [to_return], StateFactory.get_waiting_for_second_symbol_state()
        elif STRING_LITERAL_SYMBOL == symbol:
            to_return = "".join(context.buffer)
            context.buffer = [symbol]
            return [to_return], StateFactory.get_string_literal_state()
        elif is_valid_symbol(symbol):
            context.buffer.append(symbol)
            return [], None
        else:
            raise ValueError


class StringLiteralState(State):
    def __init__(self):
        State.__init__(self)

    def process_symbol(self, symbol, context):
        context.buffer.append(symbol)
        if symbol == STRING_LITERAL_SYMBOL:
            to_return = context.buffer
            context.buffer = []
            return ["".join(to_return)], StateFactory.get_init_state()
        else:
            return [], None


class StateFactory:
    def __init__(self):
        pass

    STRING_LITERAL_STATE = StringLiteralState()
    WAITING_FOR_SECOND_COMMENT_CLOSING_SYMBOL_STATE = WaitingForSecondCommentClosingSymbolState()
    INIT_STATE = InitState()
    WAITING_FOR_SECOND_SYMBOL_STATE = WaitingForSecondSymbolState()
    COMMENT_STATE = CommentState()
    WAITING_FOR_DELIMITERS_STATE = WaitingForDelimitersState()

    @staticmethod
    def get_init_state():
        return StateFactory.INIT_STATE

    @staticmethod
    def get_waiting_for_second_symbol_state():
        return StateFactory.WAITING_FOR_SECOND_SYMBOL_STATE

    @staticmethod
    def get_comment_state():
        return StateFactory.COMMENT_STATE

    @staticmethod
    def waiting_for_second_comment_closing_symbol():
        return StateFactory.WAITING_FOR_SECOND_COMMENT_CLOSING_SYMBOL_STATE

    @staticmethod
    def get_waiting_for_delimiters_state():
        return StateFactory.WAITING_FOR_DELIMITERS_STATE

    @staticmethod
    def get_string_literal_state():
        return StateFactory.STRING_LITERAL_STATE
