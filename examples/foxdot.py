import time
from FoxDot import *
from stemel import *
Scale.default = "chromatic"
Clock.bpm = 100

bass_pattern = S|"> (0 0 0-) :1 :1 < 5 5 7 10 | amp 1.9 1.5 | lpf 120 720 120 250"
b1 >> smlp(bass, bass_pattern, step=0.5, formant=4)

bass_pattern = ">(0 0 0-) :1 :1 < 5 5 7 10 | amp 1.9 1.5 | lpf 120 720 120 250"
b1 >> smls(bass, bass_pattern, step=0.5, formant=4)

d1 >> play("X-^-", sample=5, amp=1.9, shape=0.8, room=0.4)
d2 >> play(" h hht t", sample=1, amp=1.7, shape=0.9, room=0.4)

bass_pattern = S|">>(0 0 0-) :1 :1 < 5 5 7 10 | amp 1.9 1.5 | lpf 120 720 120 250"
b1 >> smlp(bass, bass_pattern, 0.5)

d1.solo()
d2.solo()

d1.stop()
d2.stop()

b1.solo()
b1.stop()

lead_pattern = S|"> 7 7 7 7 10 10 7 0 7 2 0 7 0 12 / 0 * 7 0 | amp 1.3 1.2 1.24 1.4 | formant 3 4 3 6 | bpf 400 100 300 100 | oct 4 5 3 4 / 4 5 | delay 0.01 0.02 0.04"
p1 >> smlp(charm, lead_pattern >> 0, 0.25, shape=0.13)
p2.stop()

p1.solo()

lead_pattern = "<<0---(****)/7---:1/12---:1"
p2 >> smls(blip, lead_pattern, 1, amp=0.3, sus=7, shape=0.5)

p2.solo()

p1.stop()

Clock.clear()

Clock.bpm = 90

d2 >> play("x-t-", sample=2, room=0.7)

d1.solo()

d1.stop()

minor = (0, -1, 0)

rpat = S|"> 0 - 0 0 / 7 - 7 7 / 12 - 12 12 | amp 0.8 0.3 0.5 0.3/0.3/0.3 | formant 2 4 3 2| delay 0.01 0.02 0.04"
s1 >> smlp(dirt, rpat >> 0, 0.5, sus=1, pshift=0, lpf=[190, 190, 2000, 400],echo=0.5)


rpat= S|"7 7 5 7 5 7 4 4/0 0 0 0 0 0 0 0"
rpat= S|"7 7 5 7 5 7 4 4/0"
s2 >> smlp(charm, rpat, 0.5)

s2.solo()

s2.stop()

while 1:
  time.sleep(100)
