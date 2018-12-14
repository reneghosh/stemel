from FoxDot import *
import sys
sys.path.append("../")
from stemel.stemel_parser import *
from stemel.stemel import *
from stemel.stemel_foxdot import *
Scale.default = "chromatic"


bass_pattern = "0 0 0"
lead_pattern = ">> 7 7 7 7 10 10 7 0 7 2 0 7 0 12"

b1 >> stplay(jbass, bass_pattern, 0.5, oct=4, lpf=240, room=0.7, mix=0.3, shape=0.1, amp=1.5)
p1 >> stplay(sitar, lead_pattern, 0.25, oct=5, hpf=320, room=0.7, mix=0.3, amp=0.7)
d1 >> play("x-t-")
# print(fdpat(bass_pattern, 1))

while 1:
  sleep(100)


b1 >> bass()
