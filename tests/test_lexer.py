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
        ("comments",
            "/*hi*/there//+++\n1",
            ['there', '1']),
        ("2 double signs followed by digit together",
            "+=++3",
            ['+=', '++', '3']),
        ("2 double signs followed by digit with whitespaces",
             "*=     --  \n  0",
             ['*=', '--', '0']),
        ("string literal",
             '="hi"',
             ['=', '"hi"']),
        ("string literal",
             'house*car',
             ['house', '*', 'car']),
    ])
    def test_lexer(self, name, source, expected_tokens):
        tokens = [tokens for tokens, _ in lx.scan(source)]

        self.assertEquals(tokens, expected_tokens)