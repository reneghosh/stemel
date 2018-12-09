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

# drum player
def sp_drums(stemel, samples, amplitude=1)
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
        sample samples[note % samples.size()], amp:amp
        duration = dur
      end
      puts duration
      counter2 +=1
    end
    sleep duration
    counter1 += 1
  end
end
