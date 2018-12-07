from FoxDot import *
import time
sys.path.append("../python")
from stemel.stemel import *

def print_pattern(pitch, duration, sustain):
  print("#output")
  print("pitch=%s" % pitch)
  print("duration=%s" % duration)
  print("sustain=%s" % sustain)

# pat = make_pattern("0 - 0")
# print_pattern(*pat)
pat = make_pattern("0 * 0")
print_pattern(*pat)
# pat = replace_rests(*pat, -1)
# print_pattern(*pat)
# print_pattern(replace_rests(*make_pattern("0 * 0"), rest(0.5)))
