import os
import unittest
from unittest import TestCase

from src.grammar import GrammarBuilder


class TestParser(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        grammar_file = os.path.abspath('../src/resources/testgrammar.txt')
        cls.grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        pass

    def tearDown(self):  # After each test
        pass

    #        TESTS
    # -----------------------

    def test_parse(self):
        self.assertTrue(True)

    def test_apply(self):
        self.assertTrue(True)

    def test_match(self):
        self.assertTrue(True)

    def test_create_parse_table(self):
        self.assertTrue(True)
