from FoxDot import *
import time
import sys
sys.path.append("../lib")
from stemel.stemel import *

"""
Example of using stemel with FoxDot
"""

def print_pattern(pitch, duration, sustain):
  """
  utility method to print the pattern elements
  """
  print("#output")
  print("pitch=%s" % pitch)
  print("duration=%s" % duration)
  print("sustain=%s" % sustain)


def stemel_player(player,pattern,step_size,**args):
  """
  player that wraps foxdot synthdefs and calls them
  with freqency, duration and sustain parameters,
  relaying any other keyword parameter while doing so.
  """
  pattern = Stemel(pattern, step_size)
  # (frequencies,durations, sustains) = replace_rests(*pattern, rest(step_size))
  # print_pattern(*(frequencies,durations, sustains))
  return player(pat.frequencies, dur=pat.durations, sus=pat.sustains, **args)

(frequencies, durations, sustains) = make_pattern("> 0 - 0", 0.5)
print("pitch=%s" % frequencies)
print("duration=%s" % durations)
print("sustain=%s" % sustains)

amplitudes = P(PRand([0.3, 1.0, 0.8, 0.1]), PRand([0.3, 1.0, 0.8, 0.1]))*3.6
Scale.default ="chromatic"
s1 >> stemel_player(sitar, "<< 0 0 7 0 / > 0 7 5 7 12 10 8 7", 0.5, lpf=150, pan=(-1,1), oct=4, echo=1, room=0.5, mix=0.5)

b3 >> stemel_player(bass, "> 0 0 0 0 5 5 0 0 7 7 0 0", 2, amp=0.5,lpf=150, pan=[-1,1], oct=4, echo=0,room=0.5, mix=0.5)
# b1 >> pluck(frequencies, dur=durations, sus=sustains, amp=amplitudes, )
#
p1 >> stemel_player(ambi, ">> 0 * 0 --- ", 0.25, tremolo=4)
