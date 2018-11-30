class Sequencer
  class Note
    def initialize(value, duration, amplitude, slide)
      @value = value
      @duration = duration
      @amplitude = amplitude
      @slide = slide
    end
    def to_s()
      "["+@value.to_s+"-"+@duration.to_s+"-"+@amplitude.to_s+"-"+@slide.to_s+"]"
    end
  end


  class Track
    def initialize(instrument_name)
      @voices = []
      @instrument = instrument_name
    end

    def size()
      @voices.size
    end

    def to_s()
      buffer = "Track "+@instrument+"\n"
      @voices.each do |voice_list|
        counter=0
        voice_list.each do |note|
          buffer += note.to_s+" "
        end
        buffer+="\n"
        counter +=1
      end
      buffer
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
            vals << Note.new(-1, 1, amplitude, 0)
          end
        when /^\*+?$/
          note.size().times do
            vals << Note.new(-1, 1, amplitude, 0)
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
            vals << Note.new(note.to_f+(oct*12), 1, amplitude, 0)
        when /^a[\d | \.]+?$/
          amplitude = note.slice(1,note.size()-1).to_f
        else
          puts "? " + note
        end
      end
      polyvals
    end

    def add_pattern(pattern)
      notes = make_notes(pattern)
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
        @voices << seq_buffer
        counter += 1
      end
    end   
  end #tracks
  def instr(name)
    unless @tracks[name]
      @tracks[name]=Track.new(name)
    end
    yield(@tracks[name]) if block_given?
    @tracks[name]
  end
  def initialize()
    @tracks = Hash.new
    yield(self) if block_given?
  end
end

s = Sequencer.new do |seq|
    seq.instr("pluck")
end
s3 = Sequencer.new
bass = s.instr("bass")
bass.add_pattern("7 5 5 7 / 0 * * *")
puts bass.to_s
