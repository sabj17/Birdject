import os
from codegen.visitor import CodeGenVisitor
from src.symbol_table import BuildSymbolTableVisitor
from src.grammar import *
from src.lexer import Lexer
from src.parser import Parser
from src.parsetree import BuildASTVisitor
from src.ast import GraphASTVisitor

wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/grammar.txt')
program_file = os.path.join(wd, 'resources/Example1.jnr')
keyword_file = os.path.join(wd, 'resources/keywords.txt')
token_spec_file = os.path.join(wd, 'resources/token_spec.txt')
output_path = os.path.join(wd, "resources/program.txt")

# Build grammar
grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

# Lex input
lexer = Lexer(program_file, keyword_file, token_spec_file)
tokens = lexer.lex()

# Parse tokens
parser = Parser(grammar)
parse_tree = parser.parse(tokens)

# Graph parse tree
parse_tree.graph()

# Convert parse tree to AST and graph
ast = parse_tree.accept(BuildASTVisitor())
ast.accept(GraphASTVisitor())

# Create symbol table and do type checking
visitor = BuildSymbolTableVisitor()
ast.accept(visitor)
symtable = visitor.current_scope
print('Global')
print(symtable.symbols)
print('GlobalFunctionScope')
glb = symtable.lookup('GlobalFunctionScope')
print(glb.symbols)
print('ClasseNameScope')
atab = symtable.lookup('ClassNameScope')
print(atab.symbols)
print('FunctionNameScope')
btab = atab.lookup('FunctionNameScope')
print(btab.symbols)

# Generate Ardujeno Code
#codeVisitor = CodeGenVisitor(symtable, output_path)
#ast.accept(codeVisitor)