class Symbol:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Terminal(Symbol):
    def __init__(self, name):
        super().__init__(name)


class Nonterminal(Symbol):
    def __init__(self, name, *args):
        super().__init__(name)
        self.visitedfollow = False
        self.visitedfirst = False
        self.derivesempty = False
        self.productions = []
        for production in args:
            if isinstance(production, list):
                self.productions.append(production)

    def add_production(self, production):
        self.productions.append(production)

    def occurences(self, A):
        ans = []
        for production in self.productions:
            if A in production:
                ans.append(production)
        return ans

    def symbolderivesempty(self):
        for production in self.productions:
            p_derives_empty = True
            for x in production:
                if isinstance(x, Terminal) or not x.derivesempty:
                    p_derives_empty = False

            if p_derives_empty:
                return True

        return False
