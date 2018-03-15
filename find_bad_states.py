#! /usr/bin/python

'''find_bad_zips.py - test whether Zip Code point is located within polygon. Report bad zipcodes.'''

__author__ = "Roger Andre, Tableau, March 2012"

import sys
from shapely.wkt import loads
from shapely.geometry import Point

def GetUSAZips():
  '''Returns list of tuples, [(zip, lat, lon, poly_geom)]'''
  usa_zips = []
  zips = open('LocalDataState.csv').readlines()
  for line in zips[1:]:
    line = line.strip()
    line_elem = line.split("|")
    zip = line_elem[0]
    lat = line_elem[1]
    lon = line_elem[2]
    poly_geom = line_elem[3]
    if poly_geom == 'None':
      pass
    else:
      usa_zips.append((zip, lat, lon, poly_geom))
  return usa_zips

def main():
  usa_zips = GetUSAZips()
  for zip in usa_zips:
    code = zip[0]
    lat = float(zip[1])
    lon = float(zip[2])
    poly_geom = zip[3]
    test_point = Point(lon, lat)
    test_poly = loads(poly_geom)
    if test_poly.is_valid:
      if not test_poly.contains(test_point):
        print "%s has a bad centroid" % (code)

if __name__ == '__main__':
  main()
