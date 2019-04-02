from src.grammar import *
from src.token import Token
from src.parser import Parser
import os
from prettytable import PrettyTable
from src.lexer import *


wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/grammar.txt')
grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

code_file = '/home/rasmus/PycharmProjects/Birdject/ArdujenoCode/Example.jnr'

code = '''
    LivingRoom{
        set temp1 to Thermometer();
	    set window1 to pinA10;
    
        function getTemp1(){
		    return temp1 * 5;
	    }
    }
'''


lexer = Lexer(file_path=code_file)
tokens = lexer.lex()

print(",".join([x.kind for x in tokens]))

parser = Parser(grammar)

ptable = PrettyTable(['Nonterminals'] + list(grammar.terminals.keys()))
for val in parser.parse_table:
    row = []
    for key, value in parser.parse_table[val].items():
        row.append(value)
    ptable.add_row([val] + row)

print("\n", ptable)

print("\nMatches:")

parse_tree = parser.parse(tokens)

parse_tree.graph()