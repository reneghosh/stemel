# lark test

from lark import Lark

stemel = '''
start: pattern+

pattern: PATTERN_NAME ":" instruction+

PATTERN_NAME : (NUMBER | WORDZ)+
instruction: note+
           | step+
           | BACKTRACK+

note: NUMBER
    | NUMBER MODIFIER+

MODIFIER: LENGTH | VOLUME

BACKTRACK: "/"
VOLUME: "-" NUMBER
step: "s" 
    | "s" INTEGER
LENGTH: ("_" NUMBER)
WORDZ: (("a".."z") | ("A".."Z"))+
NUMBER: (("0".."9") | ("."))+
INTEGER: ("0".."9")+
WHITESPACE: (" " | "\\n")+

%ignore WHITESPACE

'''
parser = Lark(stemel)

example = '''
  P1: 0 4.2 8_2 5-10.4 2 
  P2: 0 / 0 4 s1 s
'''

tree = parser.parse(example)
print(tree.pretty())

for pattern in tree.children:
  pattern_name = pattern.children[0]
  print("Pattern: %s" % pattern_name.value)
  instruction_list = pattern.children[1:]
  for instructions in instruction_list:
    for instruction in instructions.children:
      if instruction == "/":
        print("\tbacktrack")
      else:
        instruction_type = instruction.data
        if instruction_type == "note":
          print("\tNote %s" % instruction.children[0])
        elif instruction_type == "step":
          if len(instruction.children)>0:
            print("\tstep %s" % instruction.children[0])
          else:
            print("\tstep 1")
        # else:
        #   print("\t%s" % instruction.data)
        #   for sub_instruction in instruction.children:
        #     print("\t%s" % sub_instruction)
