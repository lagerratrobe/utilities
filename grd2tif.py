#! /usr/bin/env python

# grd2tif.py

'''Reads in a grd file and creates a North-up GeoTIFF from it.
   This is needed because the input files are ordered differently.'''

__author__ = '(Roger Andre)'

from glob import glob
import Numeric
import sys
from osgeo import gdal

def Usage():
  '''Brief use example.'''
  print ('Usage:  grd2tif.py <in_file>')

def MkGeoTIFF(infile):
  name = infile.split('.')[0]
  tif_name = name + ".tif"
  src_ds = gdal.Open( infile )
  src_band = src_ds.GetRasterBand(1)
  width = src_ds.RasterXSize
  height = src_ds.RasterYSize
  numbands = src_ds.RasterCount
  src_geotransform = src_ds.GetGeoTransform()
  #ul_x = float( "%.3f" % (src_geotransform[0]) )
  #ul_y = float( "%.3f" % (src_geotransform[3]) )
  #pix_x = float( "%.3f" % (src_geotransform[1]) )
  #pix_y = float( "%.3f" % (src_geotransform[5]) )
  ul_x = src_geotransform[0]
  ul_y = src_geotransform[3]
  pix_x = src_geotransform[1]
  pix_y = src_geotransform[5]

  # CREATE OUTPUT FILE
  print "Creating: ", tif_name
  tif_drv = gdal.GetDriverByName('GTiff')
  tif_ds = tif_drv.Create(tif_name, width, height,1, src_ds.GetRasterBand(1).DataType)
  # Line below is suspect and needs to be tested.
  tif_ds.SetGeoTransform([ul_x, pix_x, 0, ul_y, 0, pix_y])
  tif_band = tif_ds.GetRasterBand(1)

  # READ INPUT DATA AND WRITE OUTPUT DATA, BACKWARDS
  for iY in range(height):
    src_data = src_band.ReadAsArray(0, iY, width, 1)
    tif_band.WriteArray(src_data, 0, abs(iY - height) -1 )
  
def main():
  if len(sys.argv) != 2:
    Usage()
    sys.exit(1) 
   
  infile = sys.argv[1]
  MkGeoTIFF(infile)

if __name__ == '__main__':
  main()
