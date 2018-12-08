pattern1 = make_pattern("0 0 7 10", 0.25)
pattern2 = make_pattern(">> 0 0 < 7 > 0 / > 7 - 7 5 - 10 10 - - 7 - - ", 0.25)

with_fx :lpf, mix: 0.7, cutoff: 70 do
  with_fx :reverb, mix:0.3 do

    live_loop :loop1 do
      use_synth :pluck
      sp(pattern1, 1)
    end

    live_loop :loop2 do
      use_synth :fm
      sp(pattern2, 0.6)
    end
  end
end
