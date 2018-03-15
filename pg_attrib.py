# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("volcanoes.shp")

# create the layer
layer = data_source.CreateLayer("volcanoes", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)

field_region = ogr.FieldDefn("Region", ogr.OFTString)
field_region.SetWidth(24)
layer.CreateField(field_region)

field_elev = ogr.FieldDefn("Elevation", ogr.OFTInteger)
layer.CreateField(field_elev)

# Process the text file and add the attributes and features to the shapefile
for row in reader:
  # create the feature
  feature = ogr.Feature(layer.GetLayerDefn())
  # Set the attributes using the values from the delimited text file
  feature.SetField("Name", row['Name'])
  feature.SetField("Region", row['Region'])
  feature.SetField("Elevation", row['Elev'])

  # create the WKT for the feature using Python string formatting
  wkt = "POINT(%f %f)" %  (float(row['Longitude']) , float(row['Latitude']))

  # Create the point from the Well Known Txt
  point = ogr.CreateGeometryFromWkt(wkt)

  # Set the feature geometry using the point
  feature.SetGeometry(point)
  # Create the feature in the layer (shapefile)
  layer.CreateFeature(feature)
  # Destroy the feature to free resources
  feature.Destroy()

# Destroy the data source to free resources
data_source.Destroy()