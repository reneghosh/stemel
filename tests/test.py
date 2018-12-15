from FoxDot import *
import sys
sys.path.append("../")
from stemel import *
Scale.default = "chromatic"
Clock.bpm = 100

d1 >> play("x-t-", sample=6, amp=0.9, room=0.5, mix=0.2, bpf=390)

d1.stop()

bass_pattern = "> (0 0 0-) :1 :1 0 0 < 10 7 | amp 1.2 0.9 | lpf 70 220 70 150 | formant 2 2 6 2"
b1 >> stplay(bass, bass_pattern, 0.5, room=0.5, mix=0.1)

b1.stop()

b1.solo()

lead_pattern = "> 7 7 7 7 10 10 7 0 7 2 0 7 0 12 / 0 * 7 0 | amp 0.2 0.5 0.1 | sus 0.7 | formant 1 4 3 4 | lpf 400 800 300 2000"
p1 >> stplay(pluck, lead_pattern, 0.25, shape=0.1)

while 1:
  sleep(100)
