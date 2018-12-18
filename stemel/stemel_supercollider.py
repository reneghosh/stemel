from OSC3 import OSCClient, OSCMessage


if __name__ == "__main__":
  client = OSCClient()
  client.connect(("localhost", 57120))
  msg = OSCMessage()
  msg.setAddress("/stemels")
  msg.append(72)
  client.send(msg)
