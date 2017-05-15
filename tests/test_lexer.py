from pyc.lexer import NextTokenNotAvailable

__author__ = 'hlib'

import pyc.lexer as lx
import unittest


class TestLexer(unittest.TestCase):
    def test_lexer(self):
        source = "{\nint a = (3+2);\n{\nprint a;\n}\n}"
        expected_tokens = ['{', 'int', 'a', '=', '(', '3', '+', '2', ')', ';', '{', 'print', 'a', ';', '}', '}']

        tokens = []

        lexer = lx.Lexer(source)
        while lexer.next_available():
            tokens.append(lexer.next_token())

        print tokens
        self.assertEquals([x for x,y in tokens], expected_tokens)

    def test_next_available(self):
        lexer = lx.Lexer("}")
        lexer.next_token()
        is_available = lexer.next_available()

        self.assertEquals(is_available, False)
        with self.assertRaises(NextTokenNotAvailable):
            lexer.next_token()