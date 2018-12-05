Note = Struct.new :frequency, :duration, :amplitude, :attack, :release do
  def initialize(*)
    super
    self.amplitude ||= 1.0
    self.attack ||= 0.2
    self.release ||= 0.8
  end
end
Plan = Struct.new :note, :time do
  def initialize(*)
    super
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
          vals[lookback_counter].duration+=1
        end
        vals << Note.new(-1, 1)
      end
    when /^\*+?$/
      note.size().times do
        vals << Note.new(-1, 1)
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
        vals << Note.new(note.to_f+(oct*12), 1)
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
  pattern.each do |voices|
    voices.each do |note|
      buffer << Plan.new(note, counter)
    end
    counter += 1
  end
  buffer.sort{|a,b| a.time <=> b.time}
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
  flatten(pattern)
end

#randomize the time of a note
def randomize_time(notes, factor)
  buffer = []
  notes.each do |note|
    buffer << Plan.new(note.note, note.time+(rand()-0.5)*factor)
  end
  buffer.sort{|a,b| a.time <=> b.time}
end

# randomize amplitudes
def randomize_amplitude(notes, factor)
  buffer = []
  notes.each do |pland|
    new_note = pland.note.clone
    new_note.amplitude = new_note.amplitude+((rand()-0.5)*factor)
    buffer << Plan.new(new_note, pland.time)
  end
  buffer.sort{|a,b| a.time <=> b.time}
end

# randomize attack-delays
def randomize_attack(notes, factor)
  buffer = []
  notes.each do |pland|
    new_note = pland.note.clone
    point = (rand())
    new_note.attack = point
    new_note.release = 1- point
    buffer << Plan.new(new_note, pland.time)
  end
  buffer.sort{|a,b| a.time <=> b.time}
end


player1 = Proc.new do |frequency, duration, amplitude|
    use_synth :fm
    point = rand()*0.1
    p = play frequency, attack: duration*point, release: duration*(1-point), amp:amplitude
end

step=0.25
notes = make_pattern(" 7 - 7 7 / >> 12 7 5 7 12 7 5 7")
notes = make_pattern(" 5 - 5 5 / >> 12 7 5 7 12 7 5 7")
notes = make_pattern("> 0 - 0 0 / > 12 7 5 7 12 7 5 7")
notes = randomize_time(notes, 0.04)
notes = randomize_amplitude(notes, 0.9)
notes = randomize_attack(notes, 0.9)
puts notes.to_s

live_loop :loopi do
  with_fx :gverb, mix:0.1 do
    with_fx :ixi_techno do
      prev_time = 0
      notes.each do |plan|
        unless (plan.time == 0) || (plan.time-prev_time<0.01)
          sleep (plan.time - prev_time)*step
        end
        if plan.note.frequency > 0
          player1.call(plan.note.frequency,plan.note.duration*step)
        end
        prev_time = plan.time
      end
      sleep step
    end
  end
end
