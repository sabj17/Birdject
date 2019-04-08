import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestProduction(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #####################
    #       TESTS       #
    #####################
    # all derives empty #
    #####################

    def test_all_derives_empty(self):
        production = self.grammar.get_rule_from_line(3).RHS
        self.assertTrue(production.all_derive_empty(self.grammar.rules))

        production = self.grammar.get_rule_from_line(5).RHS
        self.assertTrue(production.all_derive_empty(self.grammar.rules))

    def test_all_derives_empty_fails_if_not_empty(self):
        production = self.grammar.get_rule_from_line(1).RHS
        self.assertFalse(production.all_derive_empty(self.grammar.rules))

        production = self.grammar.get_rule_from_line(4).RHS
        self.assertFalse(production.all_derive_empty(self.grammar.rules))

        production = self.grammar.get_rule_from_line(6).RHS
        self.assertFalse(production.all_derive_empty(self.grammar.rules))

    ########
    # tail #
    ########

    def test_tail(self):
        expected_tail = 'C d'
        self.assertEqual(repr(self.grammar.get_rule_from_line(4).RHS.tail('B')), expected_tail)

    def test_tail_is_upper_lower_sensitive(self):
        expected_tail = 'C D'
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(4).RHS.tail('B')), expected_tail)

    ############
    # is empty #
    ############
    def test_production_is_empty(self):
        production = self.grammar.get_rule_from_line(4).RHS.tail('d')
        self.assertTrue(production.is_empty())

    def test_production_is_not_empty(self):
        production = self.grammar.get_rule_from_line(4).RHS.tail('B')
        self.assertFalse(production.is_empty())

    ############
    # get copy #
    ############

    def test_get_copy(self):
        production = self.grammar.get_rule_from_line(2).RHS
        production_copy = production.get_copy(production)
        self.assertEqual(repr(production), repr(production_copy))

        production = self.grammar.get_rule_from_line(4).RHS
        production_copy = production.get_copy(production)
        self.assertEqual(repr(production), repr(production_copy))