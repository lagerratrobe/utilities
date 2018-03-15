"""
WKT ?PointInPolygon? script for Tableau

"""
import csv
from osgeo.ogr import *

workDir ="C:\\Users\\Owninator\\Documents\\TABLEAU APP WORK\\python_exercise\\"
points="zip.csv"
states="states.csv"

pointsDict={}
statesDict={}

class StateObj(object):
	"""holds well-known text definition of states, takes (id number, state label, wkt of multipoint polygon)"""
	def __init__(self, ident, state, coords):
		super(StateObj, self).__init__()
		self.ident = ident
		self.state = state
		self.coords = coords

		
class PointObj(object):
	"""holds well-known text definition of point, takes (id number, wkt of point), inits with empty slot for state label"""
	def __init__(self, ident, coords):
		super(PointObj, self).__init__()
		self.ident = ident
		self.state = str
		self.coords = coords

#----------------------------------------------------------------------

#File Readers & Writers 
def state_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter='|') #for seperator specificity, after file_obj add in : , delimiter=','
    for line in reader:
        statesDict[line["state"]] = StateObj(line["id"], line["state"], line["geometry"])


def point_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter='|') #for seperator specificity, after file_obj add in : , delimiter=','
    for line in reader:
        pointsDict["point"+line["id"]] = PointObj(line["id"], line["geometry"])

def csv_writer(data, path):
    """
    Write pointsDict to CSV in id|state|geometry format
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        for point in pointsDict:
            ident = point.ident
            state = point.states
            coords = point.coords
            row = str(ident)+"|"+str(state)+"|"+str(coords)
            writer.writerow(row)
    csv_file.close() 

#----------------------------------------------------------------------

print "Reading in .csv files"
with open(workDir+states) as file:
        state_reader(file)
        file.close()
        print "States complete"

with open(workDir+points) as file:
        point_reader(file)
        file.close()
        print "Points complete"


for item in pointsDict:
#testPoint = pointsDict["point1"].coords
	testPoint = pointsDict[item].coords
	runCount=0
	runlimit = len(statesDict)
	for statePoly in statesDict:
		print statesDict[statePoly].state
		testPoly = statesDict[statePoly].coords
		#print testPoly.
		#print testPoint
		thing1 =CreateGeometryFromWkt(testPoint)
		#print thing1
		thing2=CreateGeometryFromWkt(testPoly)
		#print thing2
		
		check = thing1.Within(thing2)
		print check
		if check == True:
			pointsDict[item].state = statesDict[statePoly].state
			print "Changed to"+pointsDict[item].state
			
		else:
			if runlimit >= runCount:
				pointsDict[item].state = "NA" 
			else:
				runCount +=1
				continue





#csv_writer(pointsDict, pointsCompared.csv)
for item in pointsDict:
	print pointsDict[item].state
print "Processing complete"