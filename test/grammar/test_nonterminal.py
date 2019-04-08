import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestNonterminal(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################

    def test_nonterminal_derives_empty(self):
        symbol = self.grammar.get_symbol("A")
        self.assertTrue(symbol.derives_empty(self.grammar.rules))

        symbol = self.grammar.get_symbol("B")
        self.assertTrue(symbol.derives_empty(self.grammar.rules))

    def test_nonterminal_derives_empty_fails_if_not_empty(self):
        symbol = self.grammar.get_symbol("S")
        self.assertFalse(symbol.derives_empty(self.grammar.rules))

        symbol = self.grammar.get_symbol("$")
        self.assertFalse(symbol.derives_empty(self.grammar.rules))
