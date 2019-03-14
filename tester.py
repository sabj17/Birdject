import re


# rewrite of code: https://docs.python.org/3/library/re.html in the bottom of the page
class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token(type='{self.kind}', value='{self.value}', line='{self.line}', column='{self.column}')"


class Lexer:

    keywords = {'set', 'to', 'if', 'else', 'function', 'run', 'foreach', 'in', 'when', 'return'}
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
        ('STRING', r'["][\w\s]*["]'),  # String value
        ('ASSIGN', r':='),  # Assignment operator
        ('END', r';'),  # Statement terminator
        ('ID', r'[A-Za-z]+'),  # Identifiers
        ('OP', r'[+\-*/]'),  # Arithmetic operators
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH', r'.'),  # Any other character
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
        for mo in re.finditer(tok_regex, self.program):
            # finditer returns an iterator over all non-overlapping matches for the regular expression

            kind = mo.lastgroup  # returns the name of the matched group/kind
            value = mo.group()  # returns value that was matched e.g. "if"
            column = mo.start() - line_start  # where in the where in the code the match was found

            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)

            elif kind == 'ID' and value in self.keywords:
                kind = value

            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue

            elif kind == 'SKIP':
                continue

            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')

            tokens.append(Token(kind, value, line_num, column))

        return tokens


statements = '''
    set hello to "hello there"
'''

lexer = Lexer(program_string=statements)
for token in lexer.lex():
    print(token)
