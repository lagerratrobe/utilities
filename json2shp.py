#! /usr/bin/python

import fiona
import fiona.crs
import sys
import geojson
import json
from shapely.geometry import shape

infile = sys.argv[1]
outfile = sys.argv[2]
 
with fiona.open(infile) as source:
  with fiona.open(outfile, 'w', driver='ESRI Shapefile', crs=fiona.crs.from_epsg(4326), schema=source.schema, encoding='UTF-8') as sink:
    for rec in source:
      geometry = rec['geometry']
      #print geometry
      g0 = json.dumps(geometry)
      g1 = geojson.loads(g0)
      g2 = shape(g1)
      #print g2.wkt
      sink.write(rec)
