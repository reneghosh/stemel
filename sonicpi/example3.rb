def complete_notes(notes)
  notes.each do |note|
    unless note[:attack]
      note[:attack]=0.2
    end
    unless note[:release]
      note[:release]=0.8
    end
    unless note[:amplitude]
      note[:amplitude]=1.0
    end
  end
end

def make_notes(note_s)
  polyvals=[]
  vals = []
  polyvals << vals
  oct = 3
  amplitude = 1.0
  note_s.split(" ").each do |note|
    note.strip!
    note.downcase!
    case note
    when /^-+?/
      note.size().times do
        lookback_counter = vals.size()-1
        while ((lookback_counter > 0) && (vals[lookback_counter].value<0))
          lookback_counter -=1
        end
        if lookback_counter>=0
          vals[lookback_counter][:duration]+=1
        end
        vals << {:frequency => -1, :duration=> 1}
      end
    when /^\*+?$/
      note.size().times do
        vals << {:frequency => -1, :duration=> 1}
      end
    when '/'
      vals = []
      polyvals << vals
    when /^>+?/
      note.size().times do
        oct +=1
      end
    when /^<+?/
      note.size().times do
        oct -=1
      end
      if oct < 0
        oct = 0
      end
    when /^[\d | \.]+?$/
        vals << { :frequency => note.to_f+(oct*12), :duration=> 1}
    when /^a[\d | \.]+?$/
      amplitude = note.slice(1,note.size()-1).to_f
    else
      puts "? " + note
    end
  end
  polyvals
end

# make a list of list of notes into a single list by incorporating
# the time at which each note is played. This allows
# for shifting notes at non-integer values
def flatten(pattern)
  buffer = []
  counter = 0
  pattern.each do |voice|
    voice.each do |note|
      new_note=note.clone()
      new_note[:time] = counter
      buffer << new_note
    end
    counter = counter + 1
  end
  buffer = buffer.sort{|a,b| a[:time] <=> b[:time]}
  buffer = complete_notes(buffer)
  buffer
end

def make_pattern(score)
  pattern = []
  notes = make_notes(score)
  return if notes.size()==0
  length = notes.max{ |a,b| a.size() <=> b.size()}.size()
  counter = 0
  length.times do
    seq_buffer = []
    notes.each do |voice_line|
      if (voice_line.size()>0)
        seq_buffer << voice_line[counter % voice_line.size()]
      end
    end
    pattern << seq_buffer
    counter += 1
  end
  pattern = flatten(pattern)
  pattern
end

#randomize the time of a note
def randomize_time(notes, factor)
  buffer = []
  notes.each do |note|
    note[:time]=note[:time]+(rand()-0.5)*factor
    buffer << note
  end
  buffer.sort{|a,b| a[:time] <=> b[:time]}
end

# randomize amplitudes
def randomize_amplitude(notes, factor)
  buffer = []
  notes.each do |pland|
    new_note = pland.clone()
    new_note[:amplitude] = new_note[:amplitude]+((rand()-0.5)*factor)
    buffer << new_note
  end
  buffer.sort{|a,b| a[:time] <=> b[:time]}
end

def multiply_plan(factor, plan)
  return plan if factor<2
  max_time = plan.max{ |a,b| a[:time] <=> b[:time] }[:time]
  buffer = []
  (factor-1).times do |i|
    plan.each do |note|
      new_note = note.clone()
      new_note[:time] += i*(max_time+1)
      buffer << new_note
    end
  end
  buffer
end

# randomize attack-delays
def randomize_attack(notes, factor)
  buffer = []
  notes.each do |note|
    new_note = note.clone()
    point = 1+((rand()-0.5)*factor)
    new_note[:attack] *= point
    if new_note[:attack] > 1
      new_note[:attack] = 1
    end
    if new_note[:attack] < 0
      new_note[:attack] = 0
    end
    new_note[:release] = 1-new_note[:attack]
    buffer << new_note
  end
  buffer.sort{|a,b| a[:time] <=> b[:time]}
end

player1 = Proc.new do |frequency, duration, amplitude, attack, release|
    use_synth :tb303
    p = play frequency, attack:attack*0.01, decay:0.1, sustain:duration*0.7, release:duration*0.3, amp:amplitude
end

step=0.18
# plan = make_pattern(" 7 - 7 7 / >> 12 7 5 7 12 7 5 7")
# plan = make_pattern(" 5 - 5 5 / >> 12 7 5 7 12 7 5 7")
plan = make_pattern(">> 0 7 5 8")
plan = make_pattern("> 0 - 0 0 / > 12 7 5 7 12 7 5 7")
# plan = multiply_plan(10, plan)
# plan = randomize_time(plan, 0.09)
# plan = randomize_amplitude(plan, 1.7)
# plan = randomize_attack(plan, 2)
puts plan
live_loop :loopi do
  with_fx :lpf, cutoff: 100 do
    with_fx :reverb, mix:0.3 do
      prev_time = 0
      plan.each do |note|
        puts note
        unless (note[:time] == 0) || (note[:time]-prev_time<0.01)
          sleep (note[:time] - prev_time)*step
        end
        if note[:frequency] > 0
          player1.call(note[:frequency],note[:duration]*step,
            note[:amplitude],note[:attack]*step, note[:release]*step)
        end
        prev_time = note[:time]
      end
      sleep step
    end
  end
end
