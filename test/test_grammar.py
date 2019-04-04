import os
from unittest import TestCase

from src.grammar import GrammarBuilder, Grammar, Rule
from src.parser import Parser


class TestGrammar(TestCase):

    @classmethod
    def setUpClass(self):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')

        self.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

        parser = Parser(self.grammar)

    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        pass

    def tearDown(self):  # After each test
        pass

    def test_get_rules_for(self):
        pass

    def test_get_rule_from_line(self):
        pass

    def test_get_symbol(self):
        pass

    def test_occurrence(self):
        pass

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
