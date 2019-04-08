import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestTerminal(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################

    # Can't derive empty since it's a terminal
    def test_terminal_derives_empty(self):
        symbol = self.grammar.get_symbol('a')
        self.assertFalse(symbol.derives_empty(self.grammar.rules))

        symbol = self.grammar.get_symbol('d')
        self.assertFalse(symbol.derives_empty(self.grammar.rules))