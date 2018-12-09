import re

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

def make_pattern(score, step_size):
  """
  Take a score inputted as a line of text and a step size (0.25 default)
  and return a tuple of frequencies, sustains and durations
  """
  polyvals=[]
  vals = []
  polyvals.append(vals)
  oct = 0
  amplitude = 1.0
  for note in re.split(r'\s+', score):
    note = note.strip()
    note = note.lower()
    if re.search(r'^-+?', note):
      # carry previous note one more step
      for i in note:
        lookback_counter = len(vals)-1
        while (lookback_counter > 0) and (vals[lookback_counter]['frequency']<0):
          lookback_counter -=1
        if lookback_counter>=0:
          vals[lookback_counter]["sustain"]+=step_size
          vals.append({'frequency':-1,'duration':make_rest(step_size),'sustain':step_size})
    elif re.search(r'^\*+?$', note):
      # add a rest
      for i in note:
         vals.append({'frequency':-1,'duration':make_rest(step_size),'sustain':step_size})
    elif re.search(r'/',note):
      # new track
      vals = []
      polyvals.append(vals)
    elif re.search(r'^>+?', note):
      # octave up
      for i in note:
        oct +=1
    elif re.search(r'^<+?', note):
      # octave down
      for i in note:
        oct -=1
      if oct < 0:
        oct = 0
    elif re.search(r'^[\d | \.]+?$', note):
      # note
      vals.append({'frequency':(float(note)+(oct*12)),'duration':step_size,'sustain':step_size})
  return separate(polyvals)

class Stemel:

  def replace_rests(pitch, duration, sustain, obj):
    new_duration = []
    for step in duration:
      if type(step)==type((1,)):
        new_dur = ()
        for dur in step:
          if type(dur) == type({}):
            new_dur = (*new_dur, obj)
          else:
            new_dur = (*new_dur, dur)
        new_duration.append(new_dur)
      else:
        if type(step) == type({}):
          new_duration.append(obj)
        else:
          new_duration.append(step)
    return (pitch, new_duration, sustain)


  def print(self):
    return (self.pitches, self.durations, self.sustains)

  def __init__(self, pattern, step_size):
    self.pattern = pattern
    self.step_size = step_size
    (self.pitches, self.durations, self.sustains) = make_pattern(pattern,step_size)

pat = Stemel("0 - 0 0 / 5- 7-", 0.25)
