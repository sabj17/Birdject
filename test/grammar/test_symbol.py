import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestSymbol(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################

    def test_derives_empty_1(self):
        symbol = self.grammar.get_symbol('<else-clause>')
        self.assertTrue(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))

    def test_derives_empty_2(self):
        symbol = self.grammar.get_symbol('<var-dcl>')
        self.assertFalse(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))

    def test_derives_empty_3(self):
        symbol = self.grammar.get_symbol('<for-stmt>')
        self.assertFalse(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))
