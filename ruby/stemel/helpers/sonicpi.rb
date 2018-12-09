# play a pattern in sonic pi
def sp(stemel, amplitude=1)
  pattern = stemel.pattern()
  counter1 = 0
  pattern[:pitches].each do |notes|
    counter2 = 0
    duration = 0
    notes.each do |note|
      dur = pattern[:durations][counter1][counter2]
      if dur.class==Hash
        duration = dur[:rest]
      else
        if amplitude.class == [].class
          amp = amplitude[counter2 % amplitude.size()]
        else
          amp = amplitude
        end
        play note, release:pattern[:sustains][counter1][counter2], amp:amp
        duration = dur
      end
      puts duration
      counter2 +=1
    end
    sleep duration
    counter1 += 1
  end
end
Sample_table = [
  :drum_bass_hard, #0
  :drum_bass_soft, #1
  :drum_cowbell,   #2
  :drum_cymbal_closed, #3
  :drum_cymbal_hard,   #4
  :drum_cymbal_open,   #5
  :drum_cymbal_pedal,  #6
  :drum_cymbal_soft,   #7
  :drum_heavy_kick,    #8
  :drum_roll,          #9
  :drum_snare_hard,    #10
  :drum_snare_soft,    #11
  :drum_splash_hard,   #12
  :drum_splash_soft,   #13
  :drum_tom_hi_hard,   #14
  :drum_tom_hi_soft,   #15
  :drum_tom_lo_hard,   #16
  :drum_tom_lo_soft,   #17
  :drum_tom_mid_hard,  #18
  :drum_tom_mid_soft   #19
]
# drum player
def sp_drums(stemel, amplitude=1)
  pattern = stemel.pattern()
  counter1 = 0
  pattern[:pitches].each do |notes|
    counter2 = 0
    duration = 0
    notes.each do |note|
      dur = pattern[:durations][counter1][counter2]
      if dur.class==Hash
        duration = dur[:rest]
      else
        if amplitude.class == [].class
          amp = amplitude[counter2 % amplitude.size()]
        else
          amp = amplitude
        end
        sample Sample_table[note % Sample_table.size()], amp:amp
        duration = dur
      end
      puts duration
      counter2 +=1
    end
    sleep duration
    counter1 += 1
  end
end
