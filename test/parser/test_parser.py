import os
from unittest import TestCase
from src.grammar import GrammarBuilder
from src.lexer import Lexer
from src.parser import Parser, Stack
from src.tokens import Token


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
        self.lexer = Lexer(program_string='set x to 4;\n'
                                          'set y to 5\n;'
                                          'if(x<y){\n'
                                          '  run print("yay");\n'
                                          '  if(x>y){\n'
                                          '    run print("yay2");\n'
                                          '  }else{\n'
                                          '    run print("nooo");\n'
                                          '  }\n'
                                          '}')
        self.tokens = self.lexer.lex()

        self.stack = Stack()

    def tearDown(self):  # After each test
        pass

    #########
    # tests #
    #########

    def test_parse(self):
        expected_tokens = [Token('SET', 'set', '1', '0'),
                           Token('ID', 'x', '1', '4'),
                           Token('TO', 'to', '1', '6'),
                           Token('INTEGER', '4', '1', '9'),
                           Token('END', ';', '1', '10'),
                           Token('SET', 'set', '2', '0'),
                           Token('ID', 'y', '2', '4'),
                           Token('TO', 'to', '2', '6'),
                           Token('INTEGER', '5', '2', '9'),
                           Token('END', ';', '2', '10'),

                           Token('IF', 'if', '3', '0'),
                           Token('LPAREN', '(', '3', '2'),
                           Token('ID', 'x', '3', '3'),
                           Token('LESS', '<', '3', '4'),
                           Token('ID', 'y', '3', '5'),
                           Token('RPAREN', '(', '3', '6'),
                           Token('LCURLY', '{', '3', '7'),
                           Token('RUN', 'run', '4', '2'),
                           Token('ID', 'print', '4', '6'),
                           Token('LPAREN', '(', '4', '8'),
                           Token('STRING', '"yay"', '4', '9'),
                           Token('RPAREN', ')', '4', '13'),
                           Token('END', ';', '4', '14'),

                           Token('IF', 'if', '5', '0'),
                           Token('LPAREN', '(', '5', '2'),
                           Token('ID', 'x', '5', '3'),
                           Token('GREATER', '>', '3', '4'),
                           Token('ID', 'y', '3', '5'),
                           Token('RPAREN', '(', '5', '6'),
                           Token('LCURLY', '{', '5', '7'),
                           Token('RUN', 'run', '6', '4'),
                           Token('ID', 'print', '6', '8'),
                           Token('LPAREN', '(', '6', '13'),
                           Token('STRING', '"yay2"', '6', '14'),
                           Token('RPAREN', ')', '6', '20'),
                           Token('END', ';', '6', '21'),

                           Token('RCURLY', '}', '7', '2'),
                           Token('ELSE', 'else', '7', '3'),
                           Token('LCURLY', '{', '7', '4'),
                           Token('RUN', 'run', '8', '4'),
                           Token('ID', 'print', '8', '8'),
                           Token('LPAREN', '(', '8', '9'),
                           Token('STRING', '"nooo"', '8', '10'),
                           Token('RPAREN', ')', '8', '16'),
                           Token('END', ';', '8', '17'),
                           Token('RCURLY', '}', '9', '2'),
                           Token('RCURLY', '}', '10', '0'),

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

        # we only need the keys
        nonterminal_dict = {'<stmt>': 0, '<var-dcl>': 0, '<else-clause>': 0, '<for-stmt>': 0, '<if-stmt>': 0,
                            '<stmts>': 0, '<expr>': 0, '<dot-ref>': 0, '<block-body-part>': 0, '<when-stmt>': 0,
                            '<prog>': 0, '<block>': 0, '<block-body>': 0, '<else>': 0, '<id>': 0}
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
