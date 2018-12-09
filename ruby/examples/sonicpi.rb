bass_pattern = Stemel.new(">>>0-0-0-0-0-0-5 5 7 10/ * 12 * 12 * 12 * 12 ****10 22 22 24", 0.25)
lead_pattern = Stemel.new(">>7 7 7 7 7 7 7 7 10 10 7 0 7 2 0 7 0 12", 0.125)
samples = [:drum_bass_hard, :drum_cymbal_closed, :drum_snare_soft,:drum_tom_mid_soft]
drum_pattern = Stemel.new("0 3 2 0/*1*1***1******1 1", 0.25)

bass_pattern = Stemel.new(">>>0-7-0-10 10 10 12 9 / 12 12 - - - 15", 0.25)
with_fx :lpf, mix: 0.7, cutoff: 90 do |filter|
  with_fx :reverb, mix:0.3 do
    # bass
    live_loop :bass do
      use_synth :fm
      sp(bass_pattern, amplitude=1)
    end

    # lead
    live_loop :lead do
      with_fx :ixi_techno do
        use_synth :pluck
        sp(lead_pattern, amplitude=[0.6, 1.0, 0.3, 0.6, 0.1, 3.0])
      end
    end

    # drums
    live_loop :drums do
      # with_fx :echo do
        sp_drums(drum_pattern, samples, amplitude=[0.6, 1.0, 0.3, 0.6, 0.1, 3.0])
      # end
    end
  end
end
