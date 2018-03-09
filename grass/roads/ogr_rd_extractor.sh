#! /bin/bash

# SCRIPT TO EXTRACT Streets FEATURE CLASS FROM file.gdb

ogrinfo file.gdb/ -sql "SELECT Link_ID, StreetName, FuncClass, RestrictCars, Ramp, ISOCountryCode, FerryType, Shape FROM Streets" \
| sed 's/ = $/ = Blank/' \
| sed 's/^\s\s//' \
| sed 's/OGRFeature(Streets):/ID = /' \
| sed 's/MULTILINESTRING/GEOM = MULTILINESTRING/' \
| awk -F"=" '{print $2}' \
| sed 's/^\s//' \
| sed 's/^$/#/' \
