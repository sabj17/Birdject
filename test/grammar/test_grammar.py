import os
from unittest import TestCase
from src.grammar import GrammarBuilder, LAMBDA


class TestGrammar(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    #################
    #     TESTS     #
    #################
    # get rules for #
    #################

    def test_get_rules_for_1(self):
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for('<stmts>')]
        expected_rules = ['<stmts> -> <stmt> <stmts>', '<stmts> -> λ']
        self.assertListEqual(rules_from_file, expected_rules)

        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for('<else>')]
        expected_rules = ['<else> -> <block>', '<else> -> <if-stmt>']
        self.assertListEqual(rules_from_file, expected_rules)

        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for('<when-stmt>')]
        expected_rules = ['<when-stmt> -> WHEN LPAREN <expr> RPAREN <block>']
        self.assertListEqual(rules_from_file, expected_rules)

    def test_get_rules_for_is_sensitive_to_upper_and_lower_case(self):
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for('<block-body-part>')]
        expected_rules = ['<block-body-part> -> <FOR-STMT>',
                          '<BLOCK-BODY-PART> -> <if-stmt>',
                          '<block-body-part> -> <var-dcl>']
        self.assertNotEqual(rules_from_file, expected_rules)

    def test_get_rules_for_fails_if_a_rule_is_missing(self):
        rules_from_file = [(repr(rule)) for rule in self.grammar.get_rules_for('<id>')]
        expected_rules = ['<id> -> λ']
        self.assertNotEqual(rules_from_file, expected_rules)

    #######################
    # get rules from line #
    #######################

    def test_get_rule_from_line(self):
        self.assertEqual(repr(self.grammar.get_rule_from_line(1)), '<prog> -> <stmts> $')
        self.assertEqual(repr(self.grammar.get_rule_from_line(4)), '<stmt> -> <when-stmt>')
        self.assertEqual(repr(self.grammar.get_rule_from_line(10)), '<else-clause> -> λ')

    def test_get_rule_from_line_fails_if_not_exact_match(self):
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(1)), '<stmts> -> <stmt> <stmts>')
        self.assertNotEqual(repr(self.grammar.get_rule_from_line(4)), '<block-body> -> λ')

    ##############
    # get symbol #
    ##############

    def test_get_symbol(self):
        self.assertTrue(self.grammar.get_symbol('<when-stmt>'))
        self.assertTrue(self.grammar.get_symbol('WHEN'))

    def test_get_symbol_w_matching_second_parameter(self):
        self.assertTrue(self.grammar.get_symbol('WHEN', 'terminals'))
        self.assertTrue(self.grammar.get_symbol('<when-stmt>', 'non-terminals'))

    def test_get_symbol_fails_w_second_parameter_not_matching(self):
        self.assertFalse(self.grammar.get_symbol('<when-stmt>', 'terminals'))
        self.assertFalse(self.grammar.get_symbol('WHEN', 'non-terminals'))

    ##############
    # occurrence #
    ##############

    def test_occurrence(self):
        expected_occurrence = ['<stmt> -> <for-stmt>', '<block-body-part> -> <for-stmt>']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('<for-stmt>')]
        self.assertListEqual(occurrence_from_file, expected_occurrence)

        expected_occurrence = ['<stmts> -> λ', '<else-clause> -> λ', '<block-body> -> λ', '<dot-ref> -> λ']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('λ')]
        self.assertListEqual(occurrence_from_file, expected_occurrence)

        expected_occurrence = ['<prog> -> <stmts> $']
        occurrence_from_file = [(repr(occurrence)) for occurrence in self.grammar.occurrence('$')]
        self.assertListEqual(occurrence_from_file, expected_occurrence)

    ##############
    # first sets #
    ##############

    def test_first_1(self):
        first_set = self.grammar.first(self.grammar.rules[0].RHS)
        self.assertEqual(first_set, {'WHEN', 'SET', 'FOREACH', 'IF', '$'}, 'First set calculation error')

    def test_first_2(self):
        first_set = self.grammar.first(self.grammar.rules[2].RHS)
        self.assertEqual(first_set, set(), 'First set calculation error')

    def test_first_3(self):
        first_set = self.grammar.first(self.grammar.rules[6].RHS)
        self.assertEqual(first_set, {'SET'}, 'First set calculation error')

    def test_first_4(self):
        first_set = self.grammar.first(self.grammar.rules[10].RHS)
        self.assertEqual(first_set, {'LCURLY'}, 'First set calculation error')

    def test_first_5(self):
        first_set = self.grammar.first(self.grammar.rules[13].RHS)
        self.assertEqual(first_set, {'WHEN'}, 'First set calculation error')

    def test_first_not_equal(self):
        first_set = self.grammar.first(self.grammar.rules[18].RHS)
        self.assertNotEqual(first_set, {'q', '$'}, 'First set calculation error')

    ###############
    # follow sets #
    ###############

    def test_follow_1(self):
        follow_set = self.grammar.follow('<stmts>')
        self.assertEqual(follow_set, {'$'}, 'Follow set calculation error')

    def test_follow_2(self):
        follow_set = self.grammar.follow('<for-stmt>')
        self.assertEqual(follow_set, {'WHEN', 'RCURLY', 'SET', 'IF', 'FOREACH', '$'}, 'Follow set calculation error')

    def test_follow_3(self):
        follow_set = self.grammar.follow('<if-stmt>')
        self.assertEqual(follow_set, {'IF', 'FOREACH', 'WHEN', 'RCURLY', 'SET', '$'}, 'Follow set calculation error')

    def test_follow_4(self):
        follow_set = self.grammar.follow('<else-clause>')
        self.assertEqual(follow_set, {'FOREACH', 'SET', 'IF', 'RCURLY', 'WHEN', '$'}, 'Follow set calculation error')

    def test_follow_5(self):
        follow_set = self.grammar.follow('<else>')
        self.assertEqual(follow_set, {'FOREACH', 'SET', 'IF', 'RCURLY', 'WHEN', '$'}, 'Follow set calculation error')

    def test_follow_not_equal(self):
        follow_set = self.grammar.follow('<var-dcl>')
        self.assertNotEqual(follow_set, {'<dot-ref>'})

    ################
    # predict sets #
    ################

    def test_predict_1(self):
        predict_set = self.grammar.predict(self.grammar.rules[0])
        self.assertEqual(predict_set, {'WHEN', 'SET', 'FOREACH', 'IF', '$'}, 'Predict set calculation error')

    def test_predict_2(self):
        predict_set = self.grammar.predict(self.grammar.rules[1])
        self.assertEqual(predict_set, {'WHEN', 'SET', 'FOREACH', 'IF'}, 'Predict set calculation error')

    def test_predict_3(self):
        predict_set = self.grammar.predict(self.grammar.rules[2])
        self.assertEqual(predict_set, {'$'}, 'Predict set calculation error')

    def test_predict_4(self):
        predict_set = self.grammar.predict(self.grammar.rules[3])
        self.assertEqual(predict_set, {'WHEN'}, 'Predict set calculation error')

    def test_predict_5(self):
        predict_set = self.grammar.predict(self.grammar.rules[4])
        self.assertEqual(predict_set, {'FOREACH'}, 'Predict set calculation error')

    def test_predict_6(self):
        predict_set = self.grammar.predict(self.grammar.rules[5])
        self.assertEqual(predict_set, {'IF'}, 'Predict set calculation error')

    def test_predict_7(self):
        predict_set = self.grammar.predict(self.grammar.rules[6])
        self.assertEqual(predict_set, {'SET'}, 'Predict set calculation error')

    def test_predict_8(self):
        predict_set = self.grammar.predict(self.grammar.rules[7])
        self.assertEqual(predict_set, {'IF'}, 'Predict set calculation error')

    def test_predict_9(self):
        predict_set = self.grammar.predict(self.grammar.rules[8])
        self.assertEqual(predict_set, {'ELSE'}, 'Predict set calculation error')

    def test_predict_not_equal(self):
        predict_set = self.grammar.predict(self.grammar.rules[8])
        self.assertNotEqual(predict_set, {'<for-stmt>', '<if-stmt>'}, 'Predict set calculation error')
