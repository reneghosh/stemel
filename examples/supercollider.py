from FoxDot.lib.OSC3 import OSCClient, OSCMessage
import time
import threading
from stemel.stemel_parser import *
from stemel.stemel import *

def play(client, instrument, pitch, sustain):
  msg = OSCMessage()
  msg.setAddress("/stemel")
  msg.append(instrument)
  msg.append(pitch)
  msg.append(sustain)
  client.send(msg)

class StemelPlayer(threading.Thread):
  def __init__(self, client, stemel_pattern, instrument,step=1):
    self.stemel_pattern = stemel_pattern.stretch(step)
    self.instrument = instrument
    self.client = client
    super(StemelPlayer, self).__init__()

  def run(self):
    runner = lambda pitch, sustain : play(self.client, self.instrument, pitch, sustain)
    self.stemel_pattern.play(runner)


if __name__ == "__main__":
  client = OSCClient()
  client.connect(("localhost", 57120))
  bpm = 140
  step = 60.0/bpm
  StemelPlayer(client, S|">>> (0 0 0-) :1 0 0 0 < 10 7 7 7-", "bassfoundation", step).start()
  StemelPlayer(client, S|">>>>>>7 7 7 7 10 10 7 0 7 2 0 7 0 12 7 12 / 0 * 7 0", "situationsynth", step).start()
