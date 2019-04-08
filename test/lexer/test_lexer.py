import os
from unittest import TestCase

from src.grammar import GrammarBuilder
from src.lexer import Lexer


class TestLexer(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        program_file = os.path.abspath('../src/resources/Example.jnr')
        lexer = Lexer(file_path=program_file)
        tokens = lexer.lex()

        print()
        print(",".join([str(x) for x in tokens]))

    def test_lex(self):
        pass
