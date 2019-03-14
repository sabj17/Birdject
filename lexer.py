import re
from token import Token


# rewrite of code: https://docs.python.org/3/library/re.html in the bottom of the page
class Lexer:
    keywords = {'for each', 'in', 'is', 'when', 'function', 'if', 'else', 'in', 'run', 'return', 'and', 'or', 'not',\
                'function', 'set', 'to', 'input', 'output', 'delay', 'date', 'read', 'write', 'print'}
    token_specification = [
        ('COMMENT', r'//.*[\n]*'),

        ('NUMBER',  r'\d+(\.\d*)?'),  # Integer or decimal number
        ('STRING',  r'["][^"]*["]'),  # String value
        ('BOOL',    r'true|false|on|off'),  # Boolean
        ('PIN',     r'pin[A]?[\d]+'),  # Identifiers
        ('ID',      r'[a-zA-Z][\w]+'),  # Identifiers

        # Operators
        ('PLUS',    r'[+]'),
        ('MINUS',   r'[\-]'),
        ('MULT',    r'[*]'),
        ('DIVIDE',  r'[/]'),
        ('MODULO',  r'[%]'),
        ('EQUALS',  r'=='),
        ('GREATER', r'[>]'),
        ('LESS',    r'[<]'),

        # Allowed symbols
        ('END',     r';'),  # Statement terminator
        ('LPAREN',  r'[\(]'),
        ('RPAREN',  r'[\)]'),
        ('LCURLY',  r'[\{]'),
        ('RCURLY',  r'[\}]'),
        ('DOT', r'[.]'),

        ('NEWLINE', r'\n'),  # Line endings
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

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

        line_num = 1
        line_start = 0
        for matches in re.finditer(tok_regex, self.program):
            # finditer returns an iterator over all non-overlapping matches for the regular expression

            kind = matches.lastgroup  # returns the name of the matched group/kind
            value = matches.group()  # returns value that was matched e.g. "if"
            column = matches.start() - line_start  # where in the where in the code the match was found

            if kind == 'NUMBER':
                if '.' in value:
                    value = float(value)
                    kind = 'FLOAT'
                else:
                    value = int(value)
                    kind = 'INTEGER'

            elif kind == 'ID':
                if value in self.keywords:  # if there kind was ID where it should have been a keyword
                    kind = value.upper()  # make the value upper case

                elif value[0].isupper():  # if the first letter is upper case
                    kind = 'OBJ-ID'

            elif kind == 'NEWLINE' or kind == 'COMMENT':
                line_start = matches.end()  # set the new starting point, to the end of the newline/comment
                line_num += 1  # count up number of lines
                continue

            elif kind == 'SKIP':
                continue

            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')

            tokens.append(Token(kind, value, line_num, column))

        return tokens


'''
lexer = Lexer("ArdujenoCode/Example.jnr")
for token in lexer.lex():
    print(token)
'''

