import re


class Lexer:
    TOKENS = {
        "comment": r'//.*[\n]*',
        "set": "set",
        "to": "to",

        "foreach": "for each",
        "in": "in",
        "is": "is",
        "when": "when",
        "if": "if",
        "else": "else",
        "run": "run",
        "return": "return",
        "and": "and",
        "or": "or",
        "function": "function",

        "input": "input",
        "output": "output",
        "delay": "delay",
        "date": "date",
        "read": "read",
        "write": "write",
        "print": "print",
        "bool": "true|false|on|off",
        "not": 'not',

        "str": r'["][\w\s]*["]',
        "identifier": "[a-z][a-zA-z0-9]*",
        "obj-identifier": "[A-Z][a-zA-z0-9]*",
        "fnum": "[-+]?[0-9]*[.][0-9]+",
        "inum": "[-+]?[1-9][0-9]*|0",
        "lparen": "[\(]",
        "hparen": "[\)]",
        "lcurly": "[\{]",
        "rcurly": "[\}]",

        "plus": "[+]",
        "minus": "[-]",
        "multiply": "[*]",
        "divide": "[/]",
        "modulo": "[%]",
        "assign": "[=]",

        "equals": "==",
        "greater": ">",
        "less": "<"
    }

    def lex(self, string):
        # Create regular expression from all non-terminals
        re_string = "(" + "|".join(self.TOKENS.values()) + ")"
        print(re_string)

        # substitute comment in favor of an empty string
        string = re.sub(self.TOKENS["comment"], '', string)
        #print(string, "\n")

        print(re.findall(r'["][\w\s]*["]', string))
        string = re.sub(r'["][\w\s]*["]', 'str', string)

        # use the regular expression to find the individual tokens
        potential_tokens = re.findall(r'[;]|[a-zA-Z0-9]*', string)
        potential_tokens = list(filter(lambda a: a != '', potential_tokens))
        print(potential_tokens, "\n")

        for string in potential_tokens:
            for key, val in self.TOKENS.items():
                pattern = re.compile(val)
                if pattern.match(string):
                    #print(string, "matches:", key)
                    break


with open("ArdujenoCode\Example.jnr", "r") as jen:
    lexer = Lexer()
    lexer.lex(jen.read(10000))





