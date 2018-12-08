pattern = make_pattern(" 7 - 7 / >> 7 * 5 7 10 * 5 7", 0.5)
pattern = make_pattern("> 0 - 0 / > 7 * 5 7 10 * 5 7", 0.5)
puts pattern.to_s
with_fx :nlpf, mix: 0.7, cutoff: 70 do
  with_fx :reverb, mix:0.3 do
    live_loop :loopi do
      use_synth :fm
      counter1 = 0
      pattern[:pitches].each do |notes|
        counter2 = 0
        duration = 0
        notes.each do |note|
          dur = pattern[:durations][counter1][counter2]
          if dur.class==Hash
            duration = dur[:rest]
          else
            play note, release:pattern[:sustains][counter1][counter2]
            duration = dur
          end
          counter2 +=1
        end
        sleep duration
        counter1 += 1
      end
    end
  end
end
