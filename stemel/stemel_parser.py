def replace_groupings(str, groups):
  """
  replace variable references with
  the group if references
  """
  def dereference(reference_buffer, groups):
    if len(reference_buffer)>0:
      ref_number = int(''.join(reference_buffer))-1
      return groups[ref_number % len(groups)] +' '
    return ''
  reference_buffer = []
  referencing = False
  new_str = ''
  for c in str:
    if c == ':':
      if not referencing:
        referencing = True
      else:
        new_str += dereference(reference_buffer, groups)
        reference_buffer = []
      new_str += ' '
    elif c.isdigit():
      if referencing:
        reference_buffer.append(c)
      else:
        new_str += c
    else:
      if referencing:
        referencing = False
        new_str += dereference(reference_buffer, groups)+c
        reference_buffer = []
      else:
        new_str += c
  return new_str

def ungroup(str):
  """
  Find groupings and references and replace
  references with groupings
  """
  # looking for opening '(' to start a grouping buffer
  # and a closing ')' to transfer the last word buffer
  # to the groups buffer
  # the buffer is actually a stack of buffers: groups can contain groups
  buffer = [] # buffer to store arrays of group characters
  groups = [] # transfered arrays when groups are closed
  cursor = -1
  new_str = ""
  for c in str:
      if c == '(':
           cursor += 1
           buffer.append([])
           new_str += ' '
      elif c == ')':
          if cursor >= 0:
              groups.append(buffer[cursor])
              buffer.remove(buffer[cursor])
              cursor -= 1
              if cursor <-1:
                  cursor = -1
              new_str += ' '
      else:
        new_str += c
        if cursor >= 0:
          for i in range(0,cursor+1):
              buffer[i].append(c)
  replacement_buffer = []
  for buff in groups:
          replacement_buffer.append(''.join(buff))
  return replace_groupings(new_str, replacement_buffer)

def separate_commands(buffer):
  """
  separate into an array of buffers
  acording to the | pipe character"
  """
  buffers = []
  current_buffer = []
  buffers.append(current_buffer)
  for word in buffer:
    if word == '|':
      new_buffer = []
      current_buffer = new_buffer
      buffers.append(current_buffer)
    else:
      current_buffer.append(word)
  return buffers


def parse_line(str):
  """
  Parse a stemel score and generate words
  """
  symbols = ['<', '>', '|', '*', '-', '/']
  str = ungroup(str + " ")
  buffer=[]
  word_buffer = []
  wording = False
  num_buffer=[]
  for c in str:
      if c.isdigit() and not wording:
          num_buffer.append(c)
      elif c == '.' and not wording:
          if len(num_buffer)>0:
              if '.' not in num_buffer:
                  num_buffer.append(c)
      else:
          # if the number buffer holds something, pass it on to output buffer
          if len(num_buffer)>0:
              buffer.append("".join(num_buffer))
              num_buffer = []
          if not ((c == ' ') or (c=='\t') or (c=='\n')): # not whitespace
            # if symbol than pass on to output buffer
            if c in symbols:
              buffer.append(c)
            else:
              # otherwise, store in word buffer
              word_buffer.append(c)
              wording = True
          else:
            # since whitespace, empty word buffer into output buffer
            if len(word_buffer)>0 and wording:
              buffer.append(''.join(word_buffer))
              wording = False
            word_buffer=[]
  return separate_commands(buffer)

if __name__ == '__main__':
  """
  testing method
  """
  buffer = parse_line("(0):1:1/:1/:1")
  print(buffer)
