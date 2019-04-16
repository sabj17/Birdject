from unittest import TestCase
from src.lexer import Lexer
from src.tokens import Token


class TestLexer(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.lexer = Lexer(program_string='set x to 4;\n'
                                         'set y to 5;\n'
                                         'if(x<y){\n'
                                         '  run print("yay");\n'
                                         '  if(x>y){\n'
                                         '    run print("yay2");\n'
                                         '  }else{\n'
                                         '    run print("nooo");\n'
                                         '  }\n'
                                         '}')
        cls.tokens_from_program_string = cls.lexer.lex()

    #################
    #     TESTS     #
    #################

    def test_lex_w_individual_tokens(self):
        expected_token = Token('SET', 'set', '1', '0')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[0]))

        expected_token = Token('ID', 'x', '1', '4')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[1]))

        expected_token = Token('END', ';', '1', '10')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[4]))

    def test_lex_w_all_tokens(self):
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
                           Token('RPAREN', ')', '3', '6'),
                           Token('LCURLY', '{', '3', '7'),
                           Token('RUN', 'run', '4', '2'),
                           Token('ID', 'print', '4', '6'),
                           Token('LPAREN', '(', '4', '11'),
                           Token('STRING', '"yay"', '4', '12'),
                           Token('RPAREN', ')', '4', '17'),
                           Token('END', ';', '4', '18'),

                           Token('IF', 'if', '5', '2'),
                           Token('LPAREN', '(', '5', '4'),
                           Token('ID', 'x', '5', '5'),
                           Token('GREATER', '>', '5', '6'),
                           Token('ID', 'y', '5', '7'),
                           Token('RPAREN', ')', '5', '8'),
                           Token('LCURLY', '{', '5', '9'),
                           Token('RUN', 'run', '6', '4'),
                           Token('ID', 'print', '6', '8'),
                           Token('LPAREN', '(', '6', '13'),
                           Token('STRING', '"yay2"', '6', '14'),
                           Token('RPAREN', ')', '6', '20'),
                           Token('END', ';', '6', '21'),

                           Token('RCURLY', '}', '7', '2'),
                           Token('ELSE', 'else', '7', '3'),
                           Token('LCURLY', '{', '7', '7'),
                           Token('RUN', 'run', '8', '4'),
                           Token('ID', 'print', '8', '8'),
                           Token('LPAREN', '(', '8', '13'),
                           Token('STRING', '"nooo"', '8', '14'),
                           Token('RPAREN', ')', '8', '20'),
                           Token('END', ';', '8', '21'),
                           Token('RCURLY', '}', '9', '2'),
                           Token('RCURLY', '}', '10', '0'),

                           Token('$', '$', 'None', 'None')]

        self.assertEqual(repr(self.tokens_from_program_string), repr(expected_tokens))

    def test_lex_finds_amount_of_tokens(self):
        self.assertEqual(len(self.tokens_from_program_string), 48)
