from FoxDot import *
from stemel.stemel import *

def foxdotidy(pitches, durations, sustains):
  """
  transform a stemel note matrix
  into a foxdot-compatible one.
  """
  # clean up values that have rests but other notes too
  # replace mixed durations with the first non-rest
  counter = 0
  for line in durations:
    if len(line)>0:
      (found, val, rest_list) = first_non_rest(durations[counter])
      durations[counter]= val
      if (found):
        pitches_to_remove = []
        sustains_to_remove = []
        for index in rest_list:
          pitches_to_remove.append(pitches[counter][index])
          sustains_to_remove.append(sustains[counter][index])
        for pitch in pitches_to_remove:
          pitches[counter].remove(pitch)
        for sustain in sustains_to_remove:
          sustains[counter].remove(sustain)
    counter += 1
  # replace lists with tuples
  new_pitches = []
  new_durations = []
  new_sustains = []
  for li in pitches:
    new_pitches.append(tuple(li))
  for du in durations:
    if type(du)==type({}):
        new_durations.append(rest(du['rest']))
    else:
      new_durations.append(du)
  for li in sustains:
    new_sustains.append(tuple(li))
  # clean up single element tuples
  counter = 0
  for line in new_pitches:
    if (type(line)==type((tuple([])))) and (len(line)==1):
      new_pitches[counter]=new_pitches[counter][0]
    counter += 1
  counter = 0
  for line in new_sustains:
    if (type(line)==type((tuple([])))) and (len(line)==1):
      new_sustains[counter]=new_sustains[counter][0]
    counter += 1
  return (new_pitches, new_durations, new_sustains)

def first_non_rest(line):
  """
  find the first non-rest in an array of durations.
  """
  found = False
  non_rest = None
  rest_list = []
  counter = 0
  for val in line:
    if type(val) != type({}): #found a non-rest
      found = True
      non_rest = val
    else:
      rest_list.append(counter)
    counter += 1
  if found is False:
    non_rest = line[0]
  return (found, non_rest, rest_list)

def foxdotidy_pattern(pattern):
  """
  transform a pattern into a FoxDot pattern.
  This involves replacing tuples with single values
  when a tuple contains only one element, and replacing
  hash rests with foxdot rests
  """
  (pitches, durations, sustains, optionals) = pattern.patterns()
  (pitches, durations, sustains) = foxdotidy(pitches, durations, sustains)
  for optional in optionals:
    pattern = optional.pattern
    (op_values, op_durations, op_sustains) = foxdotidy(pattern[0],pattern[1],pattern[2])
    optional.pattern = op_values
  return(pitches, durations, sustains, optionals)

def stemel_player(player,pattern,**args):
  """
  player that wraps foxdot synthdefs and calls them
  with frequency, duration and sustain parameters,
  relaying any other keyword parameter while doing so.
  """
  (pitches, durations, sustains, optionals) = foxdotidy_pattern(pattern)
  opts = {}
  for optional in optionals:
    opts[optional.name]=optional.pattern
  for arg in args:
    opts[arg]=args[arg]
  if 'dur' in args.keys():
    opts['dur']=args['dur']
  else:
    opts['dur']=durations
  if 'sus' in args.keys():
    opts['sus']=args['sus']
  else:
    opts['sus']=sustains
  return player(pitches, **opts)

def splay(player,pattern,step_size, **args):
  """
  alias for stemel_player for patterns as strings, thus
  needing a step size for time allotment
  """
  return stemel_player(player, Stemel(pattern).stretch(step_size),**args)

def slay(player, pattern, step_size, **args):
  """
  alias for stemel_player for patterns as Stemel objects, thus
  needing no step size for time allotment
  """
  pattern = pattern.stretch(step_size)
  return stemel_player(player,pattern,**args)

if __name__ == '__main__':
  Scale.default = "chromatic"
  bass_pattern = "0-0-0-0-0-<5 5 7 10-0 /> * 12 * 12 * 12 * 12 * 12 10 22 22 22 22 24 | amp 0.4 0.6 0.7"
  lead_pattern = ">>7 7 7 7 7 7 7 7 10 10 7 0 7 2 0 7 0 12 | amp 0.4 0.6 0.7"
  b1 >> stplay(jbass, bass_pattern, 0.5, oct=4, lpf=240, room=0.7, mix=0.3, shape=0.1, amp=1.5)
  p1 >> stplay(sitar, lead_pattern, 0.25, oct=5, hpf=320, room=0.7, mix=0.3, amp=0.7)
  d1 >> play("x-t-")

  while 1:
    sleep(100)
