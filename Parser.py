from token import Token
from symbols import Symbol
from symbols import Terminal
from symbols import Nonterminal


class Parser:
    def llparser(self, ts):
        s = Stack()
        s.push("S")
        accepted = False
        while not accepted:
            if s.tos(): #is terminal
                s.tos().match(ts, s.tos())
                if s.tos() == "$":
                    accepted = True
                s.pop()
            else:
                p = 0 #LLtable[TOS( ), ts.peek( )]
                if p == 0:
                    print("Syntax error—no production applicable")
                else:
                    self.apply(p, s)

    def apply(self, p, s):
        a = []
        s.pop()
        for x in range(len(a) - 1, 0):
            s.push(a[x])


class Production:
    # Gotta make a map with integers for indexes for the table

    a = Terminal("a")
    b = Terminal("b")
    c = Terminal("c")
    d = Terminal("d")

    B = Nonterminal("B", [b])
    B.derivesempty = True
    A = Nonterminal("A", [a])
    A.derivesempty = True
    S = Nonterminal("S", [A, B, c])
    S.derivesempty = True

    nonterminals = [S, A, B]
    terminals = [a, b, c, d]
    symbols = [S]
    symbolsIterator = iter(symbols)

    def filltable(self, lltable):
        for A in self.nonterminals:
            for a in self.terminals:
                lltable[A][a] = 0

       # for A in self.nonterminals:
        #    for production in A:  # Get the row index of A
         #       x = 5

    def first(self, symbols):
        for A in self.nonterminals:
            A.visitedfirst = False
        ans = self._internalfirst(symbols)
        return ans

    def _internalfirst(self, symbols):
        ans = []
        if not symbols:  # empty array
            return None
        #if len(symbols) == 1:

        first_symbol = symbols[0]
        symbols.pop(0)  # Removes the first symbol from the array

        # If the symbol is a terminal, it is returned
        if first_symbol in self.terminals:
            ans.append(first_symbol)
            return ans

        # If the symbol is a nonterminal and hasn't been visited first
        print(first_symbol.name)
        if not first_symbol.visitedfirst:
            first_symbol.visitedfirst = True
            # Gets the right hand side and calls it self recursively
            for rhs in first_symbol.productions:
                ans.extend(self._internalfirst([rhs]))
        # If the symbol derives to lambda
        if first_symbol.derivesempty:
            if len(symbols) != 0:
                ans.extend(self._internalfirst(symbols))
            return ans


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        return self.items.pop()

    def tos(self):
        return self.items[len(self.items)-1]


p = Production()
answer = p.first(p.symbols)
print("Completjens")
for x in answer:
    print(x)

