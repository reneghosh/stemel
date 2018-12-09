from FoxDot import *
import sys
from stemel import *
from stemel.helpers import *
Scale.default = "chromatic"
(pitches, durations, sustains) = fdpat("0 - 0 / > 5 5 5 ", 0.5)
b1 >> bass(pitches, dur=durations, sus=sustains, oct=5, pan=(-1,1))
while 1:
  sleep(100)
