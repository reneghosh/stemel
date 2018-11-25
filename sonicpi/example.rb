#!/bin/ruby

def notes(note_s)
  counter = 0
  table = Hash.new
  (0..9).each do |num|
    table[num.to_s]=counter
    counter += 1
  end
  ('A'..'Z').each do |letter|
    table[letter]=counter
    counter += 1
    table[letter.downcase()]=counter
    counter += 1
  end
  polyvals=[]
  polydurs=[]
  vals = []
  durs = []
  last_note = ''
  last_dur = 1
  counter = 0
  poly=0
  polyvals[poly]=vals
  polydurs[poly]=durs
  oct = 3
  note_s.split('').each do |note|
    case note
    when '-'
      lookback_counter = 0
      while (!vals[lookback_counter])
        lookback_counter -=1
      end
      if lookback_counter>=0
        durs[lookback_counter]+=1
      end
      durs[counter]=1
      vals[counter]=-1
      counter += 1
    when '*'
      vals[counter]=-1
      durs[counter]=1
      counter += 1
    when '/'
      counter=0
      poly += 1
      vals = []
      durs = []
      polyvals[poly]=vals
      polydurs[poly]=durs
    when '>'
      oct += 1
    when '<'
      oct -=1
      if oct < 0
        oct = 0
      end
    else
      if table[note]
        vals[counter]=table[note]+(oct*12)
        durs[counter]=1
        counter += 1
      end
    end
  end
  # puts polyvals.to_s
  # puts polydurs.to_s
  polynotes=[]
  (0..poly).each do |line|
    notes = []
    (0..(polyvals[line].size()-1)).each do |counter|
      notes[counter]=[polyvals[line][counter], polydurs[line][counter]]
    end
    polynotes[line]=notes
  end
  return polynotes
end


def play_notes(note_s, step_size=1, shift=0)
  the_notes = notes(note_s)
  puts the_notes.to_s
  polycursor=0
  polys = the_notes.size()
  ended = false
  counter = 0
  while !ended
    ended = true
    the_notes.each do |line|
      if polycursor < line.size()
        note = line[polycursor]
        if (note[0]>0)
          play note[0]+shift, release:note[1]*step_size
          # puts("playing "+note[0].to_s+" over "+note[1].to_s)
        end
        if polycursor + 1 < line.size()
          ended = false
        end
      end
    end
    puts("sleeping "+step_size.to_s)
    sleep step_size
    polycursor+=1
  end
end

# play_notes("AAA/BBB/CCC")

in_thread do
  loop do
    cue :tick
    sleep 0.25
  end
end


live_loop :lead do
  sync :tick
  with_fx :distortion, mix:0.1 do
    with_fx :echo, mix: 0.3, phase: 0.0, amp: 0.4 do
      use_synth :beep
      play_notes ">40504000/0---0--", step_size=0.25, shift=0
    end
  end
end

live_loop :lead2 do
  sync :tick
    with_fx :echo, mix: 0.3, phase: 0.0, amp: 0.3 do
      use_synth :beep
      play_notes ">>DdeAgAHA", step_size=0.25, shift=0
    end
end


live_loop :base do
  sync :tick
  with_fx :echo, mix: 0.3, phase: 0.25 do
    use_synth :fm
    play_notes ">0*0*", step_size=0.25, shift=5
  end
end
