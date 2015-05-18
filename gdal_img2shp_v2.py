#! /usr/bin/python

import ogr
import gdal
import struct
from gdalconst import *

'''Basically a tool to vectorize raster files'''

# POINT GDAL AT OUR INPUT DATA
filename = "sample_area.tif"
dataset = gdal.Open( filename, GA_ReadOnly )
geotransform = dataset.GetGeoTransform()

# Create x_list and y_list arrays
start_x = geotransform[0]
start_y = geotransform[3]

x_list = []
y_list = []

x_i = 0
x_val = start_x
while x_i <= dataset.RasterXSize:
  x_list.append(x_val)
  x_val += geotransform[1]
  x_i += 1

y_i = 0
y_val = start_y
while y_i <= dataset.RasterYSize:
  y_list.append(y_val)
  y_val += geotransform[5]
  y_i += 1


# CREATE A SHAPEFILE TO WRITE THE POLYS TO
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.CreateDataSource('sample_area.shp')
layer = datasource.CreateLayer('polys', geom_type=ogr.wkbPolygon)

# CREATE 'PIXEL_VALUE' ATTRIBUTE FIELD
id_field = ogr.FieldDefn('PIXEL_VALUE', ogr.OFTString)	
layer.CreateField(id_field)						

# READ RASTER DATA
band = dataset.GetRasterBand(1)
row = 0
polys = 0
while row < dataset.RasterYSize:
  scanline = band.ReadRaster( 0, row, band.XSize, 1, band.XSize, 1, GDT_Float32 )
  tuple_of_floats = struct.unpack('f' * band.XSize, scanline)
  total_cols = len(tuple_of_floats)
  col = 0
  for col in range(0,total_cols):
    pixel = tuple_of_floats[col]
    if pixel != 0.0: # <-------------- Set your pixel value here.
      print 'Creating poly for Col: %d, Row: %d' % (col, row)
      xi = col
      yi = row

      # BUILD POLYGON GEOMETRY USING VALUES FROM x_list AND y_list ARRAYS
      x1 = x_list[xi]
      x2 = x_list[xi]
      x3 = x_list[xi + 1]
      x4 = x_list[xi + 1]

      y1 = y_list[yi]
      y2 = y_list[yi + 1]
      y3 = y_list[yi + 1]
      y4 = y_list[yi]
      wkt = 'POLYGON ((%f %f, %f %f, %f %f, %f %f, %f %f))' % (x1,y1, x2,y2, x3,y3, x4,y4, x1,y1)

      # THIS IS WHERE WE CREATE A POLYGON FOR THAT PIXEL
      geom = ogr.CreateGeometryFromWkt(wkt)
      feat = ogr.Feature(layer.GetLayerDefn())
      feat.SetGeometry(geom)

      # SET THE 'PIXEL_VALUE' ATTRIBUTE VALUE
      feat.SetField('PIXEL_VALUE', pixel) 

      # CREATE THE NEW FEATURE
      layer.CreateFeature(feat)
      polys += 1
  row += 1

# CLEAN UP AFTER SHAPEFILE CREATION
datasource.Destroy()

print "Created %d polys" % (polys)



