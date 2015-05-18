#! /usr/bin/python

import sys
from osgeo import gdal

'''Prints out some basic info about a raster'''

filename = sys.argv[1]

fh = gdal.Open( filename )
xsize = fh.RasterXSize
ysize = fh.RasterYSize
band_type = fh.GetRasterBand(1).DataType
projection = fh.GetProjection()
geotransform = fh.GetGeoTransform()

# randre - print geotransform info
print "x pixel size =", geotransform[1]
print "x rotation =", geotransform[2]
print "y rotation =", geotransform[4]
print "y pixel size =", geotransform[5]
print "ul_x =", geotransform[0]
print "ul_y =", geotransform[3]

ulx = geotransform[0]
lrx = ulx + geotransform[1] * xsize
uly = geotransform[3]
lry = uly + geotransform[5] * ysize




