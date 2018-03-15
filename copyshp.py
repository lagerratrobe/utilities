#! /usr/bin/python

__author__= 'randre@3tiergroup.com'

"""Copies all of the files relevant to a shapefile to a new one."""

import shutil
import sys
import glob

def Usage():
  print ("Run with the following args:\n"
         "  copyshp.py <input_file>.shp <output_file>.shp")

def CopyFile(in_file, out_pre):
  [in_pre, in_suf] = in_file.split('.')
  new_file = '%s.%s' % (out_pre, in_suf)
  shutil.copy(in_file, new_file)
  print "Copied %s --> %s" % (in_file, new_file)

def main():
  if len(sys.argv) < 3:
    Usage()
    sys.exit(1)
  else:
    [infile, outfile] = [ sys.argv[1], sys.argv[2] ]
    in_pre = infile.split('.')[0]
    out_pre = outfile.split('.')[0]
    match = in_pre + ".*"
    in_list = glob.glob(match)
    for file in in_list:
      CopyFile(file, out_pre)
  
if __name__ == '__main__':
  main()
  
