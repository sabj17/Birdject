import os
from unittest import TestCase
from src.grammar import GrammarBuilder
from src.grammar import LAMBDA


class TestRule(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################

    def test_in_RHS_1(self):
        rule = self.grammar.get_rule_from_line(1)
        self.assertTrue(rule.in_RHS('$'))

        rule = self.grammar.get_rule_from_line(3)
        self.assertTrue(rule.in_RHS(LAMBDA))

        rule = self.grammar.get_rule_from_line(4)
        self.assertTrue(rule.in_RHS('d'))

    def test_is_not_in_RHS_4(self):
        rule = self.grammar.get_rule_from_line(3)
        self.assertFalse(rule.in_RHS('c'))

        rule = self.grammar.get_rule_from_line(4)
        self.assertFalse(rule.in_RHS(LAMBDA))

        rule = self.grammar.get_rule_from_line(4)
        self.assertFalse(rule.in_RHS('$'))