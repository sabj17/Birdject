from unittest import TestCase


class TestStack(TestCase):
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

    #########
    # tests #
    #########

    def test_is_empty(self):
        self.fail()

    def test_push(self):
        self.fail()

    def test_pop(self):
        self.fail()

    def test_top_of_stack(self):
        self.fail()
