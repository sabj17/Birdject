import re
from src.tokens import Token


# rewrite of code: https://docs.python.org/3/library/re.html in the bottom of the page
class Lexer:
    keywords = {'foreach', 'when', 'if', 'else', 'run', 'return', 'and', 'or', 'not', 'function', 'set', 'to'}
    token_specification = [
        ('COMMENT', r'//.*[\n]*'),  # Comments

        # Operators
        ('PLUS',     r'[+]'),
        ('MINUS',    r'[\-]'),
        ('MULT',     r'[*]'),
        ('DIVIDE',   r'[/]'),
        ('MODULO',   r'[%]'),
        ('NOTEQUALS',r'is not'),
        ('EQUALS',   r'is'),
        ('GREATER',  r'[>]'),
        ('LESS',     r'[<]'),

        ('FLOAT',   r'\d+[.]\d*'),  # Float
        ('INTEGER', r'\d+'),  # Integer
        ('STRING',  r'["][^"]*["]'),  # String value: "Hello World"
        ('BOOL',    r'true|false|on|off'),  # Boolean: true, false or on, off
        ('ID',      r'[\w]+'),  # Identifiers

        # Allowed symbols
        ('END',     r';'),
        ('LPAREN',  r'[\(]'),
        ('RPAREN',  r'[\)]'),
        ('LCURLY',  r'[\{]'),
        ('RCURLY',  r'[\}]'),
        ('LSQUARE', r'[\[]'),
        ('RSQUARE', r'[\]]'),
        ('DOT',     r'[.]'),
        ('COMMA',   r'[,]'),

        ('NEWLINE', r'\n'),  # Newline
        ('SKIP',    r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH',r'.'),  # Any other character
    ]

    def __init__(self, program_file=None, program_string=None):
        if program_file:
            with open(program_file, "r") as program_file:
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

        tokens.append(Token('$', '$', None, None))
        return tokens
