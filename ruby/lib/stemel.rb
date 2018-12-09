def make_notes(pattern_string)
  polyvals=[]
  vals = []
  polyvals << vals
  oct = 3
  amplitude = 1.0
  pattern_string.split(" ").each do |note|
    note.strip!
    note.downcase!
    case note
    when /^-+?/
      note.size().times do
        lookback_counter = vals.size()-1
        while ((lookback_counter > 0) && (vals[lookback_counter][:frequency]<0))
          lookback_counter -=1
        end
        if lookback_counter>=0
          vals[lookback_counter][:sustain]+=1
        end
        vals << {:frequency => -1, :duration=> {"rest":1}, :sustain => 1}
      end
    when /^\*+?$/
      # rest
      note.size().times do
        vals << {:frequency => -1, :duration=> {"rest":1}, :sustain => 1}
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
        vals << { :frequency => note.to_f+(oct*12), :duration=> 1, :sustain => 1}
    else
      puts "? " + note
    end
  end
  polyvals
end

def separate(pattern, step_size)
  durations = []
  sustains = []
  pitches = []
  pattern.each do |line|
    dur_buff =[]
    sus_buff =[]
    pit_buff =[]
    line.each do |note|
      duration = note[:duration]
      if duration.class == Hash
        duration[:rest]=step_size
        dur_buff << duration
      else
        dur_buff << duration*step_size
      end
      sus_buff << note[:sustain]*step_size
      pit_buff << note[:frequency]
    end
    durations << dur_buff
    sustains << sus_buff
    pitches << pit_buff
  end
  {:pitches => pitches, :durations => durations, :sustains => sustains}
end

def make_pattern(score, step_size)
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
  pattern = separate(pattern, step_size)
  pattern
end


pattern = make_pattern("0 - 0", 0.5)
puts pattern
