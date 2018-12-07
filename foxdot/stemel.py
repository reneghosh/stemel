import re
def separate(notes, step_size):
    frequencies = []
    durations = []
    sustains = []
    if len(notes)==0:
        return ([],[])
    length = len(max(notes, key = lambda x: len(x)))
    counter = 0
    for i in range(0, length):
        freq_buffer = ()
        dur_buffer = ()
        sus_buffer = ()
        for voice_line in notes:
            if len(voice_line)>0:
                freq_buffer = (*freq_buffer, voice_line[counter % len(voice_line)]['frequency'])
                sus_buffer = (*sus_buffer, voice_line[counter % len(voice_line)]['sustain'])
                dur_buffer = (*dur_buffer, voice_line[counter % len(voice_line)]['duration'])
        new_duration_buff = ()
        for duration in dur_buffer:
            if type(duration)==float:
                new_duration_buff = (*new_duration_buff, duration)
        if len(new_duration_buff)==0:
            new_duration_buff=(rest(step_size),)
        else:
            new_duration_buff = (step_size,)
        new_frequency_buff = ()
        for frequency in freq_buffer:
            if (frequency > -1):
                new_frequency_buff = (*new_frequency_buff, frequency)
        if len(new_frequency_buff)==0:
            new_frequency_buff=(0,)
        if len(new_frequency_buff)>1:
            frequencies.append(new_frequency_buff)
        else:
            frequencies.append(new_frequency_buff[0])
        if len(new_duration_buff)>1:
            durations.append(new_duration_buff)
        else:
            durations.append(new_duration_buff[0])
        if len(sus_buffer)>1:
            sustains.append(sus_buffer)
        else:
            sustains.append(sus_buffer[0])
        counter += 1
    return (frequencies, durations, sustains)

def make_pattern(score, step_size):
    polyvals=[]
    vals = []
    polyvals.append(vals)
    oct = 0
    amplitude = 1.0
    for note in re.split(r'\s+', score):
        note = note.strip()
        note = note.lower()
        if re.search(r'^-+?', note):
            for i in note:
                lookback_counter = len(vals)-1
                while (lookback_counter > 0) and (vals[lookback_counter]['frequency']<0):
                    lookback_counter -=1
                if lookback_counter>=0:
                    vals[lookback_counter]["sustain"]+=step_size
                    vals.append({'frequency':-1,'duration':rest(step_size),'sustain':step_size})
        elif re.search(r'^\*+?$', note):
            for i in note:
               vals.append({'frequency':-1,'duration':rest(step_size),'sustain':step_size})
        elif re.search(r'/',note):
            vals = []
            polyvals.append(vals)
        elif re.search(r'^>+?', note):
            for i in note:
              oct +=1
        elif re.search(r'^<+?', note):
            for i in note:
              oct -=1
            if oct < 0:
              oct = 0
        elif re.search(r'^[\d | \.]+?$', note):
            vals.append({'frequency':(float(note)+(oct*12)),'duration':step_size,'sustain':step_size})
    return separate(polyvals, step_size)

def stemel_player(player,pattern,step_size,**args):
    (frequencies, durations, sustains) = make_pattern(pattern, step_size)
    return player(frequencies, dur=durations, sus=sustains, **args)

# (frequencies, durations, sustains) = pattern("> 0 0 / 7 7 5 - 9 7 5 7", 0.5)
# (frequencies, durations, sustains) = pattern("> 0 - 0 / 7 7 7", 0.5)
amplitudes = P(PRand([0.3, 1.0, 0.8, 0.1]), PRand([0.3, 1.0, 0.8, 0.1]))*3.6
Scale.default ="chromatic"
b1 >> stemel_player(pluck, "<< 0 0 7 0 / > 0 7 5 7 12 10 8 7", 0.5, lpf=150, pan=(-1,1), oct=4, echo=1, room=0.5, mix=0.5)

b3 >> stemel_player(sitar, "0", 2)
# b1 >> pluck(frequencies, dur=durations, sus=sustains, amp=amplitudes, )
#
