import math
num_chars = ['-','0','1','2','3','4','5','6','7','8','9', '.']
int_chars = ['-','0','1','2','3','4','5','6','7','8','9']
positive_numchars = ['0','1','2','3','4','5','6','7','8','9', '.']
def parse(note_str):
    note_line = note_str.strip()+" "
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
            cursor2 = cursor + 1
            number_skips = 1
            if (cursor2<length) and (note_line[cursor2]=='*'):
                cursor+=2
                cursor2 = cursor+1
                while (cursor2<length) and (note_line[cursor2] in int_chars):
                    cursor2+=1
                number_skips = int(note_line[cursor:cursor2])
                cursor = cursor2
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
                dur_array.append(time_segment*number_skips)
            else:
                if len(dur_array)>0:
                    dur_array[len(dur_array)-1]+=time_segment*(number_skips)
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
        elif command in num_chars:
            # adding a note
            cursor2=cursor
            while (cursor2<length) and (note_line[cursor2] in num_chars):
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
        elif command == '>':
            # increasing amplitude
            amplitude = 2
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] == '>'):
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
        elif command == '<':
            # decreasing amplitude
            amplitude = 0
            cursor2=cursor+1
            while (cursor2<length) and (note_line[cursor2] == '<'):
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
from FoxDot.lib import *
Scale.default="major"
Clock.bpm=100
def sendto(ins, str):
    (notes_array, dur_array, sus_array, amp_array)=parse(str)
    ins.pitch = notes_array
    ins.sus = sus_array
    ins.dur=dur_array
    ins.amp=amp_array
p1.stop()
p2 >> space()
sendto(p2,"0_8,*8 0/4_8,*8 0/3_8,*8 0_8/3,*7")
p3 >> charm()
sendto(p3, "0_16,*15")
Master().room=0.5
Master().mix=0.3
# print(parse("0/4_4,*8"))

p2.stop()
p3.stop()
b1 >> bass(lpf=linvar([160,500],32), formant=2)
sendto(b1,"f0 l2 0_4/4_,,0,0,0_4/5_,,0,0,0_4/6_,,0,0,0_4/5_,,0,0")
p1 >> sitar(shape=0, drive=0.4, bpf=1200, formant=3)
sendto(p1,"l2 2_9>5,*9 4,4,2,2<,1,1<,0,2_9,*9 4,4,2,2,1,1,0")
d1 >> play("x-o-", sample=1, amp=1)

sendto(b1,"f1 l2 0_4/4_,,0,0,0_4/5_,,0,0,0_4/4_,,0,0,0_4/5_,,0,0")
sendto(p1,"l2 1_9>5,*9 4,4,2,2<,1,1<,0,1_9,*9 4,4,2,2,1,1,0")
d1 >> play("x-o-", sample=4)

sendto(b1,"f0 l2 0_4/4_,,0,0,0_4/5_,,0,0,f1 0_4/5_,,0,0,0_4/4_,,0,0")
sendto(p1,"f0 l2 9_7,*6 6,5_7,*8 -5")
d1 >> play("x-o-", sample=3)

sendto(b1,"f0 l2 0_4/4_,,0,0,0_4/5_,,0,0,0_4/6_,,0,0,0_4/5_,,0,0")
sendto(p1,"f0 l2 9_32,*31")
d1 >> play("xOO-XoOt", sample=6)

sendto(b1,"f2 l2 0_4/4_,,0,0,0_4/5_,,0,0,0_4/6_,,0,0,0_4/5_,,0,0")
sendto(p1,"f7 l2 2_9>5,*9 4,4,2,2<,1,1<,0,2_9,*9 4,4,2,2,1,1,0")
d1 >> play("[--]X-x", sample=8)

sendto(b1,"f3 l2 0_4/4_,,0,0,0_4/5_,,0,0,0_4/6_,,0,0,0_4/5_,,0,0")
sendto(p1,"l2 0_4,*4 1_4,*4 0_8/6_8,*7")
d1 >> play("X-o[----]", sample=4)

p2 >> space()
sendto(p2,"0_8,*8 0/4_8,*8 0/3_8,*8 0_8/3,*7")
