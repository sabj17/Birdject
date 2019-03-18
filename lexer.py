import re
from token import Token
import ArdujenoCode


# rewrite of code: https://docs.python.org/3/library/re.html in the bottom of the page
class Lexer:
    keywords = {'foreach', 'in', 'is', 'when', 'function', 'if', 'else', 'in', 'run', 'return', 'and', 'or', 'not',\
                'function', 'set', 'to', 'input', 'output', 'delay', 'date', 'read', 'write', 'print'}
    token_specification = [
        ('COMMENT', r'//.*[\n]*'),  # Comments

        ('FLOAT', r'\d+[.]\d*'),  # Float
        ('INTEGER',  r'\d+'),  # Integer
        ('STRING',  r'["]([^"]|\")*["]'),  # String value: "Hello World"
        ('BOOL',    r'true|false|on|off'),  # Boolean: true, false or on, off
        ('PIN',     r'pin[A]?[\d]+'),  # Arduino pins: pin15 or pinA3
        ('ID',      r'[a-z][\w]+'),  # Identifiers
        ('OBJ_ID', r'[A-Z][\w]+'),  # Object identifiers

        # Operators
        ('PLUS',    r'[+]'),
        ('MINUS',   r'[\-]'),
        ('MULT',    r'[*]'),
        ('DIVIDE',  r'[/]'),
        ('MODULO',  r'[%]'),
        ('EQUALS',  r'=='),
        ('GREATER', r'[>]'),

        # Allowed symbols
        ('LESS',    r'[<]'),
        ('END',     r';'),
        ('LPAREN',  r'[\(]'),
        ('RPAREN',  r'[\)]'),
        ('LCURLY',  r'[\{]'),
        ('RCURLY',  r'[\}]'),
        ('DOT',     r'[.]'),

        ('NEWLINE', r'\n'),  # Newline
        ('SKIP',    r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH',r'.'),  # Any other character
    ]

    def __init__(self, file_path=None, program_string=None):
        if file_path:
            with open(file_path, "r") as program_file:
                self.program = program_file.read()

        elif program_string:
            self.program = program_string

    def lex(self):
        tokens = []

        token_re = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

        line_num = 1
        line_start = 0
        for match in re.finditer(token_re, self.program):
            # finditer returns an iterator over all non-overlapping matches for the regular expression

            kind = match.lastgroup  # returns the name of the matched group/kind
            value = match.group()  # returns value that was matched e.g. "if"
            column = match.start() - line_start  # where in the code the match was found

            if kind == 'ID':
                if value in self.keywords:  # if the kind was ID where it should have been a keyword
                    kind = value.upper()  # set kind to value/keyword

            elif kind == 'NEWLINE' or kind == 'COMMENT':
                line_start = match.end()  # set the new starting point, to the end of the newline/comment
                line_num += 1  # count up number of lines
                continue

            elif kind == 'SKIP':
                continue

            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')

            tokens.append(Token(kind, value, line_num, column))

        tokens.append(Token('$', '$', -1, -1))
        return tokens


string = 'set string to Thermoboi 32 2.555'
lexer = Lexer(program_string=string)
for token in lexer.lex():
    print(repr(token.__str__()))


