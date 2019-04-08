import os
from unittest import TestCase
from src.grammar import *


class TestLambda(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################

    def test_derives_empty(self):
        symbol = Lambda()
        self.assertTrue(symbol.derives_empty(self.grammar.rules))