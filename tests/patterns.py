import sys
sys.path.append("../")
from stemel import *

if __name__ == "__main__":
  s = Stemel("0-0/7 | amp 0.8")
  s2 = s >> 2
  s3 = s << 2
  print(s)
  print(s2)
  print(s3)

  s4 = s.stretch(2)
  print(s4)

  s5 = s + s2
  print(s5)

  s6 = s * 2
  print(s6)

  s7 = S|"0 0 0"
  print(s7)

  s8 = S|"0 - 0 / 7 * *"
  print(s8)

  s9 = S|"(0 0 5) :1 :1 (7 7 12) :2 :2"
  print(s9)
