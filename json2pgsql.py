#! /usr/bin/python

import argparse
import json
from shapely.geometry import shape
from osgeo import ogr, osr

def read_file(args):
  filename = args.filename
  with open(filename) as data_file:
    data = json.load(data_file)
  return data

def read_metadata(args):
  filename = args.metadata
  with open(filename) as metadata_file:
    metadata = json.load(metadata_file)
  return metadata

def get_args():
  parser = argparse.ArgumentParser(description='Reads Geojson file and loads it into PostGIS')
  parser.add_argument('filename', metavar='<filename>', type=str, help='Provide filename to be read')
  parser.add_argument('tablename', metavar='<tablename>', type=str, help='Provide tablename to create')
  parser.add_argument('metadata', metavar='<metadata>', type=str, help='Provide metadata config to read')
  args = parser.parse_args()
  return args

def create_wkt(json_geom):
    '''Takes in jeometry in geojson and emits WKT'''
    shapely_geom = shape(json_geom)
    wkt =  shapely_geom.wkt
    return wkt

def create_table(args, record_data):
  table = args.tablename
  print "Creating table: %s" % (table)
  (database, usr, host) = ('work', 'randre', 'localhost')
  connectionString = "PG: host=%s dbname=%s user=%s" % (host, database, usr)
  data_source = ogr.Open(connectionString, 1) # THE "1" IS MEANINGFUL, ALLOWS APPENDING TO EXISTING TABLE
  table_exists = False # IF TRUE, APPENDS RECORDS TO EXISTING TABLE.  IF FALSE, CREATES NEW TABLE
  # DEFINE THE TABLE
  srs = osr.SpatialReference()
  srs.ImportFromEPSG(4326) # HARDCODING EPSG 4326
  geom_type = ogr.wkbMultiPolygon # NEED TO SET THIS DYNAMICALLY LATER

  if table_exists == False: # CREATE THE TABLE IF IT DOESN"T EXIST
    layer = data_source.CreateLayer(table, srs, geom_type, ['OVERWRITE=YES'] )
    # ADD FIELD DEFINITIONS AND CREATE THEM
    field_name = ogr.FieldDefn("name", ogr.OFTString) # name field
    field_name.SetWidth(128)
    layer.CreateField(field_name)

    field_iso2 = ogr.FieldDefn("iso2", ogr.OFTString) # iso2 field
    field_iso2.SetWidth(2)
    layer.CreateField(field_iso2)
  else:
    layer = data_source.GetLayer(table)

  # PROCESS THE RECORDS, ONE BY ONE HERE
  for row in record_data:
    layerDefn = layer.GetLayerDefn()
    feature = ogr.Feature(layerDefn)
    feature.SetField("name", row['name'])
    feature.SetField("iso2", row['iso2'])
    poly = ogr.CreateGeometryFromWkt(row['wkt'])
    feature.SetGeometry(poly)
    layer.StartTransaction()
    layer.CreateFeature(feature)
    feature = None
    layer.CommitTransaction()

def main():
  args = get_args()
  data = read_file(args)
  config = read_metadata(args)
  load_data = []
  for record in data['features']:
      json_geom = record['geometry']
      wkt_geom = create_wkt(json_geom)
      name = record['properties']['name']
      iso2 = record['properties']['country_code']
      zoom = record['properties']['zoom']
      load_data.append({'name': name, 'iso2': iso2, 'wkt': wkt_geom})
  #config['metadata']
  #config['data_fields']
  #table = create_table(args, load_data)


if __name__ == '__main__':
  main()
