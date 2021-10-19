from typing import Tuple, List, Union

from hashmap import Hashmap as SymbolTable
import sys

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

operators = {
    "+": 14,
    "-": 15,
    "/": 16,
    "*": 17,
    "=": 18,
    "<=": 19,
    "<": 20,
    "==": 21,
    "!=": 22,
    ">": 23,
    ">=": 24,
    "//": 25,
    "&&": 26,
    "||": 27,
    "++": 28,
    "--": 29,
    "%": 30,
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
    return len(token) > 1 and (token.isnumeric() or (token[0] in ("+", "-") and token[1:].isnumeric()))

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
    if token in reserved_words:
        return token
    if isIdentifier(token):
        return "IDENTIFIER"
    if isConstant(token):
        return "CONSTANT"
    raise LexicalError("Token `{0}` is not a reserved word or a valid identifier or constant!".format(token))


def scan(filename: str, reserved_words: dict, operators: dict, separators: dict) -> Tuple[SymbolTable, List]:
    ST = SymbolTable()
    PIF: List[Tuple[str, Union[Tuple[int, int], 0]]] = list()
    word = ""
    lineNumber = 0
    with open(filename) as f:
        for line in f:
            lineNumber += 1
            i = 0
            while i < len(line):
                if line[i] in (' ', '\n'):
                    try:
                        i += 1
                        tok = detect(word, reserved_words)
                        if tok == "NONE":
                            continue
                        pos = 0
                        if tok in ("IDENTIFIER", "CONSTANT"):
                            pos = ST.add(word)
                        PIF.append((tok, pos))
                    except LexicalError as e:
                        print(str(e) + " on line {0}, column {1}".format(lineNumber, i - len(word)))
                    word = ""
                    continue

                if line[i] in separators.keys() or line[i] in operators.keys():
                    try:
                        tok = detect(word, reserved_words)
                        if tok == "NONE":
                            PIF.append((line[i], 0))
                            i += 1
                            continue
                        pos = 0
                        if tok in ("IDENTIFIER", "CONSTANT"):
                            pos = ST.add(word)
                        PIF.append((tok, pos))
                    except LexicalError as e:
                        print(str(e) + " on line {0}, column {1}".format(lineNumber, i - len(word)))
                    PIF.append((line[i], 0))
                    word = ""
                    i += 1

                elif line[i: i + 2] in operators.keys():
                    try:
                        tok = detect(word, reserved_words)
                        if tok == "NONE":
                            PIF.append((line[i: i+2], 0))
                            i += 2
                            continue
                        pos = 0
                        if tok in ("IDENTIFIER", "CONSTANT"):
                            pos = ST.add(word)
                        PIF.append((tok, pos))
                    except LexicalError as e:
                        print(str(e) + " on line {0}, column {1}".format(lineNumber, i - len(word)))
                    PIF.append((line[i: i + 2], 0))
                    word = ""
                    i += 2

                else:
                    word += line[i]
                    i += 1

    return ST, PIF

if __name__ == "__main__":
    filename = sys.argv[1]
    ST, PIF = scan(filename, reserved_words, operators, separators)
    print(str(ST))
    print(PIF)
