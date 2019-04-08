import os
from unittest import TestCase

from src.grammar import GrammarBuilder, Rule, Production, Nonterminal, Terminal, LAMBDA


class TestGrammarBuilder(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)
        cls.grammar_builder = GrammarBuilder()

    def setUp(self):  # Before each test
        # Set up of manual grammar builder
        self.terminals = ['a', 'b', 'c', 'd', 'q', '$', LAMBDA]
        self.nonterminals = ['S', 'A', 'B', 'C', 'Q']

        self.grammar_builder_manual = GrammarBuilder()
        self.grammar_builder_manual.add_terminals(self.terminals)
        self.grammar_builder_manual.add_nonterminals(self.nonterminals)

        self.grammar_builder_manual.add_rule('S', ['A', 'C', '$'])
        self.grammar_builder_manual.add_rule('C', ['c'])
        self.grammar_builder_manual.add_rule('C', [LAMBDA])
        self.grammar_builder_manual.add_rule('A', ['a', 'B', 'C', 'd'])
        self.grammar_builder_manual.add_rule('A', ['B', 'Q'])
        self.grammar_builder_manual.add_rule('B', ['b', 'B'])
        self.grammar_builder_manual.add_rule('B', [LAMBDA])
        self.grammar_builder_manual.add_rule('Q', ['q'])
        self.grammar_builder_manual.add_rule('Q', [LAMBDA])

        self.builder_rules = self.grammar_builder_manual.rules

    #################
    #     TESTS     #
    #################
    #   test_add_*  #
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

    def test_add_rules_from_file(self):
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        test_builder = GrammarBuilder()
        test_builder.add_rules_from_file(grammar_file)

        self.assertEqual(test_builder.rules, self.builder_rules)

    ###################
    # everything else #
    ###################

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

    def test__format_line(self):
        self.assertEqual(self.grammar_builder._format_line('S -> A, C, $', 1), ('S', ['A', 'C', '$']))
        self.assertEqual(self.grammar_builder._format_line('C -> LAMBDA', 1), ('C', ['λ']))
        self.assertEqual(self.grammar_builder._format_line('A -> a, B, C, d', 1), ('A', ['a', 'B', 'C', 'd']))
        self.assertEqual(self.grammar_builder._format_line('B -> b, B', 1), ('B', ['b', 'B']))
        self.assertEqual(self.grammar_builder._format_line('Q -> q', 1), ('Q', ['q']))

    def test_build(self):
        test_grammar = self.grammar_builder_manual.build()
        self.assertEqual(test_grammar.to_str(), self.grammar.to_str())

    def test__get_production(self):
        terminal_dict = {}
        nonterminal_dict = {}

        for terminal in self.grammar_builder_manual.terminals:
            terminal_dict[terminal] = Terminal(terminal)

        for nonterminal in self.grammar_builder_manual.nonterminals:
            nonterminal_dict[nonterminal] = Nonterminal(nonterminal)

        for rule in self.grammar.rules:
            lhs = rule.LHS.name
            rhs = [symbol.name for symbol in rule.RHS.symbols]
            self.grammar_builder.add_rule(lhs, rhs)

        LHS_1, RHS_1 = self.grammar_builder_manual.rules[0]
        LHS_2, RHS_2 = self.grammar_builder_manual.rules[3]
        LHS_3, RHS_3 = self.grammar_builder_manual.rules[6]
        LHS_4, RHS_4 = self.grammar_builder_manual.rules[7]

        test_production_1 = self.grammar_builder_manual._get_production(RHS_1, terminal_dict, nonterminal_dict)
        test_production_2 = self.grammar_builder_manual._get_production(RHS_2, terminal_dict, nonterminal_dict)
        test_production_3 = self.grammar_builder_manual._get_production(RHS_3, terminal_dict, nonterminal_dict)
        test_production_4 = self.grammar_builder_manual._get_production(RHS_4, terminal_dict, nonterminal_dict)

        self.assertEqual(test_production_1.__str__(), 'A C $')
        self.assertEqual(test_production_2.__str__(), 'a B C d')
        self.assertEqual(test_production_3.__str__(), LAMBDA)
        self.assertNotEqual(test_production_4.__str__(), 'a')
