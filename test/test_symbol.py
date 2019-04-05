import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestSymbol(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        pass

    def tearDown(self):  # After each test
        pass

    #        TESTS
    # -----------------------

    def test_derives_empty_1(self):
        symbol = self.grammar.get_symbol('A')
        self.assertTrue(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))

    def test_derives_empty_2(self):
        symbol = self.grammar.get_symbol('S')
        self.assertFalse(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))

    def test_derives_empty_3(self):
        symbol = self.grammar.get_symbol('a')
        self.assertFalse(symbol.derives_empty(self.grammar.get_rules_for(symbol.name)))