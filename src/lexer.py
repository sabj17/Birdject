import re
from src.tokens import Token
import csv



class Lexer:

    def __init__(self, program, keyword_file, token_spec_file):
        # keyword_file format: keyword1 \n keyword2
        # token_spec_file format: name1, re1 \n name2, re1

        with open(keyword_file, 'r') as k_file:
            self.keywords = [keyword for keyword in k_file.read().splitlines()]

        with open(token_spec_file, 'r') as ts_file:
            reader = csv.reader(ts_file, delimiter=':', skipinitialspace=True)
            self.token_specification = [(x, y) for x, y in reader]

        # If it is a file use it's contents as the program, else use the input directly
        try:
            with open(program, "r") as program_file:
                self.program = program_file.read()
        except FileNotFoundError:
            self.program = program


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
                    if value == 'is':
                        kind = 'EQUALS'

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
