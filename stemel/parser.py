str = "(This is a (test)) (with) groups \1"
buffer = []
groups = []
cursor = -1
for c in str:
    if c == '(':
         cursor += 1
         buffer.append([])
    elif c == ')':
        if cursor >= 0:
            groups.append(buffer[cursor])
            buffer.remove(buffer[cursor])
            cursor -= 1
            if cursor <-1:
                cursor = -1
    elif cursor >= 0:
        for i in range(0,cursor+1):
            buffer[i].append(c)
print("groups:")
for buff in groups:
        print("".join(buff))
decs = ['0','1','2','3','4','5','6','7','8','9']
str = "0.1 10 *"
str += " "
buffer=[]
num_buffer=[]
for i in range(0,len(str)):
    c = str[i]
    if c in decs:
        num_buffer.append(c)
    elif c == '.':
        if len(num_buffer)>0:
            if '.' not in num_buffer:
                num_buffer.append(c)
    else:
        if len(num_buffer)>0:
            buffer.append("".join(num_buffer))
            num_buffer = []
        buffer.append(c)
print(buffer)
