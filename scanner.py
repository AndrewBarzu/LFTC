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
    return len(token) >= 1 and token[0].isalpha() and (len(token) == 1 or token[1:].isalnum())

def isNumber(token: str) -> bool:
    return len(token) >= 1 and (token.isnumeric() or (token[0] in ("+", "-") and token[1:].isnumeric()))

def isChar(token: str) -> bool:
    return len(token) == 3 and token[0] == "'" and token[-1] == "'"

def isString(token: str) -> bool:
    return len(token) >= 2 and token[0] == '"' and token[-1] == '"' and (len(token) == 2 or token[1:-1].isalnum())

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
    raise LexicalError("Token `{0}` is not a reserved word or a valid identifier or constant!".format(token))

def scan(filename: str, separator_pattern: re.Pattern, reserved_words: dict) -> Tuple[SymbolTable, List]:
    ST = SymbolTable()
    PIF: List[Tuple[str, Union[Tuple[int, int], 0]]] = list()
    lineNumber = 0
    with open(filename) as f:
        for line in f:
            lineNumber += 1
            i = 0
            for token in separator_pattern.split(line):
                if token == " " or token == "\n" or token == "":
                    continue
                i += 1
                try:
                    tok = detect(token, reserved_words)
                    pos = 0
                    if tok in ("IDENTIFIER", "CONSTANT"):
                        pos = ST.add(token)
                    PIF.append((tok, pos))
                except LexicalError as e:
                    print(str(e) + " on line {0}, token {1}".format(lineNumber, i))

    return ST, PIF

if __name__ == "__main__":
    filename = sys.argv[1]
    reducer = lambda x, y: x + "|" + y
    regex_separators = r'(' + str(reduce(reducer, escaped_operators.keys())) + "|" + str(reduce(reducer, escaped_separators.keys())) + '| |\\r\\n)'
    print(regex_separators)
    regex_separator_pattern = re.compile(regex_separators)
    ST, PIF = scan(filename, regex_separator_pattern, reserved_words)
    print(str(ST))
    print(PIF)
