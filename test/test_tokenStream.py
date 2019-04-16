from unittest import TestCase
from src.lexer import Lexer
from src.tokens import TokenStream


class TestTokenStream(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.lexer = Lexer(program_string='set number1 to 4;')
        cls.tokens_from_program_string = cls.lexer.lex()

    def setUp(self):
        self.token_stream = TokenStream(self.tokens_from_program_string)

    #################
    #     TESTS     #
    #################

    def test_peek(self):
        self.assertEqual(self.token_stream.peek(), self.tokens_from_program_string[0])

        self.token_stream.current_index = 4
        self.assertEqual(self.token_stream.peek(), self.tokens_from_program_string[5])

    def test_peek_raise_exception(self):
        self.token_stream.current_index = self.token_stream.length + 1
        with self.assertRaises(Exception):
            self.token_stream.peek()

    def test_advance(self):
        expected_token = self.token_stream.tokens[self.token_stream.current_index + 1]
        advance_token = self.token_stream.advance()
        self.assertEqual(advance_token, expected_token)

        self.token_stream.current_index = 3

        expected_token = self.token_stream.tokens[self.token_stream.current_index + 1]
        advance_token = self.token_stream.advance()
        self.assertEqual(advance_token, expected_token)

        expected_token = self.token_stream.tokens[self.token_stream.current_index]
        advance_token = self.token_stream.advance()
        self.assertNotEqual(advance_token, expected_token)
