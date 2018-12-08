from stemel.stemel import *
from FoxDot import *
import time
import sys

Scale.default = "chromatic"
Master().room=0.3
Master().mix=0.1

def stemel_player(player,pattern,step_size,**args):
  """
  player that wraps foxdot synthdefs and calls them
  with freqency, duration and sustain parameters,
  relaying any other keyword parameter while doing so.
  """
  pattern = make_pattern(pattern, step_size)
  (frequencies,durations, sustains) = replace_rests(*pattern, rest(step_size))
  return player(frequencies, dur=durations, sus=sustains, **args)


d1 >> play("x-t", sample=1)

b1 >> stemel_player(bass, "0 - 0", 0.5, lpf=100)

b1 >> stemel_player(bass, "5 - 5", 0.5, lpf=100)

s2 >> stemel_player(sitar, "7 7 5 7 12 17 19 ----- 7 - 12 - 7 -- 12 ", 0.25, hpf=100)

s2 >> stemel_player(sitar, "7 - 7 --- / 0 - 0 ---", 0.25, hpf=100)

s2.stop()

while 1:
  time.sleep(100)
