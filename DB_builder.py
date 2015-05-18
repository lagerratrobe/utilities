#! /usr/bin/python

from __future__ import with_statement

'''Script to build Firebird database.'''

__author__ = "Roger Andre"

import os
import sys
import string
from glob import glob
from copy import deepcopy
import kinterbasdb
kinterbasdb.init(type_conv=200)

customTPB = (kinterbasdb.isc_tpb_write + kinterbasdb.isc_tpb_read_committed
   + kinterbasdb.isc_tpb_rec_version)
       
################################################

class CheckFiles:
  '''Checks to see what files are contained in the ./local directory. Depending
     on what it finds, does checks to ensure that a logical database can be built.
     Returns a list of valid table names to build.
  '''
  def __init__(self):
    if not os.path.exists('./local'):
      print '\nERROR: You need a folder named "local" (all lower case)\n'
      sys.exit(1)
    else:
      self.infiles = glob("./local/*.csv")
      self.checkContents()

  def checkCountryLevel(self):
    '''Check that all 3 country level tables will have data'''
    level_tables = ["LocalDataCountry", "CountrySynonyms", "Country"]
    for table in level_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from country level data\n" % (table)
        print error_msg
        sys.exit(1)

  def checkStateLevel(self):
    '''Check that all the state tables are there, AND that country tables exit'''
    state_tables = ['LocalDataState', 'StateSynonyms']
    for table in state_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from state level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkCountryLevel()

  def checkCountyLevel(self):
    '''Check that all county tables are there, AND state, AND country'''
    county_tables = ['LocalDataCounty', 'CountySynonyms']
    for table in county_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from county level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkStateLevel()
    self.checkCountryLevel()

  def checkCongressLevel(self):
    '''Check that all congress tables are there, AND state, AND country'''
    congress_tables = ['LocalDataCongress', 'CongressSynonyms']
    for table in congress_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from congress level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkStateLevel()
    self.checkCountryLevel()

  def checkCMSALevel(self):
    '''Check that all CMSA tables are there, AND country'''
    cmsa_tables = ["CMSA", "LocalDataCMSA", "CMSASynonyms"] 
    for table in cmsa_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from CMSA level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkCountryLevel()

  def checkCityLevel(self):
    '''Check that all City tables are there, AND state, AND country'''
    city_tables = ["City", "CitySynonyms", "LocalDataCity"]
    for table in city_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from city level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkStateLevel()
    self.checkCountryLevel() 

  def checkAreaCodeLevel(self):
    '''Check that all AreaCode tables are there, AND country'''
    areacode_tables = ["AreaCode", "LocalDataAreaCode"]
    for table in areacode_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from area code level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkCountryLevel() 

  def checkZipCodeLevel(self):
    '''Check that all ZipCode tables are there, AND country'''
    zipcode_tables = ["ZipCode", "LocalDataZipCode"]
    for table in zipcode_tables:
      if table not in self.tables:
        error_msg = "\nERROR: Missing %s.csv from zip code level data\n" % (table)
        print error_msg
        sys.exit(1)
    self.checkCountryLevel() 

  def checkContents(self):
    '''Check that the files in 'local' folder make sense'''
    # TABLES THAT USER WANTS TO BUILD
    self.tables = []
    for csv_file in self.infiles:
      basename = os.path.basename(csv_file)
      table_name = os.path.splitext(basename)[0]
      self.tables.append(table_name)
    # TEST THAT THERE IS AT LEAST ONE 'CORE' TABLE BEING BUILT
    base_tables = ["Country", "State", "County", "Congress", "City", "CMSA", "AreaCode", "ZipCode"]
    has_base = 0
    for table in base_tables:
      if table in self.tables:
        has_base += 1
    if has_base == 0:
      print "\nERROR: Missing at least one base-table in source files\n"
      sys.exit(1)
    # CHECK THAT COUNTRY LEVEL CAN BE BUILT    
    if "Country" in self.tables:
      self.checkCountryLevel()
    # CHECK THAT STATE LEVEL CAN BE BUILT
    if "State" in self.tables:
      self.checkStateLevel()
    # CHECK THAT COUNTY LEVEL CAN BE BUILT
    if "County" in self.tables:
      self.checkCountyLevel()
    # CHECK THAT CONGRESS LEVEL CAN BE BUILT
    if "Congress" in self.tables:
      self.checkCongressLevel()
    # CHECK THAT CMSA LEVEL CAN BE BUILT
    if "CMSA" in self.tables:
      self.checkCMSALevel()
    # CHECK THAT CITY LEVEL CAN BE BUILT
    if "City" in self.tables:
      self.checkCityLevel()
    # CHECK THAT AREACODE LEVEL CAN BE BUILT
    if "AreaCode" in self.tables:
      self.checkAreaCodeLevel()
    # CHECK THAT ZIPCODE LEVEL CAN BE BUILT
    if "ZipCode" in self.tables:
      self.checkZipCodeLevel()
    return self.tables

  def returnTables(self):
    return self.tables

################################################

class CreateDB:
  
  def __init__(self, dbname, tables):
    self.dbname = dbname
    self.tables = tables
    self.login = 'sysdba'
    self.passwd = 'masterkey'
    self.table_defs = {
      # COUNTRY LEVEL TABLES
      "Country": [
        '"ID" integer,'
        '"ParentID" integer default null,'
        '"FIPS" varchar(2) character set UTF8 not null collate UNICODE_CI,'
        '"ISO3166_2" varchar(2) CHARACTER SET UTF8 COLLATE UNICODE_CI,'
        '"ISO3166_3" varchar(3) CHARACTER SET UTF8 COLLATE UNICODE_CI,' 
        '"MapCode" smallint not null,'
        'constraint PK_COUNTRY primary key ("ID", "MapCode")'],
      "CountrySynonyms": [ 
        '"ParentID" integer default null,'
        '"Name" varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"IsDisplayName" smallint default 1,'
        '"MapCode" smallint not null,'
        'constraint FK_SYNONYMS_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      "LocalDataCountry": [ 
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      # STATE LEVEL TABLES
      "State": [ 
        '"ID" integer,'
        '"ParentID"integer not null,'
        '"MapCode" smallint not null,'
        'constraint PK_STATE primary key ("ID", "MapCode"),'
        'constraint FK_STATE_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      "StateSynonyms": [
        '"ParentID" integer default null,'
        '"Name" varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"IsDisplayName" smallint default 1,'
        '"MapCode" smallint not null,'
        'constraint FK_SYNONYMS_STATE foreign key ("ParentID", "MapCode") references "State"("ID", "MapCode")'],
      "LocalDataState": [
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_STATE foreign key ("ParentID", "MapCode") references "State"("ID", "MapCode")'],
      # COUNTY LEVEL TABLES
      "County": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"MapCode" smallint not null,'
        'constraint PK_COUNTY primary key ("ID", "MapCode"),'
        'constraint FK_COUNTY_STATE foreign key ("ParentID", "MapCode") references "State"("ID", "MapCode")'],
      "CountySynonyms": [ 
        '"ParentID" integer default null,'
        '"Name"  varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"IsDisplayName" smallint default 1,'
        '"MapCode" smallint not null,'
        'constraint FK_SYNONYMS_COUNTY foreign key ("ParentID", "MapCode") references "County"("ID", "MapCode")'],
      "LocalDataCounty": [
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_COUNTY foreign key ("ParentID", "MapCode") references "County"("ID", "MapCode")'],
      # CONGRESS LEVEL TABLES
      "Congress": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"MapCode" smallint not null,'
        'constraint PK_CONGRESS primary key ("ID", "MapCode"),'
        'constraint FK_CONGRESS_STATE foreign key ("ParentID", "MapCode") references "State"("ID", "MapCode")'],
      "CongressSynonyms": [
        '"ParentID" integer default null,'
        '"Name"  varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"MapCode" smallint not null,'
        '"IsDisplayName" smallint default 1,'
        'constraint FK_SYNONYMS_CONGRESS foreign key ("ParentID", "MapCode") references "Congress"("ID", "MapCode")'],
      "LocalDataCongress": [
        '"ParentID" integer not null,'
        '"Latitude"  decimal(18,15) not null,'
        '"Longitude"  decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_CONGRESS foreign key ("ParentID", "MapCode") references "Congress"("ID", "MapCode")'],
      # ZIPCODE LEVEL TABLES
      "ZipCode": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"Name" varchar(5) not null,'
        '"MapCode" smallint not null,'
        'constraint PK_ZIP primary key ("ID", "MapCode"),'
        'constraint FK_ZIPCODE_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      "LocalDataZipCode": [
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_ZIPCODE foreign key ("ParentID", "MapCode") references "ZipCode"("ID", "MapCode")'],
      # AREACODE LEVEL TABLES
      "AreaCode": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"Name" char(3) not null,'
        '"MapCode" smallint not null,'
        'constraint PK_AREACODE primary key ("ID", "MapCode"),' 
        'constraint FK_AREACODE_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      "LocalDataAreaCode": [
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_AREACODE foreign key ("ParentID", "MapCode") references "AreaCode"("ID", "MapCode")'],
      # CMSA LEVEL TABLES
      "CMSA": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"MapCode" smallint not null,'
        'constraint PK_CMSA primary key ("ID", "MapCode"),'
        'constraint FK_CMSA_COUNTRY foreign key ("ParentID", "MapCode") references "Country"("ID", "MapCode")'],
      "CMSASynonyms": [
        '"ParentID" integer default null,'
        '"Name" varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"IsDisplayName" smallint default 1,'
        '"MapCode" smallint not null,'
        'constraint FK_SYNONYMS_CMSA foreign key ("ParentID", "MapCode") references "CMSA"("ID", "MapCode")'],
      "LocalDataCMSA": [
        '"ParentID"integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"Geometry" blob sub_type text,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_CMSA foreign key ("ParentID", "MapCode") references "CMSA"("ID", "MapCode")'],
      # CITY LEVEL TABLES
      "City": [
        '"ID" integer,'
        '"ParentID" integer not null,'
        '"MapCode" smallint not null,'
        'constraint PK_CITY primary key ("ID", "MapCode"),'
        'constraint FK_CITY_STATE foreign key ("ParentID", "MapCode") references "State"("ID", "MapCode")'],
      "CitySynonyms": [
        '"ParentID" integer default null,'
        '"Name" varchar(64) character set UTF8 not null collate UNICODE_CI,'
        '"Locale" varchar(8) character set UTF8 collate UNICODE_CI,'
        '"IsDisplayName" smallint default 1,'
        '"MapCode" smallint not null,'
        'constraint FK_SYNONYMS_CITY foreign key ("ParentID", "MapCode") references "City"("ID", "MapCode")'],
      "LocalDataCity": [
        '"ParentID" integer not null,'
        '"Latitude" decimal(18,15) not null,'
        '"Longitude" decimal(18,15) not null,'
        '"MapCode" smallint not null,'
        'constraint FK_LOCALDATA_CITY foreign key ("ParentID", "MapCode") references "City"("ID", "MapCode")'],
      # HIERARCHIES
      "Hierarchies": [
        '"ID" integer primary key,'
        '"Name" varchar(32) not null,'
        '"Detail" integer not null,'
        '"ParentID" integer not null'],
      # HEURISTICS
      "Heuristics": [
        '"ID" integer primary key,'
        '"Level" varchar(128) not null,'
        '"Pattern" varchar(64) not null,'
        '"Data Type" smallint not null,'
        '"Width" smallint default null,'
        '"Format" varchar(64) default null'],
      # PROPERTIES
      "Properties": [
        '"ID"  integer primary key,'
        '"Level" varchar(128) not null,'
        '"Key" varchar(64) not null,'
        '"Value" varchar(1024) default null']}
    self.index_defs = {"Country": [('"idx_Country_FIPS"', '"Country"("FIPS")'),
                                   ('"idx_Country_ISO3166_2"', '"Country"("ISO3166_2")'),
                                   ('"idx_Country_ISO3166_3"', '"Country"("ISO3166_3")'),
                                   ('"idx_Country_Name"', '"CountrySynonyms"("Name")')],
                       "State":   [('"idx_State_Name"', '"StateSynonyms"("Name")')],
                       "County":  [('"idx_County_Name"','"CountySynonyms"("Name")')],
                     "Congress":  [('"idx_Congress_Name"','"CongressSynonyms"("Name")')],
                       "ZipCode": [('"idx_ZipCode_Name"', '"ZipCode"("Name")')],
                      "AreaCode": [('"idx_AreaCode_Name"', '"AreaCode"("Name")')],
                          "CMSA": [('"idx_CMSA_Name"', '"CMSASynonyms"("Name")')],
                          "City": [('"idx_City_Name"', '"CitySynonyms"("Name")')]}
    self.makeDB()

  def makeDB(self):
    create_string = "CREATE DATABASE '%s' user '%s' password '%s'" % (
      self.dbname, self.login, self.passwd)
    if os.path.exists(self.dbname):
      os.remove(self.dbname)
    geocoding_db = kinterbasdb.create_database(create_string)  
    self.makeConnection()

  def makeConnection(self):
    customTPB = (kinterbasdb.isc_tpb_write + kinterbasdb.isc_tpb_read_committed
      + kinterbasdb.isc_tpb_rec_version)
    self.con = kinterbasdb.connect(dsn=self.dbname, user=self.login, password=self.passwd)
    self.con.begin(tpb=customTPB)
    self.cur = self.con.cursor()
    self.makeTables()

  def makeIndexes(self):
    index_levels = self.index_defs.keys()
    for table in self.tables:
      if table in index_levels:
        indexes = self.index_defs[table]
        for index_def in indexes:
          [index_name, rule] = index_def
          create_string = 'CREATE ASC INDEX %s ON %s' % (index_name, rule)
          self.con.commit()
          self.con.begin(tpb=customTPB)
          self.cur.execute(create_string)
          self.con.commit()

  def makeTables(self):
    # IT MATTERS IN WHAT ORDER THESE TABLES ARE BUILT
    table_order = ["Country", "CountrySynonyms", "LocalDataCountry",
                   "State", "StateSynonyms", "LocalDataState",
                   "County", "CountySynonyms", "LocalDataCounty",
                   "Congress", "CongressSynonyms", "LocalDataCongress",
                   "ZipCode", "LocalDataZipCode", "AreaCode", "LocalDataAreaCode",
                   "CMSA", "CMSASynonyms", "LocalDataCMSA",
                   "City", "CitySynonyms", "LocalDataCity",
                   "Hierarchies", "Heuristics", "Properties"]
    # FIGURE OUT WHAT ORDER THE TABLES EXIST IN IDEALLY AND SORT WHAT WE HAVE ACCORDINGLY
    index_order = [] 
    for table in self.tables:
      if table in table_order:
        index_position = table_order.index(table)
        index_order.append(index_position)
    index_order.sort()
    build_order = []
    for i in index_order:
      build_order.append(table_order[i])
    # CREATE THE TABLES
    for table_name in build_order:
      fields = self.table_defs[table_name][0]
      create_string = 'CREATE TABLE "%s" (%s)' % (table_name, fields)
      self.con.commit()
      self.con.begin(tpb=customTPB)
      self.cur.execute(create_string)
      self.con.commit()
    self.makeIndexes()

################################################

class LoadDB:
  '''Takes in a list of table names, grabs the appropriate file from the ./local
     directory, parses it and loads it into the database.
  '''
  def __init__(self, tables, con, cur):
    self.tables = tables
    self.con = con
    self.cur = cur
    self.loadTables()

  def addCountry(self):
    # UPDATE Country TABLE
    print "Adding Country info"
    Country_csv = 'local/Country.csv'
    country_info = open(Country_csv)
    insertStatement = 'INSERT INTO "Country" ("ID", "ParentID", "FIPS", "ISO3166_2", "ISO3166_3", "MapCode") values (?,?,?,?,?,?)'
    i = 0
    for country in country_info.readlines()[1:]:
      country = country.strip()
      [ID, ParentID, FIPS, ISO3166_2, ISO3166_3, MapCode] = country.split('|')
      if ParentID == "None":
        ParentID = None
      self.con.commit()
      self.con.begin(tpb=customTPB)
      self.cur.execute(insertStatement, (ID, ParentID, FIPS, ISO3166_2, ISO3166_3, MapCode))
      i += 1
    print "Inserted %d Countries \n" % (i)

  def addCountrySynonyms(self):
    # UPDATE CountrySynonyms TABLE
    print "Adding Country names"
    Country_names_csv = 'local/CountrySynonyms.csv'
    country_names = open(Country_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "CountrySynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for country_name in country_names.readlines()[1:]:
      country_name = country_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = country_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d Country names \n" % (i)

  def addLocalDataCountry(self):
    print "Adding Country geometry"
    LocalDataCountry_csv = 'local/LocalDataCountry.csv'
    LocalDataCountry_data = open(LocalDataCountry_csv)
    insertStatement = 'INSERT INTO "LocalDataCountry" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    i = 0
    for country_geom in LocalDataCountry_data.readlines()[1:]:
      country_geom = country_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = country_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d Country geometries \n" % (i)    

  def addState(self):
    '''Updates State table of foo.FDB'''
    print "Adding State info"
    State_csv = 'local/State.csv'
    State_data = open(State_csv)
    insertStatement = 'INSERT INTO "State" ("ID", "ParentID", "MapCode") values (?,?,?)'
    i = 0
    for state_info in State_data.readlines()[1:]:
      state_info = state_info.strip()
      [ID, ParentID, MapCode] = state_info.split('|')
      self.cur.execute(insertStatement, (ID, ParentID, MapCode))
      i += 1
    print "Inserted %d States \n" % (i)

  def addStateSynonyms(self):
    '''Updates StateSynonyms table of foo.FDB'''
    print "Adding State names"
    State_names_csv = 'local/StateSynonyms.csv'
    state_names = open(State_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "StateSynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for state_name in state_names.readlines()[1:]:
      state_name = state_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = state_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d State names \n" % (i)

  def addLocalDataState(self):
    '''Updates LocalDataState table of foo.FDB'''
    print "Adding State geometry"
    LocalDataState_csv = 'local/LocalDataState.csv'
    LocalDataState_data = open(LocalDataState_csv)
    i = 0
    insertStatement = 'INSERT INTO "LocalDataState" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    for state_geom in LocalDataState_data.readlines()[1:]:
      state_geom = state_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = state_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d State geometries \n" % (i)

  def addCounty(self):
    '''Updates County table of foo.FDB'''
    print "Adding County info"
    County_csv = 'local/County.csv'
    County_data = open(County_csv)
    i = 0
    insertStatement = 'INSERT INTO "County" ("ID", "ParentID", "MapCode") values (?,?,?)'
    for county_info in County_data.readlines()[1:]:
      county_info = county_info.strip()
      [ID, ParentID, MapCode] = county_info.split('|')
      self.cur.execute(insertStatement, (ID, ParentID, MapCode))
      i += 1
    print "Inserted %d Counties \n" % (i)

  def addCountySynonyms(self):
    '''Updates CountySynonyms table of foo.FDB'''
    print "Adding County names"
    County_names_csv = 'local/CountySynonyms.csv'
    county_names = open(County_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "CountySynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for county_name in county_names.readlines()[1:]:
      county_name = county_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = county_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d County names \n" % (i)

  def addLocalDataCounty(self):
    '''Updates LocalDataCounty table of foo.FDB'''
    print "Adding County geometry"
    LocalDataCounty_csv = 'local/LocalDataCounty.csv'
    LocalDataCounty_data = open(LocalDataCounty_csv)
    i = 0
    insertStatement = 'INSERT INTO "LocalDataCounty" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    for county_geom in LocalDataCounty_data.readlines()[1:]:
      county_geom = county_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = county_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d County geometries \n" % (i)

  def addCongress(self):
    '''Updates Congress table of foo.FDB'''
    print "Adding Congress info"
    Congress_csv = 'local/Congress.csv'
    Congress_data = open(Congress_csv)
    i = 0
    insertStatement = 'INSERT INTO "Congress" ("ID", "ParentID", "MapCode") values (?,?,?)'
    for congress_info in Congress_data.readlines()[1:]:
      congress_info = congress_info.strip()
      [ID, ParentID, MapCode] = congress_info.split('|')
      self.cur.execute(insertStatement, (ID, ParentID, MapCode))
      i += 1
    print "Inserted %d Congress Districts \n" % (i)

  def addCongressSynonyms(self):
    '''Updates CongressSynonyms table of foo.FDB'''
    print "Adding Congress District names"
    Congress_names_csv = 'local/CongressSynonyms.csv'
    congress_names = open(Congress_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "CongressSynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for congress_name in congress_names.readlines()[1:]:
      congress_name = congress_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = congress_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d Congress District names \n" % (i)

  def addLocalDataCongress(self):
    '''Updates LocalDataCongress table of foo.FDB'''
    print "Adding Congress geometry"
    LocalDataCongress_csv = 'local/LocalDataCongress.csv'
    LocalDataCongress_data = open(LocalDataCongress_csv)
    i = 0
    insertStatement = 'INSERT INTO "LocalDataCongress" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    for congress_geom in LocalDataCongress_data.readlines()[1:]:
      congress_geom = congress_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = congress_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d Congress District geometries \n" % (i)

  def addZipCode(self):
    '''Updates ZipCode table of foo.FDB'''
    print "Adding ZipCode info"
    ZipCode_csv = 'local/ZipCode.csv'
    ZipCode_data = open(ZipCode_csv)
    i = 0
    insertStatement = 'INSERT INTO "ZipCode" ("ID", "ParentID", "Name", "MapCode") values (?,?,?,?)'
    for zipcode_info in ZipCode_data.readlines()[1:]:
      zipcode_info = zipcode_info.strip()
      [ID, ParentID, Name, MapCode] = zipcode_info.split('|')
      self.cur.execute(insertStatement, (ID, ParentID, Name, MapCode))
      i += 1
    print "Inserted %d ZipCodes \n" % (i)

  def addLocalDataZipCode(self):
    '''Updates LocalDataZipCode table of foo.FDB'''
    print "Adding ZipCode geometry"
    LocalDataZipCode_csv = 'local/LocalDataZipCode.csv'
    LocalDataZipCode_data = open(LocalDataZipCode_csv)
    i = 0
    insertStatement = 'INSERT INTO "LocalDataZipCode" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    for zipcode_geom in LocalDataZipCode_data.readlines()[1:]:
      zipcode_geom = zipcode_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = zipcode_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d ZipCode points \n" % (i)
  

  def addAreaCode(self):
    '''Updates AreaCode table of foo.FDB'''
    print "Adding AreaCode info"
    AreaCode_csv = 'local/AreaCode.csv'
    AreaCode_data = open(AreaCode_csv)
    i = 0
    for areacode_info in AreaCode_data.readlines()[1:]:
      areacode_info = areacode_info.strip()
      [ID, ParentID, Name, MapCode] = areacode_info.split('|')
      record = "(%s, %s, '%s', %s)" % (ID, ParentID, Name, MapCode)
      insert_statement = '''INSERT INTO "AreaCode" ("ID", "ParentID", "Name", "MapCode") values %s''' % (record)
      self.cur.execute(insert_statement)
      i += 1
    print "Inserted %d AreaCodes \n" % (i)


  def addLocalDataAreaCode(self):
    '''Updates LocalDataAreaCode table of foo.FDB'''
    print "Adding AreaCode geometry"
    LocalDataAreaCode_csv = 'local/LocalDataAreaCode.csv'
    LocalDataAreaCode_data = open(LocalDataAreaCode_csv)
    i = 0
    for areacode_geom in LocalDataAreaCode_data.readlines()[1:]:
      areacode_geom = areacode_geom.strip()
      [ParentID, Latitude, Longitude, MapCode] = areacode_geom.split('|')
      record = "(%s, %s, %s, %s)" % (ParentID, Latitude, Longitude, MapCode)
      insert_statement = '''INSERT INTO "LocalDataAreaCode" ("ParentID", "Latitude", "Longitude", "MapCode") values %s''' % (record)
      self.cur.execute(insert_statement)
      i += 1
    print "Inserted %d AreaCode points \n" % (i)
  

  def addCMSA(self):
    '''Updates CMSA table of foo.FDB'''
    print "Adding CMSA info"
    CMSA_csv = 'local/CMSA.csv'
    CMSA_data = open(CMSA_csv)
    i = 0
    for cmsa_info in CMSA_data.readlines()[1:]:
      cmsa_info = cmsa_info.strip()
      [ID, ParentID, MapCode] = cmsa_info.split('|')
      record = "(%s, %s, %s)" % (ID, ParentID, MapCode)
      insert_statement = '''INSERT INTO "CMSA" ("ID", "ParentID", "MapCode") values %s''' % (record)
      self.cur.execute(insert_statement)
      i += 1
    print "Inserted %d CMSA's \n" % (i)


  def addCMSASynonyms(self):
    '''Updates CMSASynonyms table of foo.FDB'''
    print "Adding CMSA names"
    CMSA_names_csv = 'local/CMSASynonyms.csv'
    cmsa_names = open(CMSA_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "CMSASynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for cmsa_name in cmsa_names.readlines()[1:]:
      cmsa_name = cmsa_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = cmsa_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d CMSA names \n" % (i)


  def addLocalDataCMSA(self):
    '''Updates LocalDataCMSA table of foo.FDB'''
    print "Adding CMSA geometry"
    LocalDataCMSA_csv = 'local/LocalDataCMSA.csv'
    LocalDataCMSA_data = open(LocalDataCMSA_csv)
    i = 0
    insertStatement = 'INSERT INTO "LocalDataCMSA" ("ParentID", "Latitude", "Longitude", "Geometry", "MapCode") values (?,?,?,?,?)'
    for cmsa_geom in LocalDataCMSA_data.readlines()[1:]:
      cmsa_geom = cmsa_geom.strip()
      [ParentID, Latitude, Longitude, Geometry, MapCode] = cmsa_geom.split('|')
      if Geometry == "None":
        Geometry = None
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, Geometry, MapCode))
      i += 1
    print "Inserted %d CMSA geometries \n" % (i)


  def addCity(self):
    '''Updates City table of foo.FDB'''
    print "Adding City info"
    City_csv = 'local/City.csv'
    City_data = open(City_csv)
    i = 0
    insertStatement = 'INSERT INTO "City" ("ID", "ParentID", "MapCode") values (?,?,?)'
    for city_info in City_data.readlines()[1:]:
      city_info = city_info.strip()
      [ID, ParentID, MapCode] = city_info.split('|')
      self.cur.execute(insertStatement, (ID, ParentID, MapCode))
      i += 1
    print "Inserted %d Cities \n" % (i)


  def addCitySynonyms(self):
    '''Updates CitySynonyms table of foo.FDB'''
    print "Adding City names"
    City_names_csv = 'local/CitySynonyms.csv'
    city_names = open(City_names_csv)
    i = 0
    insertStatement = 'INSERT INTO "CitySynonyms" ("ParentID", "Name", "Locale", "IsDisplayName", "MapCode") values (?,?,?,?,?)'
    for city_name in city_names.readlines()[1:]:
      city_name = city_name.strip()
      [ParentID, Name, Locale, IsDisplayName, MapCode] = city_name.split('|')
      if Locale == "None" or Locale == "":
        Locale = None;
      self.cur.execute(insertStatement, (ParentID, Name, Locale, IsDisplayName, MapCode))
      i += 1
    print "Inserted %d City names \n" % (i)


  def addLocalDataCity(self):
    '''Updates LocalDataCity table of foo.FDB'''
    print "Adding City geometry"
    LocalDataCity_csv = 'local/LocalDataCity.csv'
    LocalDataCity_data = open(LocalDataCity_csv)
    i = 0 
    insertStatement = 'INSERT INTO "LocalDataCity" ("ParentID", "Latitude", "Longitude", "MapCode") values (?,?,?,?)'
    for city_geom in LocalDataCity_data.readlines()[1:]:
      city_geom = city_geom.strip()
      [ParentID, Latitude, Longitude, MapCode] = city_geom.split('|')
      self.cur.execute(insertStatement, (ParentID, Latitude, Longitude, MapCode))
      i += 1
    print "Inserted %d City geometries \n" % (i)
  

  def addHierarchies(self):
    '''Updates Hierarchies table of foo.FDB'''
    print "Adding Hierarchies"
    Hierarchies_csv = 'local/Hierarchies.csv'
    hierarchies = open(Hierarchies_csv)
    i = 0
    for level in hierarchies.readlines()[1:]:
      level = level.strip()
      [ID, Name, Detail, ParentID] = level.split('|')
      record = "(%s, '%s', %s, %s)" % (ID, Name, Detail, ParentID)
      insert_statement = '''insert into "Hierarchies" ("ID", "Name", "Detail", "ParentID") values %s''' % (record)
      self.cur.execute(insert_statement)
      i += 1
    print "Inserted %d Hierarchies \n" % (i)
  

  def addHeuristics(self):
    '''Updates Heuristics table of foo.FDB'''
    print "Adding Heuristics"
    Heuristics_csv = 'local/Heuristics.csv'
    heuristics = open(Heuristics_csv)
    insertStatement = 'INSERT INTO "Heuristics" ("ID", "Level", "Pattern", "Data Type", "Width", "Format") values (?,?,?,?,?,?)'
    i = 0
    for rule in heuristics.readlines()[1:]:
      rule = rule.strip()
      [ID,  Level, Pattern, Data_Type, Width, Format] = rule.split('|')
      if Format == "None":
        Format = None
      if Width == "None":
        Width = None
      self.cur.execute(insertStatement, (ID,  Level, Pattern, Data_Type, Width, Format))
      i += 1
    print "Inserted %d Heuristics \n" % (i)


  def addProperties(self):
    '''Updates Properties table of foo.FDB'''
    print "Merging translations and adding Properties"
    dir = "local"
    baseName = "Properties.csv"
    files = {}
    files[ "" ] = os.path.join( dir, baseName )
    for lang in os.listdir( dir ):
        if os.path.isdir( os.path.join( dir, lang ) ):
            path = os.path.join( dir, lang, baseName )
            if os.path.exists( path ):
                files[ lang ] = path
    ID = 0
    for lang in files.iterkeys():
        path = files[ lang ]
        print "  reading from %s" % ( path )
        with open( path ) as properties:
            for property in properties.readlines()[1:]:
                property = property.strip()
                [Level, Key, Value] = property.split('|')
                if lang:
                    Key = "%s_%s" % ( Key, lang )            
                record = "(%d, '%s', '%s', '%s')" % (ID,  Level, Key, Value)
                insert_statement = '''insert into "Properties" ("ID", "Level", "Key", "Value") values %s''' % (record)
                self.cur.execute(insert_statement)
                ID += 1
    print "Inserted %d Properties \n" % ( ID )
    
  def loadTables(self):
    if "Country" in self.tables:
      self.addCountry()
      self.addCountrySynonyms()
      self.addLocalDataCountry()
    if "State" in self.tables:
      self.addState()
      self.addStateSynonyms()
      self.addLocalDataState()
    if "County" in self.tables:
      self.addCounty()
      self.addCountySynonyms()
      self.addLocalDataCounty()
    if "Congress" in self.tables:
      self.addCongress()
      self.addCongressSynonyms()
      self.addLocalDataCongress()
    if "ZipCode" in self.tables:
      self.addZipCode()
      self.addLocalDataZipCode()
    if "AreaCode" in self.tables:
      self.addAreaCode()
      self.addLocalDataAreaCode()
    if "CMSA" in self.tables:
      self.addCMSA()
      self.addCMSASynonyms()
      self.addLocalDataCMSA()
    if "City" in self.tables:
      self.addCity()
      self.addCitySynonyms()
      self.addLocalDataCity()
    if "Hierarchies" in self.tables:
      self.addHierarchies()
    if "Heuristics" in self.tables:
      self.addHeuristics()
    if "Properties" in self.tables:
      self.addProperties()

    print "Committing changes to database"
    self.con.commit()
    
################################################

def main(dbname = 'foo.FDB'):
  if len(sys.argv) > 1:
    dbname = sys.argv[1]
  file_check = CheckFiles()
  tables = file_check.returnTables()
  database = CreateDB(dbname, tables)
  cursor = database.cur
  connection = database.con

  reload(sys)
  sys.setdefaultencoding( "utf-8" )
 
  LoadDB(tables, connection, cursor)

if __name__ == '__main__':
  main()
