import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestProduction(TestCase):
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

    #####################
    # all_derives_empty #
    #####################

    def test_all_derives_empty_1(self):
        production = self.grammar.get_rule_from_line(1).RHS
        self.assertFalse(production.all_derives_empty(self.grammar.rules))

    def test_all_derives_empty_2(self):
        production = self.grammar.get_rule_from_line(3).RHS
        self.assertTrue(production.all_derives_empty(self.grammar.rules))

    def test_all_derives_empty_3(self):
        production = self.grammar.get_rule_from_line(4).RHS
        self.assertFalse(production.all_derives_empty(self.grammar.rules))

    def test_all_derives_empty_4(self):
        production = self.grammar.get_rule_from_line(5).RHS
        self.assertTrue(production.all_derives_empty(self.grammar.rules))

    def test_all_derives_empty_5(self):
        production = self.grammar.get_rule_from_line(6).RHS
        self.assertFalse(production.all_derives_empty(self.grammar.rules))

    ########
    # tail #
    ########

    def test_tail_1(self):
        expected_tail = 'C d'
        self.assertEqual(repr(self.grammar.get_rule_from_line(4).RHS.tail('B')), expected_tail)

    def test_tail_2(self):
        expected_tail = 'C D'
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(4).RHS.tail('B')), expected_tail)

    ############
    # is_empty #
    ############

    def test_is_empty_1(self):
        production = self.grammar.get_rule_from_line(4).RHS.tail('B')
        self.assertFalse(production.is_empty())

    def test_is_empty_2(self):
        production = self.grammar.get_rule_from_line(4).RHS.tail('d')
        self.assertTrue(production.is_empty())

    ############
    # get_copy #
    ############

    def test_get_copy_1(self):
        production = self.grammar.get_rule_from_line(2).RHS
        production_copy = production.get_copy(production)
        self.assertEqual(repr(production), repr(production_copy))

    def test_get_copy_2(self):
        production = self.grammar.get_rule_from_line(4).RHS
        production_copy = production.get_copy(production)
        self.assertEqual(repr(production), repr(production_copy))