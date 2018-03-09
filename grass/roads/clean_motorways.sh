#! /bin/bash

################## MOTORWAYS ############################
# LOAD osm_motorways INTO DB and REPROJECT TO 4326
#ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=roads" -s_srs "EPSG:3857" -t_srs "EPSG:4326" ./ osm_motorways

# REMOVE THE link FEATURES, WE DON'T NEED THEM IN THE SIMPLIFIED DATA
#psql -d roads -c "DELETE FROM osm_motorways WHERE TYPE LIKE '%link'"

#################### UNION THE LINE SEGMENTS INTO LONGER FEATURES
#Select out only the non-link geometries and union them based on 'name', 'ref' and 'type'
psql -d roads -c "CREATE TABLE osm_motorways_union AS SELECT name, ref, type, ST_MULTI(ST_UNION(wkb_geometry)) AS geom FROM osm_motorways GROUP BY name, ref, type"

psql -d roads -c "ALTER TABLE osm_motorways_union ALTER COLUMN geom TYPE geometry(multilinestring, 4326) USING st_setsrid(geom,4326)"

psql -d roads -c "SELECT name, ref, type, (ST_DUMP(ST_LineMerge(geom))).geom AS geom INTO osm_motorways_linemerge FROM osm_motorways_union"
####################

#CLEAN OUT ANY OLD ARTIFACTS
#rm -f gen0_motorways.*

# CLEAN OUT OLD LAYERS IN GRASS
#for i in `g.list -f vect | egrep -v 'world|---'`; do g.remove vect=$i; done

# SET THE GRASS REGION TO BE THE FULL MAPSET
#g.region -d

# CREATE BUFFERED CLASS 1 ROADS IN POSTGIS
#psql -d roads -c "CREATE TABLE motorways_buffer AS SELECT name, st_buffer(geom::geography, 35) AS geom FROM osm_motorways_linemerge"
#psql -d roads -c "ALTER TABLE motorways_buffer ADD COLUMN dis INTEGER"
#psql -d roads -c "UPDATE motorways_buffer SET dis=1"
#psql -d roads -c "CREATE TABLE motorways_dissolve AS SELECT dis, ST_Union(geom::geometry) AS geom FROM motorways_buffer GROUP BY dis"

# CREATE SIMPLIFIED VERSION OF BUFFER
#psql -d roads -c "CREATE TABLE simple_motorways_dissolve AS SELECT st_simplify(motorways_dissolve.geom, .00015) AS geom FROM motorways_dissolve"

# LOAD DATA INTO GRASS DIRECTLY FROM POSTGIS
#v.in.ogr dsn="PG:host=localhost dbname=roads" layer=simple_motorways_dissolve out=motorways_dissolve -o

# CREATE INPUT POINTS FOR VORONOI FUNCTION
#v.to.points in=motorways_dissolve out=motorways_points dmax=.0005

# CREATE VORONOI DIAGRAM
#v.voronoi -l in=motorways_points out=motorways_voronoi

# EXPORT THE VORONOI LINES TO POSTGIS
#v.out.ogr in=motorways_voronoi type=line dsn="PG:host=localhost dbname=roads" olayer=motorways_voronoi format=PostgreSQL

# SET THE SRID OF THE NEW TABLE
#psql -d roads -c "alter table simple_motorways_dissolve alter column geom type geometry(MultiPolygon, 4326) using st_multi(st_setsrid(geom,4326))"

#################################### OPTIMIZATIONS FOR SPEED ###################

# SPLIT THE DISSOLVE BUFFER INTO SMALLER PIECES
#psql -d roads -c "CREATE TABLE simple_motorways_dissolve_dump AS SELECT (ST_Dump(simple_motorways_dissolve.geom)).geom AS geom FROM simple_motorways_dissolve"

# CREATE SPATIAL INDEXES
#psql -d roads -c "CREATE INDEX simple_motorways_dissolve_dump_gix ON simple_motorways_dissolve_dump USING GIST (geom)"
#psql -d roads -c "CREATE INDEX motorways_voronoi_gix ON motorways_voronoi USING GIST (wkb_geometry)"

# REDUCE THE NUMBER OF VORONOI LINES THAT NEED TO BE EXAMINED LATER
#psql -d roads -c "CREATE TABLE motorways_centerline_intersects AS SELECT motorways_voronoi.wkb_geometry AS geom FROM motorways_voronoi, simple_motorways_dissolve_dump WHERE motorways_voronoi.wkb_geometry && simple_motorways_dissolve_dump.geom"

#psql -d roads -c "CREATE INDEX motorways_centerline_intersects_gix ON motorways_centerline_intersects USING GIST (geom)"

#####################################

# EXTRACT CENTER LINE FROM VORONOI DIAGRAM
#psql -d roads -c "CREATE TABLE motorways_centerlines AS SELECT motorways_centerline_intersects.geom AS geom FROM motorways_centerline_intersects, simple_motorways_dissolve_dump WHERE st_within(motorways_centerline_intersects.geom, simple_motorways_dissolve_dump.geom)"

# UNION THE LITLE CENTERLINE SEGMENTS INTO LONGER ONES
psql -d roads -c "ALTER TABLE motorways_centerlines ADD COLUMN name varchar(1)"
psql -d roads -c "CREATE TABLE motorways_centerline_union AS SELECT name, ST_MULTI(ST_UNION(geom)) AS geom FROM motorways_centerlines GROUP BY name"
psql -d roads -c "ALTER TABLE motorways_centerline_union ALTER COLUMN geom TYPE geometry(multilinestring, 4326) USING st_setsrid(geom,4326)"
psql -d roads -c "CREATE TABLE motorways_centerline_linemerge AS SELECT name, (ST_DUMP(ST_LineMerge(geom))).geom AS geom FROM motorways_centerline_union"

# SIMPLIFY THE CENTERLINES TO "UNKINK" THEM FROM THE Voronoi PROCESS
psql -d roads -c "CREATE TABLE simple_motorways_centerlines as select name, st_simplify(geom, .0005) as geom from motorways_centerline_linemerge"

# ADD FIELDS AND VALUES NEEDED IN MAP SERVICE
psql -d roads -c "ALTER TABLE simple_motorways_centerlines ADD COLUMN scalerank integer"
psql -d roads -c "ALTER TABLE simple_motorways_centerlines ADD COLUMN type varchar(24)"
psql -d roads -c "UPDATE simple_motorways_centerlines SET scalerank = 5"
psql -d roads -c "UPDATE simple_motorways_centerlines SET type = 'motorway'"

# DUMP OUT AND REPROJECT
ogr2ogr -f "ESRI Shapefile" gen0_motorways.shp  -s_srs "EPSG:4326" -t_srs "EPSG:3857" PG:"host=localhost dbname=roads" -sql "SELECT * FROM simple_motorways_centerlines"
