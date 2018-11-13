# lark test

from lark import Lark

stemel = """
start: pattern+

pattern: PATTERN_NAME \":\" instruction+

instruction: NUMBER

PATTERN_NAME : (NUMBER | LETTER)+
LETTER: ((\"a\"..\"z\") | (\"A\"..\"Z\"))+
NUMBER: (\"0\"..\"9\")+
WHITESPACE: (\" \" | \"\\n\")+

%ignore WHITESPACE

"""
parser = Lark(stemel)

example = "P1: 4 5 2"

print(parser.parse(example).pretty())
