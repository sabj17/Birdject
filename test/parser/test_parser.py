import os
import unittest
from unittest import TestCase

from prettytable import PrettyTable

from src.grammar import GrammarBuilder, Terminal
from src.lexer import Lexer
from src.parser import Parser, Stack, Tree, Node
from src.tokens import Token, TokenStream


class TestParser(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/grammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(cls.grammar_file)

    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        self.parser = Parser(self.grammar)
        self.lexer = Lexer(program_string='set number1 to 4;')
        self.tokens = self.lexer.lex()

        self.stack = Stack()

    def tearDown(self):  # After each test
        pass

    #########
    # tests #
    #########

    def test_parse(self):
        expected_tokens = [Token('SET', 'set', '1', '0'),
                           Token('ID', 'number1', '1', '4'),
                           Token('TO', 'to', '1', '12'),
                           Token('INTEGER', '4', '1', '15'),
                           Token('END', ';', '1', '16'),
                           Token('$', '$', 'None', 'None')]

        parse_tree = self.parser.parse(self.tokens)
        expected_parse_tree = self.parser.parse(expected_tokens)

        self.assertEqual(parse_tree.__str__(), expected_parse_tree.__str__())

    def test_parse_raise_exception(self):
        test_grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        test_grammar = GrammarBuilder.build_grammar_from_file(test_grammar_file)
        test_parser = Parser(test_grammar)
        with self.assertRaises(Exception):
            test_parser.parse([Token("a", 1, 0, 0), Token("q", 1, 0, 0), Token("$", 1, 0, 0)])

    def test_create_parse_table(self):
        test_grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        test_grammar = GrammarBuilder.build_grammar_from_file(test_grammar_file)
        test_parser = Parser(test_grammar)

        nonterminal_dict = {'A': 0, 'S': 0, 'C': 0, 'B': 0, 'Q': 0}  # we only need the keys
        test_parse_table = test_parser.create_parse_table()

        self.assertEqual(test_parse_table.keys(), nonterminal_dict.keys())

    # Double entry in parse table 'S -> A c | A b'
    def test_create_parse_table_raise_exception(self):
        terminals = ['a', 'c', 'b', '$']
        nonterminals = ['S', 'A']

        grammar_builder_manual = GrammarBuilder()
        grammar_builder_manual.add_terminals(terminals)
        grammar_builder_manual.add_nonterminals(nonterminals)

        grammar_builder_manual.add_rule('S', ['A', 'c', '$'])
        grammar_builder_manual.add_rule('S', ['A', 'b', '$'])
        grammar_builder_manual.add_rule('A', ['a'])

        grammar = grammar_builder_manual.build()

        with self.assertRaises(Exception):
            Parser(grammar)

    # ad hoc exception, it gets 'a' and 'd' as input
    # 1. 'a' is the first terminal, so it goes into rule 1 and derives 'A' into 'a'
    # 2. Now it is expecting 'c' as the next input and match is called because 'd' is TOS and 'd' is a terminal
    # 3. Match is called with 'c' == 'd', which is wrong and throws the exception
    def test_match_raise_exception(self):
        terminals = ['a', 'c', 'b', '$']
        nonterminals = ['S', 'A', 'B']

        grammar_builder_manual = GrammarBuilder()
        grammar_builder_manual.add_terminals(terminals)
        grammar_builder_manual.add_nonterminals(nonterminals)

        grammar_builder_manual.add_rule('S', ['A', 'c', '$'])
        grammar_builder_manual.add_rule('S', ['B', 'b', '$'])
        grammar_builder_manual.add_rule('A', ['a'])

        grammar = grammar_builder_manual.build()
        parser = Parser(grammar)

        with self.assertRaises(Exception):
            parser.parse([Token('a', 1, 0, 0), Token('d', 1, 0, 0)])
