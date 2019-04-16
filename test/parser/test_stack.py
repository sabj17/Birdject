import os
from unittest import TestCase

from src.parser import Stack, GrammarBuilder, LAMBDA


class TestStack(TestCase):
    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/grammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(cls.grammar_file)

    @classmethod
    def tearDownClass(cls):  # After all tests
        pass

    def setUp(self):  # Before each test
        self.stack = Stack()
        self.stack.push('$')
        self.stack.push('A')
        self.stack.push('c')
        self.stack.push('Q')
        self.stack.push('b')

    def tearDown(self):  # After each test
        pass

    #########
    # tests #
    #########

    def test_is_empty(self):
        self.assertFalse(self.stack.is_empty())
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_push(self):
        self.stack.push('C')
        self.assertEqual(self.stack.top_of_stack(), 'C')

        self.stack.push('A')
        self.assertEqual(self.stack.top_of_stack(), 'A')

        self.stack.push('a')
        self.assertEqual(self.stack.top_of_stack(), 'a')

        self.stack.push('Q')
        self.assertEqual(self.stack.top_of_stack(), 'Q')

        self.stack.push('q')
        self.assertNotEqual(self.stack.top_of_stack(), 'b')

    def test_pop(self):
        self.assertEqual(self.stack.pop(), 'b')
        self.assertEqual(self.stack.pop(), 'Q')
        self.assertEqual(self.stack.pop(), 'c')
        self.assertEqual(self.stack.pop(), 'A')
        self.assertEqual(self.stack.pop(), '$')

    def test_top_of_stack(self):
        self.assertEqual(self.stack.top_of_stack(), 'b')
        self.stack.pop()
        self.assertEqual(self.stack.top_of_stack(), 'Q')
        self.stack.pop()
        self.assertEqual(self.stack.top_of_stack(), 'c')
        self.stack.pop()
        self.assertEqual(self.stack.top_of_stack(), 'A')
        self.stack.pop()
        self.assertEqual(self.stack.top_of_stack(), '$')
        self.stack.push('B')
        self.assertNotEqual(self.stack.top_of_stack(), 'A')
