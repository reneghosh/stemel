import re

def stemel_rest(step_size):
  return {"rest":step_size}

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
    freq_buffer = ()
    dur_buffer = ()
    sus_buffer = ()
    for voice_line in notes:
      if len(voice_line)>0:
        freq_buffer = (*freq_buffer, voice_line[counter % len(voice_line)]['frequency'])
        sus_buffer = (*sus_buffer, voice_line[counter % len(voice_line)]['sustain'])
        dur_buffer = (*dur_buffer, voice_line[counter % len(voice_line)]['duration'])
    new_duration_buff = ()
    for duration in dur_buffer:
      new_duration_buff = (*new_duration_buff, duration)
    new_frequency_buff = ()
    for frequency in freq_buffer:
      if (frequency > -1):
        new_frequency_buff = (*new_frequency_buff, frequency)
    if len(new_frequency_buff)==0:
      #add a placeholder
      new_frequency_buff=(0,)
    if len(new_frequency_buff)>1:
      frequencies.append(new_frequency_buff)
    else:
      #replace single tuple with single value
      frequencies.append(new_frequency_buff[0])
    if len(new_duration_buff)>1:
      durations.append(new_duration_buff)
    elif len(new_duration_buff) == 1:
      durations.append(new_duration_buff[0])
    else:
      durations.append(0)
    if len(sus_buffer)>1:
      sustains.append(sus_buffer)
    else:
      sustains.append(sus_buffer[0])
    counter += 1
  return (frequencies, durations, sustains)

def make_pattern(score, step_size=0.25):
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
          vals[lookback_counter]["duration"]+=step_size
          print(vals[lookback_counter]["duration"])
    elif re.search(r'^\*+?$', note):
      # rest
      for i in note:
         vals.append({'frequency':-1,'duration':stemel_rest(step_size),'sustain':step_size})
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
