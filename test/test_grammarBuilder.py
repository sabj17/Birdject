import os
from unittest import TestCase

from src.grammar import GrammarBuilder, Rule, Production, Nonterminal, Terminal, Symbol, LAMBDA, Grammar


class TestGrammarBuilder(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)
        cls.grammar_builder = GrammarBuilder()

        # Set up of manual grammar builder
        cls.terminals = ['a', 'b', 'c', 'd', 'q', '$', LAMBDA]
        cls.nonterminals = ['S', 'A', 'B', 'C', 'Q']

        cls.grammar_builder_manual = GrammarBuilder()
        cls.grammar_builder_manual.add_terminals(cls.terminals)
        cls.grammar_builder_manual.add_nonterminals(cls.nonterminals)

        cls.grammar_builder_manual.add_rule('S', ['A', 'C', '$'])
        cls.grammar_builder_manual.add_rule('C', ['c'])
        cls.grammar_builder_manual.add_rule('C', [LAMBDA])
        cls.grammar_builder_manual.add_rule('A', ['a', 'B', 'C', 'd'])
        cls.grammar_builder_manual.add_rule('A', ['B', 'Q'])
        cls.grammar_builder_manual.add_rule('B', ['b', 'B'])
        cls.grammar_builder_manual.add_rule('B', [LAMBDA])
        cls.grammar_builder_manual.add_rule('Q', ['q'])
        cls.grammar_builder_manual.add_rule('Q', [LAMBDA])

        cls.builder_rules = cls.grammar_builder_manual.rules


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
        # Construct rule for testing
        S = Nonterminal('S')
        A = Nonterminal('A')
        C = Nonterminal('C')
        dollar = Terminal('$')
        production = Production([A, C, dollar])
        test_rule = Rule(S, production)

        # Get lhs and rhs of rule. Lhs in string and rhs in list of strings. Add as rule to grammar_builder
        lhs = self.grammar.rules[0].LHS.name
        rhs = [symbol.name for symbol in self.grammar.rules[0].RHS.symbols]
        self.grammar_builder.add_rule(lhs, rhs)

        # Unpack grammar_builder rule of index 0
        x, y = self.grammar_builder.rules[0]
        x_nonterminal = Nonterminal(x)
        symbol_list = []

        # Make all strings from rhs into relevant symbol type
        for S in y:
            if S is not '$' and S is not LAMBDA and S.isupper:
                s_symbol = Nonterminal(S)
            else:
                s_symbol = Terminal(S)

            symbol_list.append(s_symbol)

        y_production = Production(symbol_list)
        builder_rule = Rule(x_nonterminal, y_production)
        self.assertEqual(builder_rule.__str__(), test_rule.__str__())

    def test_build_grammar_from_file(self):
        test_grammar = self.grammar_builder_manual.build()
        self.assertEqual(self.grammar.to_str(), test_grammar.to_str())

    def test__find_nonterminals_from_rules(self):
        nonterminals_from_rules = self.grammar_builder_manual._find_nonterminals_from_rules(self.builder_rules)
        self.assertEqual(set(nonterminals_from_rules), set(self.nonterminals))

    def test__find_terminals_from_rules(self):
        terminals_from_rules = self.grammar_builder_manual._find_terminals_from_rules(self.builder_rules,
                                                                                      self.nonterminals)
        self.assertEqual(set(terminals_from_rules), set(self.terminals))

    def test_add_rules_from_file(self):
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        test_builder = GrammarBuilder()
        test_builder.add_rules_from_file(grammar_file)

        self.assertEqual(test_builder.rules, self.builder_rules)

    def test__format_line_1(self):
        test_string = 'S -> A, C, $'
        test_split = self.grammar_builder._format_line(test_string, 1)
        self.assertEqual(test_split, ('S', ['A', 'C', '$']))

    def test__format_line_2(self):
        test_string = 'C -> LAMBDA'
        test_split = self.grammar_builder._format_line(test_string, 1)
        self.assertEqual(test_split, ('C', ['λ']))

    def test__format_line_3(self):
        test_string = 'A -> a, B, C, d'
        test_split = self.grammar_builder._format_line(test_string, 1)
        self.assertEqual(test_split, ('A', ['a', 'B', 'C', 'd']))

    def test__format_line_4(self):
        test_string = 'B -> b, B'
        test_split = self.grammar_builder._format_line(test_string, 1)
        self.assertEqual(test_split, ('B', ['b', 'B']))

    def test__format_line_5(self):
        test_string = 'Q -> q'
        test_split = self.grammar_builder._format_line(test_string, 1)
        self.assertEqual(test_split, ('Q', ['q']))

    def test_build(self):
        pass

    def test__get_production(self):
        pass
