# play a pattern in sonic pi
def sp(pattern, amplitude)
  counter1 = 0
  pattern[:pitches].each do |notes|
    counter2 = 0
    duration = 0
    notes.each do |note|
      dur = pattern[:durations][counter1][counter2]
      if dur.class==Hash
        duration = dur[:rest]
      else
        play note, release:pattern[:sustains][counter1][counter2], amp:amplitude
        duration = dur
      end
      puts duration
      counter2 +=1
    end
    sleep duration
    counter1 += 1
  end
end
