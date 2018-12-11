from FoxDot import *
import sys
sys.path.append("../")
from stemel import *
Scale.default = "chromatic"


bass_pattern = "((0-):1):2:2:1 <5 5 7 10-0/>(* 12) :3 :3 :3 :3 10 22 22 22 22 24"
lead_pattern = ">> (7 7 7 7):2 10 10 7 0 7 2 0 7 0 12"

b1 >> stplay(jbass, bass_pattern, 0.5, oct=4, lpf=240, room=0.7, mix=0.3, shape=0.1, amp=1.5)
p1 >> stplay(sitar, lead_pattern, 0.25, oct=5, hpf=320, room=0.7, mix=0.3, amp=0.7)
d1 >> play("x-t-")
# print(fdpat(bass_pattern, 1))

while 1:
  sleep(100)
