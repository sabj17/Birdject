from unittest import TestCase
from src.lexer import Lexer
from src.tokens import Token


class TestLexer(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.lexer = Lexer(program_string='set number1 to 4;')
        cls.tokens_from_program_string = cls.lexer.lex()

    #################
    #     TESTS     #
    #################

    def test_lex_w_individual_tokens(self):
        expected_token = Token('SET', 'set', '1', '0')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[0]))

        expected_token = Token('ID', 'number1', '1', '4')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[1]))

        expected_token = Token('END', ';', '1', '16')
        self.assertEqual(repr(expected_token), repr(self.tokens_from_program_string[4]))

    def test_lex_w_all_tokens(self):
        expected_tokens = [Token('SET', 'set', '1', '0'),
                           Token('ID', 'number1', '1', '4'),
                           Token('TO', 'to', '1', '12'),
                           Token('INTEGER', '4', '1', '15'),
                           Token('END', ';', '1', '16'),
                           Token('$', '$', 'None', 'None')]

        self.assertEqual(repr(self.tokens_from_program_string), repr(expected_tokens))

    def test_lex_finds_amount_of_tokens(self):
        self.assertEqual(len(self.tokens_from_program_string), 6)