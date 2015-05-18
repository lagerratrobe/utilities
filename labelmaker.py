#! /usr/bin/python

import sys
from osgeo import ogr

class DataGetter:
  
  def __init__(self, level):
    self.level = level
    db_host = "pgsqlgis-repos"
    db = "pg_geocoding"
    user = "local-dev"
    password = "local-dev"
    connection_string = "PG: host=%s dbname=%s user=%s password=%s" % (db_host, db, user, password)
    self.conn = ogr.Open(connection_string)
    self.processLevel()
    
  def processLevel(self):
    '''Evaluate the level type and activate the right method'''
    if self.level == 'county':
      self.getCountyNames()
      self.getCountyGeom()
      self.destroyConn()
      self.assembleCountyData()
      self.buildCountyShapeFiles()
    # ADD NEW LEVELS BELOW THIS

  def getCountyNames(self):
    print "Retrieving County level names" 
    self.county_names = []
    sql = ("SELECT n.id, "
           "       f.parent_id, "
           "       n.de_de, "
           "       n.en_us, "
           "       n.es_es, "
           "       n.fr_fr, "
           "       n.ja_jp, "
           "       n.ko_kr, "
           "       n.pt_br, "
           "       n.zh_cn, "
           "       n.none, "
           "       n.map_code "
           "  FROM names n, "
           "       features f "
           " WHERE f.class = 2 AND "
           "       n.id = f.id AND "
           "       n.map_code = f.map_code")
    name_layer = self.conn.ExecuteSQL(sql)
    for name in name_layer:
      name_id =  name.GetFieldAsString("id")
      parent_id = name.GetFieldAsString("parent_id")
      de_de = name.GetField("de_de")
      en_us = name.GetField("en_us")
      es_es = name.GetField("es_es")
      fr_fr = name.GetField("fr_fr")
      ja_jp = name.GetField("ja_jp")
      ko_kr = name.GetField("ko_kr")
      pt_br = name.GetField("pt_br")
      zh_cn = name.GetField("zh_cn")
      null  = name.GetField("none")
      map_code = name.GetFieldAsString("map_code")
      # POPULATE EMPTY LANGUAGE FIELDS WITH null TYPE NAME
      if not de_de:
        de_de = null
      if not en_us:
        en_us = null
      if not es_es:
        es_es = null
      if not fr_fr:
        fr_fr = null
      if not ja_jp:
        ja_jp = null
      if not ko_kr:
        ko_kr = null
      if not pt_br:
        pt_br = null
      if not zh_cn:
        zh_cn = null
      # NOTE THAT 'null' TYPE NAME IS DROPPED BELOW
      self.county_names.append([name_id, parent_id, de_de, en_us, es_es, fr_fr, ja_jp, ko_kr, pt_br, zh_cn, map_code])
 
  def getCountyGeom(self):
    print "Retrieving County level point geoms"
    self.county_geoms = []
    sql = ("SELECT p.id, "
           "       ST_TRANSFORM(p.the_geom, '3857'), "
           "       p.map_code "
           "  FROM points p, "
           "       features f "
           " WHERE f.class = 2 AND "
           "       f.id = p.id AND "
           "       f.map_code = p.map_code")
    points_layer = self.conn.ExecuteSQL(sql)
    for point in points_layer:
      pt_id = point.GetFieldAsString("id")
      geom = point.geometry()
      geom_wkt = geom.ExportToWkt()
      map_code = point.GetFieldAsString("map_code")
      self.county_geoms.append([pt_id, geom_wkt, map_code])

  def assembleCountyData(self):
    '''Merge the county_names and county_geoms lists into single records
       which are matched on id and map_code'''
    self.map_code_1_counties = {}
    self.map_code_2_counties = {}
    self.map_code_3_counties = {}
    for name in self.county_names:
      [name_id, parent_id, de_de, en_us, es_es, fr_fr, ja_jp, ko_kr, pt_br, zh_cn, map_code] = name
      if map_code == "0" or map_code == "1":
        self.map_code_1_counties[name_id] = {"parent_id": parent_id,
                                         "de_de": de_de,
                                         "en_us": en_us,
                                         "es_es": es_es,
                                         "fr_fr": fr_fr,
                                         "ja_jp": ja_jp,
                                         "ko_kr": ko_kr,
                                         "pt_br": pt_br,
                                         "zh_cn": zh_cn,
                                         "map_code": map_code}
      if map_code == "0" or map_code == "2":
        self.map_code_2_counties[name_id] = {"parent_id": parent_id,
                                         "de_de": de_de,
                                         "en_us": en_us,
                                         "es_es": es_es,
                                         "fr_fr": fr_fr,
                                         "ja_jp": ja_jp,
                                         "ko_kr": ko_kr,
                                         "pt_br": pt_br,
                                         "zh_cn": zh_cn,
                                         "map_code": map_code}
      if map_code == "0" or map_code == "3":
        self.map_code_3_counties[name_id] = {"parent_id": parent_id,
                                         "de_de": de_de,
                                         "en_us": en_us,
                                         "es_es": es_es,
                                         "fr_fr": fr_fr,
                                         "ja_jp": ja_jp,
                                         "ko_kr": ko_kr,
                                         "pt_br": pt_br,
                                         "zh_cn": zh_cn,
                                         "map_code": map_code}
    for point in self.county_geoms:
      [pt_id, geom_wkt, map_code] = point
      if map_code == "0" or map_code == "1":
        self.map_code_1_counties[pt_id]["geom_wkt"] = geom_wkt
      if map_code == "0" or map_code == "2":
        self.map_code_2_counties[pt_id]["geom_wkt"] = geom_wkt
      if map_code == "0" or map_code == "3":
        self.map_code_3_counties[pt_id]["geom_wkt"] = geom_wkt

  def buildCountyShapeFiles(self):
        print "Writing shapefiles"
        filenames = ["us_admin2_labels.shp", "cn_admin2_labels.shp", "in_admin2_labels.shp"]
        for shapefile in filenames:
          driver = ogr.GetDriverByName('ESRI Shapefile')
          datasource = driver.CreateDataSource(shapefile)
          layer = datasource.CreateLayer('points', geom_type=ogr.wkbPoint, options = ['ENCODING=UTF-8'])
          id_field = ogr.FieldDefn('id', ogr.OFTInteger)
          layer.CreateField(id_field)
          parent_id_field = ogr.FieldDefn('parent_id', ogr.OFTInteger)
          layer.CreateField(parent_id_field)
          map_code_field =  ogr.FieldDefn('map_code', ogr.OFTInteger)
          layer.CreateField(map_code_field)          
          de_de_field = ogr.FieldDefn('de_de', ogr.OFTString)
          layer.CreateField(de_de_field)
          en_us_field = ogr.FieldDefn('en_us', ogr.OFTString)
          layer.CreateField(en_us_field)
          es_es_field = ogr.FieldDefn('es_es', ogr.OFTString)
          layer.CreateField(es_es_field)
          fr_fr_field = ogr.FieldDefn('fr_fr', ogr.OFTString)
          layer.CreateField(fr_fr_field)
          ja_jp_field = ogr.FieldDefn('ja_jp', ogr.OFTString)
          layer.CreateField(ja_jp_field)
          ko_kr_field = ogr.FieldDefn('ko_kr', ogr.OFTString)
          layer.CreateField(ko_kr_field)
          pt_br_field = ogr.FieldDefn('pt_br', ogr.OFTString)
          layer.CreateField(pt_br_field)
          zh_cn_field = ogr.FieldDefn('zh_cn', ogr.OFTString)
          layer.CreateField(zh_cn_field)
          if shapefile == "us_admin2_labels.shp":
            county_data = self.map_code_1_counties
          if shapefile == "cn_admin2_labels.shp":
            county_data = self.map_code_2_counties
          if shapefile == "in_admin2_labels.shp":
            county_data = self.map_code_3_counties
          for record_id in county_data:
            id = record_id
            parent_id = county_data[record_id]["parent_id"]
            map_code = county_data[record_id]["map_code"]
            de_de = county_data[record_id]["de_de"]
            en_us = county_data[record_id]["en_us"]
            es_es = county_data[record_id]["es_es"]
            fr_fr = county_data[record_id]["fr_fr"]
            ja_jp = county_data[record_id]["ja_jp"]
            ko_kr = county_data[record_id]["ko_kr"]
            pt_br = county_data[record_id]["pt_br"]
            zh_cn = county_data[record_id]["zh_cn"]
            wkt = county_data[record_id]["geom_wkt"]
            geom = ogr.CreateGeometryFromWkt(wkt)
            feat = ogr.Feature(layer.GetLayerDefn())
            feat.SetField('id', id)
            feat.SetField('parent_id', parent_id)
            feat.SetField('map_code', map_code)
            feat.SetField('de_de', de_de)
            feat.SetField('en_us', en_us)
            feat.SetField('es_es', es_es)
            feat.SetField('fr_fr', fr_fr)
            feat.SetField('ja_jp', ja_jp)
            feat.SetField('ko_kr', ko_kr)
            feat.SetField('pt_br', pt_br)
            feat.SetField('zh_cn', zh_cn)
            feat.SetGeometry(geom)
            layer.CreateFeature(feat)
            feat.SetGeometry(geom)
          datasource.Destroy()
    

  def destroyConn(self):
    self.conn.Destroy()

################################## END CLASS ################################

def parseOptions():
  # BASIC USAGE STATEMENT
  usage = ("Usage:\n"
           "\textract_map_labels.py <level>\n"
           "\nWhere level is one of [all, country, state, county, city]\n")
  # CRUDE CHECK FOR OPTIONS
  if len(sys.argv) != 2:
    print usage
    sys.exit(1)
  else:
    level = sys.argv[1]
  # LOWERCASE OPTION AND CHECK THAT IT'S VALID
  level = level.lower()
  level_types = ["all", "country", "state", "county", "city"]
  if level not in level_types:
    print "%s\n%s" % ("Unsupported level\n", usage)
    sys.exit(1)
  # IT'S VALID, USE IT
  else:
    return level

def main():
  level = parseOptions()  
  data_factory = DataGetter(level)

if __name__ == '__main__':
  main()
