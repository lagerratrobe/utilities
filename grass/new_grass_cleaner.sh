# Reads all shapefiles in a directory and generates internal lines or shells from them

# Script expects polygon geometry as input and generates lines

for i in `ls -1 *.shp | awk -F"." '{print $1}'`
do
v.in.ogr dsn=$i.shp out=$i -o --overwrite
v.clean tool=rmdupl in=$i out=clean_$i --overwrite

# Create a new layer which is a boundary (line) type
v.category clean_$i out=bdy_$i layer=2 type=boundary option=add --overwrite

# Add 'left' and 'right' columns to line layer
v.db.addtable bdy_$i layer=2 col="left integer, right integer" --overwrite

# Identify what is present to the left and right of a line and assign to 'left' and 'right'
v.to.db bdy_$i option=sides col=left,right layer=2 --overwrite

# Create a new table from the lines layer
v.extract layer=2 in=bdy_$i out=boundaries_$i --overwrite

# With '-r' below, the internal lines are generated, without it the external shell.
#v.extract -r boundaries_$i layer=2 out=cleaned_$i where="left = -1" --overwrite
v.extract boundaries_$i layer=2 out=cleaned_$i where="left = -1" --overwrite

v.out.ogr type=boundary in=cleaned_$i layer=2 dsn=cleaned_$i.shp --overwrite
done
