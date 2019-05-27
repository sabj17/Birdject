from unittest import TestCase
import os
from prettytable import PrettyTable
from src.symbol_table import BuildSymbolTableVisitor
from src.grammar import *
from src.lexer import Lexer
from src.parser import Parser
from src.parsetree import BuildASTVisitor
from src.ast import GraphASTVisitor


class TestSymbolTable(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        pass

    def make_table(self, program):
        grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/grammar.txt'))
        program_file = os.path.abspath(os.path.join('../..', 'src/resources/testSymTable.jnr'))
        keyword_file = os.path.abspath(os.path.join('../..', 'src/resources/keywords.txt'))
        token_spec_file = os.path.abspath(os.path.join('../..', 'src/resources/token_spec.txt'))
        grammar = GrammarBuilder.build_grammar_from_file(grammar_file)
        lexer = Lexer(program, keyword_file, token_spec_file)
        tokens = lexer.lex()
        parser = Parser(grammar)
        parse_tree = parser.parse(tokens)
        parse_tree.graph()
        ast = parse_tree.accept(BuildASTVisitor())
        ast.accept(GraphASTVisitor())
        visitor = BuildSymbolTableVisitor()
        ast.accept(visitor)
        symtable = visitor.current_scope
        return symtable


    # The test would failed if any errors is detected in the source program.
    # No specific error is detected but the entire program as a whole.
    def test_big_program(self):
        program = os.path.abspath(os.path.join('../..', 'src/resources/testSymTable.jnr'))
        self.make_table(program)

    def test_symbols_gets_added_to_table(self):
        program = '''
                set window1 to Window();
                '''
        symtable = self.make_table(program)
        self.assertNotEqual(symtable.symbols, None)

    def test_lookup_func1(self):
        program = '''
                set window1 to Window();
                '''
        symtable = self.make_table(program)
        self.assertEqual(symtable.lookup('window1'), 'Window')

    def test_lookup_func2(self):
        program = '''
                set window1 to Window();
                set varName to 123 + 4.56 * 3;
                '''
        symtable = self.make_table(program)
        self.assertEqual(symtable.lookup('varName'), float)

    def test_classScopes_gets_added(self):
        program = '''
                TestClass{
                    set testVar to 123;
                }
                '''
        symtable = self.make_table(program)
        self.assertNotEqual(symtable.lookup('TestClassScope'), None)

    # Does also checks that the funtion changes the type of the formal parameters to the actual.
    def test_lookup_func_in_a_class(self):
        program = '''
                TestClass{
                    function testFunc(x, y){
                        return "test123";
                    }
                }
                run TestClass.testFunc(123, "test");
                '''
        symtable = self.make_table(program)
        class_scope = symtable.lookup('TestClassScope')
        self.assertEqual(class_scope.lookup('testFunc'), [int, str])

    def test_eval_binExpr(self):
        program = '''
                set window1 to Window();
                set varName to (123 + 4.56) * 3 + "test";
                '''
        symtable = self.make_table(program)
        self.assertEqual(symtable.lookup('varName'), str)

    def test_lookup_func_raise_exception(self):
        program = '''
                set window1 to Window();
                set varName to 123 + 4.56;
                '''
        symtable = self.make_table(program)
        with self.assertRaises(NameError):
            symtable.lookup('someName')

    def test_typeEror_in_if_statement1(self):
        program = '''
                        set window1 to Window();
                        set varName to 123 + 4.56;
                        if(window1 < varName){
                        }
                        '''
        with self.assertRaises(TypeError):
            self.make_table(program)

    def test_typeEror_in_if_statement2(self):
        program = '''
                        set window1 to Window();
                        set varName to 123 + 4.56;
                        if(varName){
                        }
                        '''
        with self.assertRaises(TypeError):
            self.make_table(program)

    def test_typeEror_in_if_statement3(self):
        program = '''
                    function testFunc(){
                    return "test123";
                    }
                    
                    if(run testFunc()){
                    }
                    '''
        with self.assertRaises(TypeError):
            self.make_table(program)

    def test_typeEror_function_call1(self):
        program = '''
                    function testFunc(x, y){
                    return "test123";
                    }

                    run testFunc("test");
                    '''
        with self.assertRaises(TypeError):
            self.make_table(program)

    def test_typeEror_function_call2(self):
        program = '''
                    function testFunc(x, y){
                    return "test123";
                    }

                    run testFunc("test", 123);
                    run testFunc(123, "test");
                    '''
        with self.assertRaises(TypeError):
            self.make_table(program)

    def test_typeEror_function_call3(self):
        program = '''
                    set testVar to "Light";
                    run testVar.isTurnedOn();
                    '''
        with self.assertRaises(TypeError):
            self.make_table(program)