require 'yaml'

Struct.new("Note", :value, :duration, :amplitude, :slide)

def make_notes(note_s)
  polyvals=[]
  vals = []
  polyvals.append(vals)
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
        vals.append(Struct::Note::new(-1, 1, amplitude, 0))
      end
    when /^\*+?$/
      note.size().times do
        vals[counter]=Struct::Note::new(-1, 1, amplitude, 0)
        counter += 1
      end
    when '/'
      vals = []
      polyvals.append(vals)
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
        vals.append(Struct::Note::new(note.to_f+(oct*12), 1, amplitude, 0))
    when /^a[\d | \.]+?$/
      amplitude = note.slice(1,note.size()-1).to_f
    else
      puts "? " + note
    end
  end
  return polyvals
end



def add_pattern(times, instrument, pattern)
  notes = make_notes(pattern)
  buffer = Sequencer[instrument]
  puts buffer
  length = notes.max{ |a,b| a.size() <=> b.size()}.size()
  unless buffer
    buffer = []
    Sequencer[instrument]=buffer
  end

  times.times do
    counter = 0
    length.times do
      seq_buffer = []
      notes.each do |note_line|
        if (note_line.size()>0)
          seq_buffer.append(note_line[counter % note_line.size()])
        end
      end
      buffer.append(seq_buffer)
      counter += 1
    end
  end
  puts Sequencer.to_s
end

Sequencer = Hash.new()
Bpm = 240

def with_seq(instrument)
  buffer = Sequencer[instrument]
  step_size = 60.0/Bpm
  voice_counter = 0
  buffer.each do |seq_buffer|
    seq_buffer.each do |note|
      if note.value > 0
        yield note.value, note.duration*step_size, note.amplitude, note.slide
      end
    end
    sleep step_size
  end
end

# live_loop :seq do
#   cue :tick
#   sleep 30.0/Bpm
# end

# add_pattern(2, :bass, "> 0 0 0 0")
add_pattern(2, :bass, "0 0")
add_pattern(1, :bass, "0 - 0 0")
add_pattern(1, :pluck, ">> 4 5 7 0 7 0 5 5 7 / 10 0 10")


live_loop :bass do
  # sync :tick
  with_seq :bass do |value, duration, amplitude|
    use_synth :beep
    play value, release:duration, amp:amplitude
  end
end

live_loop :pluck do
  # sync :tick
  with_seq :pluck do |value, duration, amplitude|
    use_synth :pluck
    play value, sustain:duration*0.75, amp:amplitude, release:duration*0.75
  end
end
