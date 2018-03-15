#! /usr/bin/python

from osgeo import ogr, osr

database = 'work'
usr = 'randre'
table = 'python_test'
host = 'localhost'
port = '5432'

wkt = "POINT (1120351.5712494177 741921.4223245403)"
point = ogr.CreateGeometryFromWkt(wkt)

connectionString = "PG: host=%s dbname=%s user=%s" % (host, database, usr)
ogrds = ogr.Open(connectionString)

srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

layer = ogrds.CreateLayer(table, srs, ogr.wkbPoint, ['OVERWRITE=YES'] )

layerDefn = layer.GetLayerDefn()

feature = ogr.Feature(layerDefn)
#feature.SetGeometry(point)

layer.StartTransaction()
layer.CreateFeature(feature)
feature = None
layer.CommitTransaction()
