import os
from unittest import TestCase

from src.grammar import GrammarBuilder, Rule, Production, Nonterminal, Terminal


class TestGrammarBuilder(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)
        cls.grammar_builder = GrammarBuilder()


    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        pass

    def tearDown(self):  # After each test
        pass

    #################
    #     TESTS     #
    #################
    # ADD FUNCTIONS #
    #################

    def test_add_terminals(self):
        self.grammar_builder.add_terminals(self.grammar.terminals)
        test_set = set(self.grammar_builder.terminals)
        self.assertEqual(test_set, {'a', 'b', 'c', 'd', 'q', '$'})

    def test_add_nonterminals(self):
        self.grammar_builder.add_nonterminals(self.grammar.nonterminals)
        test_set = set(self.grammar_builder.nonterminals)
        self.assertEqual(test_set, {'A', 'B', 'C', 'Q', 'S'})

    def test_add_rule(self):
        self.grammar_builder.add_rule(self.grammar.rules[0].LHS, self.grammar.rules[0].RHS)
        start = Nonterminal('S')
        a = Nonterminal('A')
        c = Nonterminal('C')
        dollar = Terminal('$')
        production = Production([a, c, dollar])
        test_rule = Rule(start, production)
        self.assertEqual(self.grammar_builder.rules[0], test_rule)

    def test_build_grammar_from_file(self):
        pass

    def test__find_nonterminals_from_rules(self):
        pass

    def test__find_terminals_from_rules(self):
        pass

    def test_add_rules_from_file(self):
        pass

    def test__format_line(self):
        pass

    def test_build(self):
        pass

    def test__get_production(self):
        pass
