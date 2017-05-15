__author__ = 'hlib'

source = '''
{
int a = (3+2);
{
print a;
}
}

'''
# ss = ''' /*a*/


# '''

# for parsing break string into tokens

#delimiters: ' ', '\n', '{', '}', ')', '(', '[', ']', '<', '>', '=', '!', '+', '-', '/', '\"', '\'', '%', '*'

class NextTokenNotAvailable(object):
    pass


class Lexer(object):
    #delimeters that are not returned as tokens
    ignorable_delimiters = [' ', '\n']
    #delimeters that are returned as tokens and consist of one sign only
    single_sign_delimiters = ['{', '}', ')', '(', '[', ']', '\"', '\'', ',', ';']
    #delimeters that are returned as tokens and consist of either one or two signs
    #mapped values are the ones that can follow key values
    double_sign_delimiters = {'<': ['='], '>' : ['='], '=' : ['='], '!' : ['='],
                              '+' : ['+', '='], '-' : ['-', '='], '/' : ['/', '*', '='],
                              '%' : ['='], '*' : ['='], '|' : ['|'], '&' : ['&']}
    current_pos = 0
    current_token_start = 0

    #
    ignoring_list = {'"': '"', '/*': '*/', '//' : '\n'}

    #
    ignoring_sequence = None
    double_sign = None

    def __init__(self, source):
        self.source = source.strip()
        self.last_new_line = -1
        self.n_new_lines = 0 # current symbol in line

    def next_token(self):
        if not self.next_available():
            raise NextTokenNotAvailable()
        to_return = ""
        while self.current_pos < len(self.source) and (to_return == "" or self.ignoring_sequence != None):
            current_sym = self.source[self.current_pos]
            if self.ignoring_sequence == None and self.double_sign == None:
                if current_sym in self.ignorable_delimiters:
                    if current_sym == '\n':
                        self.n_new_lines += 1
                        self.last_new_line = self.current_pos
                    if self.current_pos > self.current_token_start:
                        to_return = self.source[self.current_token_start:self.current_pos]
                    self.current_pos += 1
                    self.current_token_start = self.current_pos
                elif current_sym in self.single_sign_delimiters:
                    if self.current_pos > self.current_token_start:
                        to_return = self.source[self.current_token_start:self.current_pos]
                        self.current_token_start = self.current_pos
                    else:
                        to_return = self.source[self.current_pos]
                        self.current_pos += 1
                        self.current_token_start = self.current_pos
                elif self.double_sign_delimiters.has_key(current_sym):
                    self.double_sign = current_sym
                    if self.current_pos > self.current_token_start:
                        #return token before this symbol
                        to_return = self.source[self.current_token_start:self.current_pos]
                        self.current_token_start = self.current_pos
                    self.current_pos += 1
                else:
                    self.current_pos += 1
            elif self.ignoring_sequence != None:
                to_find = self.ignoring_list[self.ignoring_sequence]
                ind = self.source[self.current_pos:].find(to_find)
                if ind == -1:
                    to_return += self.source[self.current_pos:]
                    self.current_token_start = len(self.source)
                    self.current_pos = self.current_token_start
                else:
                    ind += self.current_pos
                    to_return += self.source[self.current_pos:ind+len(to_find)]
                    self.current_token_start = ind+len(to_find)
                    self.current_pos = self.current_token_start
                self.ignoring_sequence = None
            elif self.double_sign != None:
                if current_sym == '\n':
                    self.n_new_lines += 1
                    self.last_new_line = self.current_pos
                    #delimiter consists of two symbols
                if self.double_sign_delimiters.has_key(self.double_sign) and current_sym in self.double_sign_delimiters[self.double_sign]:
                    to_return = self.double_sign + current_sym
                    self.current_token_start = self.current_pos + 1
                    self.double_sign = None
                #delimiter consists of one symbol
                else:
                    to_return = self.double_sign
                    self.current_token_start = self.current_pos
                    if current_sym in self.single_sign_delimiters:
                        self.double_sign = current_sym
                    elif current_sym in self.ignorable_delimiters:
                        self.double_sign = None
                        self.current_token_start += 1
                    else:
                        self.double_sign = None
                self.current_pos += 1
            if self.ignoring_list.has_key(to_return):
                self.ignoring_sequence = to_return

        return (to_return.strip(), (self.n_new_lines, self.current_pos - self.last_new_line))    #TODO to smth with strip

    def next_available(self):
        return self.current_pos < len(self.source)

# class PreprocessedLexer(Lexer):
#     def __init__(self, token_list):
#         super(PreprocessedLexer, self).__init__()
#         self.token_list = token_list
#         self.current_token_number = 0
#
#     def next_token(self):
#         self.current_token_number += 1
#         return self.token_list[self.current_token_number - 1]
#
#     def next_available(self):
#         return self.current_token_number < len(self.token_list)

# lexer = Lexer(source)
# while lexer.next_available():
#     print lexer.next_token()






