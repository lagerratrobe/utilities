#!/usr/bin/env python

'''Hack to resample an image using multiple, overlapping tiles.
   Needed because of interpolation artifacts that were introduced after
   some resampling operations.  Not recommended for use anymore'''

import os
import re
import sys
from osgeo import gdal

#command = 'gdal_translate -srcwin 0 0 10 10 %s out.tif' % (infile)
#os.popen(command)

def SizeTest(src_width, src_height, tile_size):
  if src_width%tile_size != 0 or src_height%tile_size != 0:
    print '%f does not divide equally into %d or %d' % (tile_size, src_width, src_height)
    sys.exit(1)

def TopLeft(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x, orig_y, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % ( 
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    orig_x, orig_y, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def TopRight(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, orig_y, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def Top(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 4
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, orig_y, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def Left(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 4
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    orig_x, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def Right(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 4
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def BottomLeft(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    orig_x, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def BottomRight(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 2
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def Bottom(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 4
  tilesize_y = tile_size + 2
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def Middle(cut_info):
  filename = cut_info[0]
  orig_x = cut_info[1][0]
  orig_y = cut_info[1][1]
  tile_size = int(cut_info[2])
  tilesize_x = tile_size + 4
  tilesize_y = tile_size + 4
  i = `cut_info[3]`
  sample_ratio = cut_info[4]
  offset = 2 * sample_ratio

  # CUT SMALL SECTION OUT OF MOSAIC
  cut_tif = '%s.tif' % (i)
  cut_command = '%d %d %d %d %s %s ' % (orig_x - 2, orig_y - 2, tilesize_x, tilesize_y, filename, cut_tif)
  cut_tile = 'gdal_translate -srcwin ' + cut_command
  os.popen(cut_tile)

  # RESAMPLE SMALL SECTION
  resample_tif = '10x_' + cut_tif
  warp_command = '-ts %d %d -r cubicspline %s %s' % (
    (tilesize_x * sample_ratio), (tilesize_y * sample_ratio), cut_tif, resample_tif)
  warp_tile = 'gdalwarp ' + warp_command
  os.popen(warp_tile)

  # CROP OUT INTERPOLATION ARTIFACTS
  crop_tif = 'crop_' + resample_tif
  crop_command = '%d %d %d %d %s %s' % (
    offset, offset, (tile_size * sample_ratio), (tile_size * sample_ratio), resample_tif, crop_tif)
  crop_tile = 'gdal_translate -srcwin ' + crop_command
  os.popen(crop_tile)
  print i,'done'

def main():
  if len(sys.argv) < 4:
    print "Missing args: resample.py infile <out_size> <scale>"
    sys.exit(1)
  
  infile = sys.argv[1]
  final_size = float(sys.argv[2])
  sample_ratio = int(re.match( r'([0-9]+)[a-z]?', sys.argv[3]).group(1))
  tile_size = final_size / sample_ratio

  # collect some info about the input file
  src_ds = gdal.Open(infile)
  src_width = src_ds.RasterXSize
  src_height = src_ds.RasterYSize
  SizeTest(src_width, src_height, tile_size)
  
  x_steps = range(0, src_width + tile_size, tile_size)
  y_steps = range(0, src_height + tile_size, tile_size)
  x_steps.pop()
  y_steps.pop()
  
  # 9 different possible conditions to account for
  i = 1
  for y in y_steps:
    for x in x_steps:
      if x == x_steps[0] and y == y_steps[0]:                            # 1 top_left
        condition = 'top_left'
        TopLeft([infile,(x,y),tile_size,i,sample_ratio])
      elif x == x_steps[-1] and y == y_steps[0]:                         # 2 top_right
        condition = 'top_right'
        TopRight([infile,(x,y),tile_size,i,sample_ratio])
      elif y == y_steps[0]:                                              # 3 top
        condition = 'top'
        Top([infile,(x,y),tile_size,i,sample_ratio])
      elif x == x_steps[0] and y != y_steps[0] and y !=  y_steps[-1]:    # 4 left
        condition = 'left'
        Left([infile,(x,y),tile_size,i,sample_ratio])
      elif x == x_steps[-1] and y != y_steps[0] and y !=  y_steps[-1]:   # 5 right
        condition = 'right'
        Right([infile,(x,y),tile_size,i,sample_ratio])
      elif x == x_steps[0] and y == y_steps[-1]:                         # 6 bottom_left
        condition = 'bottom_left'
        BottomLeft([infile,(x,y),tile_size,i,sample_ratio])
      elif x == x_steps[-1] and y == y_steps[-1]:                        # 7 bottom_right
        condition = 'bottom_right'
        BottomRight([infile,(x,y),tile_size,i,sample_ratio])
      elif y == y_steps[-1]:                                             # 8 bottom
        condition = 'bottom'
        Bottom([infile,(x,y),tile_size,i,sample_ratio])
      else:                                                              # 9 middle
        condition = 'middle'
        Middle([infile,(x,y),tile_size,i,sample_ratio])

      i +=1 

if __name__ == '__main__':
  main()


