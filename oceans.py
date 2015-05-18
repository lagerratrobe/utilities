#! /usr/bin/python

from osgeo import ogr

'''Quick and dirty way to create a global background poly for a basemap'''

driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.CreateDataSource('alasja_clip.shp')
layer = datasource.CreateLayer('polys', geom_type=ogr.wkbPolygon)

polygons = [(-180.0,90.0, -180.0,0.0, -129.95,0.0, -129.95,90.0)]

# CREATE POLYGON GEOMETRY
for polygon in polygons:
  (x1,y1,x2,y2,x3,y3,x4,y4) = polygon
  wkt = 'POLYGON ((%f %f, %f %f, %f %f, %f %f, %f %f))' % (
                         x1,y1, x2,y2, x3,y3, x4,y4, x1,y1)
  print wkt
  geom = ogr.CreateGeometryFromWkt(wkt)
  feat = ogr.Feature(layer.GetLayerDefn())
  feat.SetGeometry(geom)
  layer.CreateFeature(feat)

datasource.Destroy()
