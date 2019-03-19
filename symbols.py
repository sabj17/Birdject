class Symbol:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Terminal(Symbol):
    def __init__(self, name):
        super().__init__(name)


class Nonterminal(Symbol):

    def __init__(self, name, productions):
        super().__init__(name)
        self.visitedfollow = False
        self.visitedfirst = False
        self.derivesempty = False
        self.productions = []
        self.productions.append(productions)
        print(name, ": ", productions)

    def addproduction(self, production):
        self.productions.append(production)

    def occurences(self, A):
        ans = []
        for production in self.productions:
            if A in production:
                ans.append(production)
        return ans
