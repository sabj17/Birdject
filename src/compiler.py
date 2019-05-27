import os
from codegen import CodeGenVisitor
from src.symbol_table import BuildSymbolTableVisitor
from src.grammar import *
from src.lexer import Lexer
from src.parser import Parser
from src.parsetree import BuildASTVisitor
from src.ast import GraphASTVisitor

wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/input/grammar.txt')
program_file = os.path.join(wd, 'resources/test_programs/TestClassFunctions.jnr')
keyword_file = os.path.join(wd, 'resources/input/keywords.txt')
token_spec_file = os.path.join(wd, 'resources/input/token_spec.txt')
output_path = os.path.join(wd, "resources/output/GeneratedCode/program/program.ino")
parse_tree_path = os.path.join(wd, "resources/output/parse_tree.gv")
ast_path = os.path.join(wd, "resources/output/ast.gv")

# Build grammar
grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

# Lex input
lexer = Lexer(program_file, keyword_file, token_spec_file)
tokens = lexer.lex()

# Parse tokens
parser = Parser(grammar)
parse_tree = parser.parse(tokens)

# Graph parse tree
parse_tree.graph(parse_tree_path)

# Convert parse tree to AST and graph
ast = parse_tree.accept(BuildASTVisitor())
ast.accept(GraphASTVisitor(ast_path))

# Create symbol table and do type checking
visitor = BuildSymbolTableVisitor()
ast.accept(visitor)
symtable = visitor.current_scope

# Generate Ardujeno Code
codeVisitor = CodeGenVisitor(symtable, output_path)
ast.accept(codeVisitor)