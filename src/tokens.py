class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'Token(type: {self.kind}, value: {self.value}, line: {self.line}, column: {self.column})'

    __repr__ = __str__


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.length = len(tokens)
        self.current_index = -1

    def peek(self):
        if self.current_index < self.length - 1:
            return self.tokens[self.current_index + 1]
        else:
            raise Exception("Reached end of token stream")

    def advance(self):
        if self.length > self.current_index:
            self.current_index += 1
            return self.tokens[self.current_index]
