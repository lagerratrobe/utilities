#! /usr/bin/env python

# nc2tif_v2.py

__author__ = '(Roger Andre)'

"""Read in a group of ttnc files, extract a specific layer, and write
out a GeoTIFF of that layer. Given a file named "annual_mean.S10W060.nc",
 and a layer named "windspeed_50m", a new file named
"annual_mean.S10W060_windspeed_50m.tif" will be created.
"""

from glob import glob
import Numeric
import sys
import gdal

class INFILE:
  '''Class to hold info about input file'''

  def __init__(self, file, layer):
    self.file = file
    self.layer = layer
    self.file_root = file.split('.nc')[0]
    self.source_name = 'netCDF:"%s":%s' % (file, layer)
    self.ds = gdal.Open(self.source_name)
    self.band = self.ds.GetRasterBand(1)
    self.metadata = self.ds.GetMetadata()
    if 'NC_GLOBAL#tile_sw_long' not in self.metadata.keys():
      pass
    else:
      self.ll_x = float(self.metadata['NC_GLOBAL#tile_sw_long'])
      self.ll_y = float(self.metadata['NC_GLOBAL#tile_sw_lat'])
      self.degs = float(self.metadata['NC_GLOBAL#tile_size'])
      self.x_size = self.ds.RasterXSize
      self.y_size = self.ds.RasterYSize
      self.ul_x = self.ll_x
      self.ul_y = self.ll_y + self.degs
      self.pix_size_x = self.degs/self.x_size
      self.pix_size_y = -(self.degs/self.y_size)

def MkGeoTIFF(infile_obj, tif_name):
    # CREATE OUTPUT FILE
    tif_drv = gdal.GetDriverByName('GTiff')
    tif_ds = tif_drv.Create(tif_name, infile_obj.x_size, infile_obj.y_size,1, infile_obj.ds.GetRasterBand(1).DataType)
    tif_ds.SetGeoTransform([infile_obj.ul_x, infile_obj.pix_size_x, 0, infile_obj.ul_y, 0, infile_obj.pix_size_y])
    tif_band = tif_ds.GetRasterBand(1)

    # READ INPUT DATA AND WRITE OUTPUT DATA, BACKWARDS
    for iY in range(infile_obj.y_size):
      netcdf_data = infile_obj.band.ReadAsArray(0, iY, infile_obj.x_size, 1)
      tif_band.WriteArray(netcdf_data, 0, abs(iY - infile_obj.y_size) -1 )

def Usage():
  '''Brief use example.'''
  print ('Usage:  nc2tif.py <file_match> <layer_name>'
         '\n'
         '\nWhere <file_match> = regex to match files,'
         '\nand   <layer_name> = NetCDF layer that needs to be extracted.'
         '\n'
         '\nExample: nc2yif.py annual_mean windspeed_50m'
         '\nNOTE: wildcards need to be escaped from the shell, ie, "*.nc"'
        )

def main():
  if len(sys.argv) != 3:
    Usage()
    sys.exit(1) 
   
  match = sys.argv[1]
  layer = sys.argv[2]  
  print 'Extracting: "%s" from: "%s"\n' % (layer, match)

  file_list = glob(match)
  if not file_list:
    print 'No matches found for files named "%s"' % (match)
    sys.exit(1)

  for file in file_list:
    infile_obj = INFILE(file, layer)
    if not infile_obj.ul_x:
      print "%s is missing metadata needed to create GeoTiff" % (file)
      pass
    else:
      file_root = file.split('.nc')[0]
      tif_name = '%s_%s.tif' % (file_root, layer)
      MkGeoTIFF(infile_obj, tif_name)

if __name__ == '__main__':
  main()
