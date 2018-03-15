#! /usr/local/bin/python

'''Resizes FONTS contained in a mapfile.  Works by first analyzing all mapfiles in a directory and 
building an index of what lines need to be modified.  These lines are identified by looking for the
"FONT" tag in a line and specifying that the line following that one needs to be modified.  Once all files
have been analyzed and all lines identified, each file in the dictionary is processed and modified.'''

import glob

def read_files(file_list):
  font_index = {}
  for mapfile in file_list:
    data = open(mapfile, 'r').readlines()
    i = 0
    for line in data:
      if "FONT" in line:
        if mapfile not in font_index:
          font_index[mapfile] = [i+1]
        else:
          font_index[mapfile].append(i+1)
      i += 1
  return font_index

def resizer(size_string):
  size_string = size_string.strip()
  size_numeric = float(size_string)
  new_size = size_numeric - (size_numeric / 10)
  return new_size

def edit_files(font_index):
  for mapfile in font_index:
    if mapfile in ['stamen_normal.map', 'stamen_light.map', 'stamen_dark.map']:
      pass
    else:
      line_num = 0
      new_mapfile_name = "new_" + mapfile
      new_mapfile = open(new_mapfile_name, 'a')
      data = open(mapfile, 'r').readlines()
      for line in data:
        if line_num not in font_index[mapfile]:
          new_mapfile.write(line)
        else:
          [whitespace, tag, size] = line.partition('SIZE')
          new_size = resizer(size)
          new_line = "%s%s %.1f\n" % (whitespace, tag, new_size)
          new_mapfile.write(new_line)
        line_num += 1

def main():
  file_list = glob.glob("*.map")
  font_index = read_files(file_list)
  edit_files(font_index)

if __name__ == '__main__':
  main()
