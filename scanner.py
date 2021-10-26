import re
from typing import Tuple, List, Union

from hashmap import Hashmap as SymbolTable
import sys
from functools import reduce

class LexicalError(Exception):
    pass

reserved_words = {
    "IDENTIFIER": 0,
    "CONSTANT": 1,
    "main": 2,
    "bool": 3,
    "number": 4,
    "char": 5,
    "string": 6,
    "if": 7,
    "else": 8,
    "for": 9,
    "while": 10,
    "read": 11,
    "write": 12,
    "const": 13,
    "void": 40
}

escaped_operators = {
    "\\+\\+": 28,
    "--": 29,
    "\\+": 14,
    "-": 15,
    "//": 25,
    "/": 16,
    "\\*": 17,
    "<=": 19,
    ">=": 24,
    "==": 21,
    "!=": 22,
    "=": 18,
    "<": 20,
    ">": 23,
    "&&": 26,
    "\\|\\|": 27,
    "%": 30,
}

operators = {
    "+": 14,
    "-": 15,
    "/": 16,
    "*": 17,
    "<=": 19,
    ">=": 24,
    "==": 21,
    "!=": 22,
    "=": 18,
    "<": 20,
    ">": 23,
    "//": 25,
    "&&": 26,
    "||": 27,
    "++": 28,
    "--": 29,
    "%": 30,
}

escaped_separators = {
    "\\[": 31,
    "\\]": 32,
    "\\{": 33,
    "\\}": 34,
    "\\(": 35,
    "\\)": 36,
    ";": 38,
    ",": 39,
}

separators = {
    "[": 31,
    "]": 32,
    "{": 33,
    "}": 34,
    "(": 35,
    ")": 36,
    ";": 38,
    ",": 39,
}

def isIdentifier(token: str) -> bool:
    return token.isidentifier()

def isNumber(token: str) -> bool:
    return len(token) >= 1 and (token.isnumeric() and str(int(token)) == token or (token[0] in ("+", "-") and token[1:].isnumeric() and str(int(token[1:])) == token[1:]))

def isChar(token: str) -> bool:
    return len(token) == 3 and token[0] == "'" and token[-1] == "'"

def isString(token: str) -> bool:
    return len(token) >= 2 and token[0] == '"' and token[-1] == '"'

def isBool(token: str) -> bool:
    return token in ("true", "false")

def isConstant(token: str) -> bool:
    return isNumber(token) or isChar(token) or isString(token) or isBool(token)

def detect(token: str, reserved_words: dict) -> str:
    if token == "":
        return "NONE"
    if token in reserved_words or token in separators or token in operators:
        return token
    if isIdentifier(token):
        return "IDENTIFIER"
    if isConstant(token):
        return "CONSTANT"
    raise LexicalError("Token `{0}` is not a reserved word or a valid identifier or constant".format(token))

def scan(filename: str, separator_pattern: re.Pattern, reserved_words: dict) -> Union[Tuple[SymbolTable, List], None]:
    ST = SymbolTable()
    PIF: List[Tuple[str, Union[Tuple[int, int], 0]]] = list()
    lineNumber = 0
    quoted = ""
    number = ""
    err = False
    with open(filename) as f:
        for line in f:
            lineNumber += 1
            prev = ""
            for token in separator_pattern.split(line):
                if token == "":
                    continue
                if token[0] in ("'", '"') or quoted != "":
                    quoted += token
                    if token[-1] in ("'", '"') and quoted != "\"":
                        token = quoted
                        quoted = ""
                    else:
                        continue
                elif token in ("+", "-"):
                    if prev == "CONSTANT" or prev == "IDENTIFIER":
                        pass
                    else:
                        number += token
                        continue
                elif number in ("+", "-"):
                    if token == "0":
                        char = line.find(token) + 1
                        print("0 can't be preceeded by sign, on line {0}, character {1}".format(lineNumber, char))
                        err = True
                    number += token
                    token = number
                    number = ""

                if token in (" ", "\t", "\n"):
                    continue
                try:
                    tok = detect(token, reserved_words)
                    pos = 0
                    if tok in ("IDENTIFIER", "CONSTANT"):
                        pos = ST.add(token)
                    PIF.append((tok, pos))
                    prev = tok
                except LexicalError as e:
                    char = line.find(token) + 1
                    print(str(e) + ", on line {0}, character {1}".format(lineNumber, char))
                    err = True
    token = quoted
    if token not in (" ", "\t", "\n"):
        try:
            tok = detect(token, reserved_words)
            pos = 0
            if tok in ("IDENTIFIER", "CONSTANT"):
                pos = ST.add(token)
            PIF.append((tok, pos))
        except LexicalError as e:
            char = line.find(token) + 1
            print(str(e) + ", on line {0}, character {1}".format(lineNumber, char))
            err = True
    if not err:
        return ST, PIF

if __name__ == "__main__":
    # filename = sys.argv[1]
    filename = "p1.in"
    reducer = lambda x, y: x + "|" + y
    regex_separators = r'(' + str(reduce(reducer, escaped_operators.keys())) + "|" + str(reduce(reducer, escaped_separators.keys())) + '| |\\t|\\n)'
    regex_separator_pattern = re.compile(regex_separators)
    ret = scan(filename, regex_separator_pattern, reserved_words)
    if ret is not None:
        ST, PIF = ret
        with open("ST.out", "w") as st, open("PIF.out", "w") as pif:
            st.writelines(str(ST))
            pif.writelines(map(lambda tup: str(tup) + "\n", PIF))
            print(str(ST))
            print(PIF)
