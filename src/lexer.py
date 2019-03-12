import os, re


my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../ArdujenoCode/Example.jnr")
with open(path, "r") as file:
    data = file.readlines()

    TOKENS = {
        "set": "set",
        "to": "to",

        "foreach": "for each",
        "in": "in ",
        "when": "when",
        "if": "if",
        "else": "else",
        "run": "run",
        "return": "return",

        "input": "input",
        "output": "output",
        "delay": "delay",
        "date": "date",
        "read": "read",
        "write": "write",
        "print": "print",
        "bool": "true|false|on|off",
        "not": '!|not',

        "str": r'^"([\w]|[+*/?=:.,;<>&#%()]|[-])*"$',
        "identifier": "[a-z][a-zA-z0-9]*",
        "fnum": "^[-+]?[0-9]*[.][0-9]+",
        "inum": "^[-+]?[1-9][0-9]*$|0",
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
lexer = Lexer()


class Lexer:
    TOKENS = {
        "set": "set",
        "to": "to",

        "foreach": "for each",
        "in": "in ",
        "when": "when",
        "if": "if",
        "else": "else",
        "run": "run",
        "return": "return",

        "input": "input",
        "output": "output",
        "delay": "delay",
        "date": "date",
        "read": "read",
        "write": "write",
        "print": "print",
        "bool": "true|false|on|off",
        "not": '!|not',

        "str": r'^"([\w]|[+*/?=:.,;<>&#%()]|[-])*"$',
        "identifier": "[a-z][a-zA-z0-9]*",
        "fnum": "^[-+]?[0-9]*[.][0-9]+",
        "inum": "^[-+]?[1-9][0-9]*$|0",
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
        TOKENS = {
            "set": "set",
            "to": "to",

            "foreach": "for each",
            "in": "in ",
            "when": "when",
            "if": "if",
            "else": "else",
            "run": "run",
            "return": "return",

            "input": "input",
            "output": "output",
            "delay": "delay",
            "date": "date",
            "read": "read",
            "write": "write",
            "print": "print",
            "bool": "true|false|on|off",
            "not": '!|not',

            "str": r'^"([\w]|[+*/?=:.,;<>&#%()]|[-])*"$',
            "identifier": "[a-z][a-zA-z0-9]*",
            "fnum": "^[-+]?[0-9]*[.][0-9]+",
            "inum": "^[-+]?[1-9][0-9]*$|0",
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
        TOKENS = {
            "set": "set",
            "to": "to",

            "foreach": "for each",
            "in": "in ",
            "when": "when",
            "if": "if",
            "else": "else",
            "run": "run",
            "return": "return",

            "input": "input",
            "output": "output",
            "delay": "delay",
            "date": "date",
            "read": "read",
            "write": "write",
            "print": "print",
            "bool": "true|false|on|off",
            "not": '!|not',

            "str": r'^"([\w]|[+*/?=:.,;<>&#%()]|[-])*"$',
            "identifier": "[a-z][a-zA-z0-9]*",
            "fnum": "^[-+]?[0-9]*[.][0-9]+",
            "inum": "^[-+]?[1-9][0-9]*$|0",
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
        TOKENS = {
            "set": "set",
            "to": "to",

            "foreach": "for each",
            "in": "in ",
            "when": "when",
            "if": "if",
            "else": "else",
            "run": "run",
            "return": "return",

            "input": "input",
            "output": "output",
            "delay": "delay",
            "date": "date",
            "read": "read",
            "write": "write",
            "print": "print",
            "bool": "true|false|on|off",
            "not": '!|not',

            "str": r'^"([\w]|[+*/?=:.,;<>&#%()]|[-])*"$',
            "identifier": "[a-z][a-zA-z0-9]*",
            "fnum": "^[-+]?[0-9]*[.][0-9]+",
            "inum": "^[-+]?[1-9][0-9]*$|0",
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
        potential_tokens = re.findall(r"[\S]+", string)
        print(potential_tokens)

        for string in potential_tokens:
            for key, val in self.TOKENS.items():
                pattern = re.compile(val)
                if pattern.match(string):
                    print(string, "matches:", key)
                    break


# lexer.lex('int i = 10.5 ( ) { } + 5 "hello#jen?(" \n')
for line in data:
    lexer.lex(line)
