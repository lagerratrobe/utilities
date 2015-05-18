#! /usr/bin/env python

"""Quick test using gdal to open an input file and wrtie out the contents to a new target file."""

import gdal
import sys
import Numeric
import os.path
from ColorMaker import MakeColor

src_file = sys.argv[1]
dst_file = sys.argv[2]
out_bands = 3

# Open source file
src_ds = gdal.Open( src_file )
src_band = src_ds.GetRasterBand(1)
#width = src_ds.RasterXSize
#height = src_ds.RasterYSize
#numbands = src_ds.RasterCount

# create destination file
## driver.Create( outfile, outwidth, outheight, numbands, gdaldatatype)
dst_driver = gdal.GetDriverByName('GTiff')
dst_ds = dst_driver.Create(dst_file, src_ds.RasterXSize, src_ds.RasterYSize, out_bands, gdal.GDT_Byte) 

# create output bands
band1 = Numeric.zeros([src_ds.RasterYSize, src_ds.RasterXSize])
band2 = Numeric.zeros([src_ds.RasterYSize, src_ds.RasterXSize])
band3 = Numeric.zeros([src_ds.RasterYSize, src_ds.RasterXSize])

# set the projection and georeferencing info
dst_ds.SetProjection( src_ds.GetProjection() )
dst_ds.SetGeoTransform( src_ds.GetGeoTransform() )

# read the source file
gdal.TermProgress( 0.0 )
for iY in range(src_ds.RasterYSize):
  src_data = src_band.ReadAsArray(0,iY,src_ds.RasterXSize,1)
  col_values = src_data[0] # array of z_values, one per row in source data
  for iX in range(src_ds.RasterXSize):
    z_value = col_values[iX]
    # print z_value # randre - test to see what elev values break MakeColor
    new_color = MakeColor(z_value)
    [R,G,B] = new_color.GetValues()
    # [R,G,B] = MakeColor(z_value) # UNCOMMENT THIS AND FUNCTION TO CREATE DISCREET VAKUES
    band1[iY][iX] = R
    band2[iY][iX] = G
    band3[iY][iX] = B
  gdal.TermProgress( (iY+1.0) / src_ds.RasterYSize )

# write each band out
dst_ds.GetRasterBand(1).WriteArray(band1)
dst_ds.GetRasterBand(2).WriteArray(band2)
dst_ds.GetRasterBand(3).WriteArray(band3)

dst_ds = None
