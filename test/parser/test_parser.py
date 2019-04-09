import os
import unittest
from unittest import TestCase

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

        self.parse_table = self.parser.create_parse_table()
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

    def test_apply(self):
        # start = self.grammar.start_symbol
        # self.stack.push(start)
        # parse_tree = Tree(Node(start, None))
        # ts = TokenStream(self.tokens)
        #
        # tos = self.stack.top_of_stack()
        # if isinstance(tos, Terminal):  # The next symbol is terminal
        #     self.match(ts, tos, parse_tree)
        #     if tos.name == '$':  # EOF symbol reached and loop is stopped
        #         accepted = True
        #     self.stack.pop()
        # else:  # Top of stack is a non terminal
        #     rule_number = self.parse_table[tos.name][ts.peek().kind]
        #     if rule_number == 0:
        #         raise Exception(
        #             f"Syntax error — no production applicable for {tos.name} and {ts.peek().kind}: {ts.peek()}")
        #     else:  # Applies the RHS to the stack
        #         self.apply(rule_number, self.stack, parse_tree)
        #
        #
        # parse_tree = self.parser.parse(self.tokens)
        # self.stack.push(self.grammar.get_rule_from_line(1))
        # tos = self.stack.top_of_stack()
        # rule_number = self.parse_table[tos.name][ts.peek().kind]
        # print("STACK 1:", self.parser.stack)
        # print(self.grammar.get_rule_from_line(1))
        #
        # self.parser.apply(1, self.parser.stack, parse_tree)
        # print("STACK 2:", self.parser.stack)
        pass

    def test_match(self):
        self.assertTrue(True)

    def test_create_parse_table(self):
        self.assertTrue(True)
