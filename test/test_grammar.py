import os
from unittest import TestCase
from src.grammar import GrammarBuilder


class TestGrammar(TestCase):

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

    #################
    # GET_RULES_FOR #
    #################

    def test_get_rules_for_1(self):
        expected_rules = ['A -> a B C d', 'A -> B Q']
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for("A")]

        self.assertListEqual(rules_from_file, expected_rules)

    def test_get_rules_for_2(self):
        expected_rules = ['Q -> q', 'Q -> λ']
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for("Q")]

        self.assertListEqual(rules_from_file, expected_rules)

    def test_get_rules_for_3(self):
        expected_rules = ['S -> A C $']
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for("S")]

        self.assertListEqual(rules_from_file, expected_rules)

    # Should fail because C -> c and C - LAMBDA
    def test_get_rules_for_4(self):
        expected_rules = ['C -> c']
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for("S")]

        self.assertNotEqual(rules_from_file, expected_rules)

    #######################
    # GET_RULES_FROM_LINE #
    #######################

    def test_get_rule_from_line_1(self):
        self.assertEqual(repr(self.grammar.get_rule_from_line(1)), "S -> A C $")

    # Testing that the non-terminal on LHS has be the correct one, see A should be S
    def test_get_rule_from_line_2(self):
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(1)), "A -> A C $")

    def test_get_rule_from_line_3(self):
        self.assertEqual(repr(self.grammar.get_rule_from_line(4)), "A -> a B C d")

    # Testing if it differentiate between a terminal and non-terminal, see D should be d
    def test_get_rule_from_line_4(self):
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(1)), "A -> a B C D")

    # Returns none because the there is no rule on line 10
    def test_get_rule_from_line_5(self):
        self.assertEqual(repr(self.grammar.get_rule_from_line(10)), "None")

    ##############
    # GET_SYMBOL #
    ##############

    # Tests that it can't get a non-terminal if the parameter terminals is passed to the function
    def test_get_symbol_1(self):
        self.assertFalse(self.grammar.get_symbol('A', 'terminals'))

    def test_get_symbol_2(self):
        self.assertTrue(self.grammar.get_symbol('A', 'non-terminals'))

    # Test that the function gives a non-terminal without non-terminals as parameter
    def test_get_symbol_3(self):
        self.assertTrue(self.grammar.get_symbol('A'))

    # Test that it can't get a terminal if the non-terminals is passed as parameter to the function
    def test_get_symbol_4(self):
        self.assertFalse(self.grammar.get_symbol('a', 'non-terminals'))

    def test_get_symbol_5(self):
        self.assertTrue(self.grammar.get_symbol('a', 'terminals'))

    # Test that it outputs a terminal without the terminals as parameter
    def test_get_symbol_6(self):
        self.assertTrue(self.grammar.get_symbol('a'))

    ##############
    # OCCURRENCE #
    ##############

    def test_occurrence_1(self):
        expected_occurrence = ['A -> a B C d', 'A -> B Q', 'B -> b B']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('B')]

        self.assertListEqual(occurrence_from_file, expected_occurrence)

    def test_occurrence_2(self):
        expected_occurrence = ['C -> λ', 'B -> λ', 'Q -> λ']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('λ')]

        self.assertListEqual(occurrence_from_file, expected_occurrence)

    def test_occurrence_3(self):
        expected_occurrence = ['S -> A C $']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('$')]

        self.assertListEqual(occurrence_from_file, expected_occurrence)

    ##############
    # FIRST SETS #
    ##############

    def test_first_1(self):
        first_set = self.grammar.first(self.grammar.rules[0].RHS)
        self.assertEqual(first_set, {'a', 'b', 'c', 'q', '$'}, "First set calculation error")

    def test_first_2(self):
        first_set = self.grammar.first(self.grammar.rules[1].RHS)
        self.assertEqual(first_set, {'c'}, "First set calculation error")

    def test_first_3(self):
        first_set = self.grammar.first(self.grammar.rules[3].RHS)
        self.assertEqual(first_set, {'a'}, "First set calculation error")

    def test_first_4(self):
        first_set = self.grammar.first(self.grammar.rules[5].RHS)
        self.assertEqual(first_set, {'b'}, "First set calculation error")

    def test_first_5(self):
        first_set = self.grammar.first(self.grammar.rules[7].RHS)
        self.assertEqual(first_set, {'q'}, "First set calculation error")

    def test_first_not_equal(self):
        first_set = self.grammar.first(self.grammar.rules[7].RHS)
        self.assertNotEqual(first_set, {'q', '$'}, "First set calculation error")

    ###############
    # FOLLOW SETS #
    ###############

    def test_follow_1(self):
        follow_set = self.grammar.follow('S')
        self.assertEqual(follow_set, set(), "Follow set calculation error")

    def test_follow_2(self):
        follow_set = self.grammar.follow('A')
        self.assertEqual(follow_set, {'$', 'c'}, "Follow set calculation error")

    def test_follow_3(self):
        follow_set = self.grammar.follow('B')
        self.assertEqual(follow_set, {'c', 'q', 'd', '$'}, "Follow set calculation error")

    def test_follow_4(self):
        follow_set = self.grammar.follow('C')
        self.assertEqual(follow_set, {'d', '$'}, "Follow set calculation error")

    def test_follow_5(self):
        follow_set = self.grammar.follow('Q')
        self.assertEqual(follow_set, {'c', '$'}, "Follow set calculation error")

    def test_follow_not_equal(self):
        follow_set = self.grammar.follow('Q')
        self.assertNotEqual(follow_set, {'c', 'a', '$'}, "Follow set calculation error")

    ################
    # PREDICT SETS #
    ################

    def test_predict_1(self):
        predict_set = self.grammar.predict(self.grammar.rules[0])
        self.assertEqual(predict_set, {'a', 'b', 'c', 'q', '$'}, "Predict set calculation error")

    def test_predict_2(self):
        predict_set = self.grammar.predict(self.grammar.rules[1])
        self.assertEqual(predict_set, {'c'}, "Predict set calculation error")

    def test_predict_3(self):
        predict_set = self.grammar.predict(self.grammar.rules[2])
        self.assertEqual(predict_set, {'d', '$'}, "Predict set calculation error")

    def test_predict_4(self):
        predict_set = self.grammar.predict(self.grammar.rules[3])
        self.assertEqual(predict_set, {'a'}, "Predict set calculation error")

    def test_predict_5(self):
        predict_set = self.grammar.predict(self.grammar.rules[4])
        self.assertEqual(predict_set, {'b', 'c', 'q', '$'}, "Predict set calculation error")

    def test_predict_6(self):
        predict_set = self.grammar.predict(self.grammar.rules[5])
        self.assertEqual(predict_set, {'b'}, "Predict set calculation error")

    def test_predict_7(self):
        predict_set = self.grammar.predict(self.grammar.rules[6])
        self.assertEqual(predict_set, {'d', 'c', 'q', '$'}, "Predict set calculation error")

    def test_predict_8(self):
        predict_set = self.grammar.predict(self.grammar.rules[7])
        self.assertEqual(predict_set, {'q'}, "Predict set calculation error")

    def test_predict_9(self):
        predict_set = self.grammar.predict(self.grammar.rules[8])
        self.assertEqual(predict_set, {'c', '$'}, "Predict set calculation error")

    def test_predict_not_equal(self):
        predict_set = self.grammar.predict(self.grammar.rules[8])
        self.assertNotEqual(predict_set, {'c', 'a'}, "Predict set calculation error")
