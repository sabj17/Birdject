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
    q = Terminal("q")

    Q = Nonterminal("Q", [q])
    Q.derivesempty = True
    B = Nonterminal("B")
    B.add_production([b, B])
    B.derivesempty = True
    C = Nonterminal("C", [c])
    C.derivesempty = True
    A = Nonterminal("A", [a, B, C, d], [B, Q])
    A.derivesempty = False
    S = Nonterminal("S", [A, C])
    S.derivesempty = False

    nonterminals = [S, A, B, Q, C]
    terminals = [a, b, c, d, q]
    symbols = [S]

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
        ans = self._internalfirst(list(symbols))
        return ans

    def _internalfirst(self, symbols):
        ans = []
        if not symbols:  # empty array
            return set()

        first_symbol = symbols[0]
        symbols.pop(0)  # Removes the first symbol from the array

        # If the symbol is a terminal, it is returned
        if first_symbol in self.terminals:
            ans.append(first_symbol)
            return set(ans)

        # If the symbol is a nonterminal and hasn't been visited first
        if not first_symbol.visitedfirst:
            first_symbol.visitedfirst = True
            # Gets the right hand side and calls it self recursively
            for production in first_symbol.productions:
                if production:
                    ans.extend(self._internalfirst(production))
        # If the symbol derives to lambda
        if first_symbol.symbolderivesempty():
            if symbols:
                ans.extend(self._internalfirst(symbols))
        return set(ans)


    def follow(self, A):
        for a in self.nonterminals:
            a.visitedfollow = False
        return self._internalfollow(A)


    def _internalfollow(self, A):
        ans = []
        if not A.visitedfollow:
            A.visitedfollow = True
            for nonterminal in self.occurences(A):
                for occurence in nonterminal.occurences(A):
                    tail = self._tail(occurence, A)
                    ans.extend(self.first(tail))
                    if self._allderiveempty(tail):
                        ans.extend(self._internalfollow(nonterminal))
        return set(ans)

    def _allderiveempty(self, production):
        for X in production:
            if isinstance(X, Terminal) or not X.derivesempty:
                return False
        return True

    #  Returns a list of all RHS, where nonterminal A is
    def occurences(self, A):
        ans = []
        for nonterminal in self.nonterminals:
            if nonterminal.occurences(A):
                ans.append(nonterminal)
        return ans

    def _tail(self, production, A):
        ans = []
        found = False
        for a in production:
            if found:
                ans.append(a)
            if a.name == A.name:
                found = True
        return ans

    def predict(self, A, production):
        ans = self.first(production)
        for a in ans:
            print("First: ", a)
        if self._allderiveempty(production):
            ans.update(self.follow(A))
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


ans = p.predict(p.B, p.B.productions[0])
for a in ans:
    print("All of dem:", a)


'''
answer = p.first(p.symbols)
print("Completjens")
for x in answer:
    print(x)
'''
