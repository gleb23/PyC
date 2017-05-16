import context
import pyc.lexer as lx
import unittest
from parameterized import parameterized

__author__ = 'hlib'


class TestLexer(unittest.TestCase):
    @parameterized.expand([
        ("simple",
            "{\nint a = (3+2);\n{\nprint a;\n}\n}",
            ['{', 'int', 'a', '=', '(', '3', '+', '2', ')', ';', '{', 'print', 'a', ';', '}', '}']),
        ("simple one line",
            "{int a = (3+2);{print a;}}",
            ['{', 'int', 'a', '=', '(', '3', '+', '2', ')', ';', '{', 'print', 'a', ';', '}', '}']),
        ("simple with random whitespaces",
            "{    int      a    =(      3+2)       ;{  print a\n\n\n\n\n;                      }}",
            ['{', 'int', 'a', '=', '(', '3', '+', '2', ')', ';', '{', 'print', 'a', ';', '}', '}']),

        ("expression with array",
            "a[2-2/3*7%2]=0;",
            ['a', '[', '2', '-', '2', '/', '3', '*', '7', '%', '2', ']', '=', '0', ';']
         ),

        #FIXME
        # ("string literal",
        #      '="hi"',
        #      ['=', '"hi"']),
        # ("string literal",
        #      'house*car',
        #      ['house', '*', 'car']),
    ])
    def test_lexer(self, name, source, expected_tokens):
        tokens = []
        lexer = lx.Lexer(source)
        while lexer.next_available():
            tokens.append(lexer.next_token())

        self.assertEquals([x for x,y in tokens], expected_tokens)

    def test_next_available(self):
        lexer = lx.Lexer("}")
        lexer.next_token()
        is_available = lexer.next_available()

        self.assertEquals(is_available, False)
        with self.assertRaises(lx.NextTokenNotAvailable):
            lexer.next_token()