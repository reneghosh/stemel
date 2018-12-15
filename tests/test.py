from FoxDot import *
import sys
sys.path.append("../")
from stemel import *
Scale.default = "chromatic"
Clock.bpm = 100

bass_pattern = ">0 0 0- 0 0 0- 0 0 0- 0 0 < 10 7 | amp 0.8 0.4 | oct 3 5 4 | lpf 70 400 70"
lead_pattern = ">> 7 7 7 7 10 10 7 0 7 2 0 7 0 12 | amp 0.1 0.2 0.4 0.9 | delay 0.1 -0.1 | formant 1 4 3 5 2"

b1 >> stplay(sitar, bass_pattern, 0.5)
p1 >> stplay(pluck, lead_pattern, 0.25, hpf=320, room=0.7, mix=0.3)
d1 >> play("x-[tt]-", sample=2)
# print(fdpat(bass_pattern, 1))



while 1:
  sleep(100)
