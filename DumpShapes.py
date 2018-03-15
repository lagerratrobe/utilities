#! /usr/bin/python

# DumpShape.py

__author__ = 'Roger Andre, randre@tableausoftware.com, Aug 2011'

'''Class to dump shapefile attributes and geometry to CSV files.

   Used to create test data for case 40380'''

import os
from osgeo import ogr

# SET PRECISION OF WKT OUTPUT
os.putenv('OGR_WKT_PRECISION', '4')

class DumpShapes:

  def dumpCountry(self, country_file):
    countries = ogr.Open(country_file)
    countries_lyr = countries[0]
    COUNTRY_CSV = open('LocalDataCountry.CSV', 'w') 
    for feat in countries_lyr:
      iso = feat.GetField('ISO_A2')
      geom = feat.geometry()
      borders = geom.ExportToWkt()
      CSV = "%s\t%s\n" % (iso, borders) 
      COUNTRY_CSV.write(CSV) 
    COUNTRY_CSV.close()

  def dumpStates(self, state_file):
    states = ogr.Open(state_file)
    states_lyr = states[0]
    STATE_CSV = open('LocalDataState.CSV', 'w')
    for feat in states_lyr:
      fips = feat.GetField('FIPS_1')
      geom = feat.geometry()
      borders = geom.ExportToWkt()
      CSV = "%s\t%s\n" % (fips, borders)
      STATE_CSV.write(CSV) 
    STATE_CSV.close()
