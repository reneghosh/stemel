from FoxDot import *
import sys
sys.path.append("../stemel")
from stemel.patterns import *

def foxdotidy(pattern):

  def first_non_rest(line):
    """
    transform a pattern into a FoxDot pattern.
    This involves replacing tuples with single values
    when a tuple contains only one element, and replacing
    hash rests with foxdot rests
    """
    found = False
    non_rest = None
    rest_list = []
    counter = 0
    for val in line:
      if type(val) != type({}):
        found = True
        non_rest = val
      else:
        rest_list.append(counter)
      counter += 1
    if found is False:
      non_rest = line[0]
    return (found, val, rest_list)
  (pitches, durations, sustains) = pattern.patterns()
  # clean up values that have rests but other notes too
  # replace mixed durations with the first non-rest
  counter = 0
  for line in durations:
    if len(line)>0:
      (found, val, rest_list) = first_non_rest(durations[counter])
      durations[counter]= val
      if (found):
        for index in rest_list:
          pitches[counter].remove(pitches[counter][index])
          sustains[counter].remove(sustains[counter][index])
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

def stemel_player(player,pattern,step_size,**args):
  """
  player that wraps foxdot synthdefs and calls them
  with freqency, duration and sustain parameters,
  relaying any other keyword parameter while doing so.
  """
  pattern = Stemel(pattern, step_size)
  # (frequencies,durations, sustains) = replace_rests(*pattern, rest(step_size))
  # print_pattern(*(frequencies,durations, sustains))
  return player(pat.frequencies, dur=pat.durations, sus=pat.sustains, **args)

def fdpat(pattern, step_size):
  return foxdotidy(Stemel(pattern, step_size).patterns())
