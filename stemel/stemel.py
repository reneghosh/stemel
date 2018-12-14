from stemel.stemel_parser import *

class Filter:
  """
  Class to hold filters.
  The filter is a name and a pattern.
  """
  def __init__(self, name, pattern):
    self.name = name
    self.pattern = pattern
  def __repr__(self):
    return "[Filter %s, pattern=%s]" % (self.name, self.pattern)

def make_rest(step_size):


  """
  this method constructs a placeholder for a rest note
  """
  return {"rest":step_size}

# from FoxDot import *
def separate(notes):
  """
  separate a score of notes into a tuple of
  frequencies, sustains and durations.
  """
  frequencies = []
  durations = []
  sustains = []
  if len(notes)==0:
    return ([],[])
  length = len(max(notes, key = lambda x: len(x)))
  counter = 0
  for i in range(0, length):
    freq_buffer = []
    dur_buffer = []
    sus_buffer = []
    for voice_line in notes:
      if len(voice_line)>0:
        freq_buffer.append(voice_line[counter % len(voice_line)]['frequency'])
        sus_buffer.append(voice_line[counter % len(voice_line)]['sustain'])
        dur_buffer.append(voice_line[counter % len(voice_line)]['duration'])
    frequencies.append(freq_buffer)
    durations.append(dur_buffer)
    sustains.append(sus_buffer)
    counter += 1
  return (frequencies, durations, sustains)

def process(commands):
  """
  process a list of commands,
  concatenating all buffers that
  aren't functions into the main pitch-duration-sustain buffer
  """
  main_buffer = []
  other_buffers = []
  cursor = 0
  for command in commands:
    if command.name == "score":
      main_buffer += command.pattern
    else:
      other_buffers.append(command)
  return (main_buffer[0], main_buffer[1], main_buffer[2], other_buffers)

def make_pattern(score, step_size):
  """
  Take a score inputted as a line of text and a step size (0.25 default)
  and return a tuple of frequencies, sustains and durations
  """
  def is_number(note):
    """
    test is note is a number
    """
    try:
      float(note)
      return True
    except ValueError:
      return False
  commands = []
  buffers = parse_line(score)
  for buffer in buffers:
    polyvals=[]
    vals = []
    polyvals.append(vals)
    oct = 0
    amplitude = 1.0
    counter = 0
    type_name = "score"
    for note in buffer:
      note = note.strip()
      note = note.lower()
      if note=='-':
        # carry previous note one more step
        lookback_counter = len(vals)-1
        while (lookback_counter > 0) and (vals[lookback_counter]['frequency']<0):
          lookback_counter -=1
        if lookback_counter>=0:
          vals[lookback_counter]["sustain"]+=step_size
          vals.append({'frequency':-1,'duration':make_rest(step_size),'sustain':step_size})
      elif note == "*":
        # add a rest
         vals.append({'frequency':-1,'duration':make_rest(step_size),'sustain':step_size})
      elif note == "/":
        # new track
        vals = []
        polyvals.append(vals)
      elif note == '>':
        # octave up
        oct +=1
      elif note == '<':
        # octave down
        oct -=1
      elif is_number(note):
        # note
        frequency = float(note)+(oct*12)
        vals.append({'frequency':frequency,'duration':step_size,'sustain':step_size})
      else:
        if counter == 0:
          type_name = note
        else:
          vals.append(note)
      counter += 1
    commands.append(Filter(type_name,separate(polyvals)))
  return process(commands)

class Stemel:
  """
  This is the class that holds the patterns, parses them into
  lists of pitch, duration and sustain information.
  """

  def patterns(self):
    return (self.pitches, self.durations, self.sustains, self.opts)

  def __init__(self, pattern, step_size):
    self.pattern = pattern
    self.step_size = step_size
    (self.pitches, self.durations, self.sustains, self.opts) = make_pattern(pattern,step_size)

if __name__ == '__main__':
  Stemel("0-0/7 | amp 0.8", 0.5)
