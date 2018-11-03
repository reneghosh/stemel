import math
num_chars = ['-','0','1','2','3','4','5','6','7','8','9', '.']
int_chars = ['-','0','1','2','3','4','5','6','7','8','9']
positive_numchars = ['0','1','2','3','4','5','6','7','8','9', '.']
def parse(note_str):
    note_line = note_str.strip()
    base_frequency = 0.0
    amp_multiplier = 1.1
    bpm = 120
    time_segment = 1
    length = len(note_line) #length of line
    notes_array=[]
    dur_array=[]
    sus_array=[]
    amp_array=[]
    notes_list = []
    sus_list = []
    amp_list = []
    cursor=0
    while cursor <= length:
        command = ''
        if (cursor < length):
            command = note_line[cursor]
        if (command in [',',';']) or (cursor==length):
            while len(notes_list)>len(sus_list):
                sus_list.append(1)
            while len(notes_list)>len(amp_list):
                amp_list.append(1)
            # add a note
            if len(notes_list)>0:
                notes_tuple = ()
                sus_tuple = ()
                amp_tuple = ()
                for note in notes_list:
                    notes_tuple = notes_tuple + (note+base_frequency,)
                for sus in sus_list:
                    sus_tuple = sus_tuple + (sus*time_segment,)
                for amp in amp_list:
                    amp_tuple = amp_tuple + (math.pow(amp_multiplier,amp),)
                notes_array.append(notes_tuple)
                sus_array.append(sus_tuple)
                amp_array.append(amp_tuple)
                dur_array.append(time_segment)
            else:
                if len(dur_array)>0:
                    dur_array[len(dur_array)-1]+=time_segment
            # print("adding notes %s" % notes_list)
            # print("adding sus %s" % sus_list)
            notes_list = []
            sus_list = []
            amp_list = []
            duration_buffer = 1
            amp_buffer = 1
            cursor+= 1
        elif command=='f':
            # frequency assignment
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] in num_chars):
                cursor2 += 1
            base_frequency = float(note_line[cursor+1:cursor2])
            # print("frequency assignment: %f" % base_frequency)
            cursor=cursor2+1
        elif command=='a':
            # amplitude assignment
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] in num_chars):
                cursor2 += 1
            amp_multiplier = float(note_line[cursor+1:cursor2])
            # print("amplitude multiplier: %f" % base_amplitude)
            cursor=cursor2+1
        elif command=='b':
            # bpm assignment
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] in num_chars):
                cursor2 += 1
            bpm = float(note_line[cursor+1:cursor2])
            # print("bpm assignment: %f" % bpm)
            cursor=cursor2+1
        elif command=='l':
            # time segment assignment
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] in num_chars):
                cursor2 += 1
            time_segment = 1.0/float(note_line[cursor+1:cursor2])
            # print("time segment assignment: %f" % time_segment)
            cursor=cursor2+1
        elif command in positive_numchars:
            # adding a note
            cursor2=cursor
            while (cursor2<length) and (note_line[cursor2] in positive_numchars):
                cursor2+=1
            note_value = float(note_line[cursor:cursor2])
            notes_list.append(note_value)
            # print("note value: %f" % note_value)
            cursor=cursor2
        elif command == '_':
            # prolonging a note
            duration = 2
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] == '_'):
                cursor2 += 1
                duration += 1
            cursor = cursor2
            if note_line[cursor2] in int_chars:
                duration -= 1
                while (cursor2<length) and (note_line[cursor2] in num_chars):
                    cursor2 += 1
                duration += int(note_line[cursor:cursor2])-1
            cursor = cursor2
            sus_list.append(duration)
        elif command == '+':
            # increasing amplitude
            amplitude = 2
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] == '+'):
                cursor2 += 1
                amplitude += 1
            cursor = cursor2
            if note_line[cursor2] in int_chars:
                amplitude -= 1
                while (cursor2<length) and (note_line[cursor2] in num_chars):
                    cursor2 += 1
                amplitude += int(note_line[cursor:cursor2])-1
            cursor = cursor2
            amp_list.append(amplitude)
        elif command == '-':
            # decreasing amplitude
            amplitude = 0
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] == '-'):
                cursor2 += 1
                amplitude -= 1
            cursor = cursor2
            if note_line[cursor2] in int_chars:
                amplitude -= 1
                while (cursor2<length) and (note_line[cursor2] in num_chars):
                    cursor2 += 1
                amplitude -= int(note_line[cursor:cursor2])-1
            cursor = cursor2
            amp_list.append(amplitude)
        elif command == '/':
            while len(notes_list)>len(sus_list):
                sus_list.append(1)
            while len(notes_list)>len(amp_list):
                amp_list.append(1)
            cursor += 1
        else:
            cursor += 1
    return (notes_array, dur_array, sus_array, amp_array)
