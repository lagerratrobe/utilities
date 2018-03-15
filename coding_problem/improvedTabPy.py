#! /usr/bin/python

"""
WKT ?PointInPolygon? script for Tableau

"""
import os
import csv
from osgeo.ogr import *



#--------------------------------------------------------------------------

#Input Data Vars & Working Data Dictionaries
workDir = "./"
inPointsCSV= "zip.csv"
inStatesCSV= "states.csv"
outFile = "someFile.csv"


pointsDict={}
statesDict={}

#----------------------------------------------------------------------

# WKT Storage Objects (see Working Data Dictionaries)

class StateObj(object):
	"""holds well-known text definition of states, takes (id number, state label, wkt of multipoint polygon)"""
	def __init__(self, ident, state, coords):
		super(StateObj, self).__init__()
		self.ident = ident
		self.state = state
		self.coords = coords

		
class PointObj(object):
	"""holds well-known text definition of point, takes (id number, wkt of point), inits with default for state label"""
	def __init__(self, ident, coords):
		super(PointObj, self).__init__()
		self.ident = ident
		self.state = "..."
		self.coords = coords

#----------------------------------------------------------------------

#File Readers & Writers 
def state_reader(file_obj):
	'''takes in a csv with header id|state|geometry, state as 2-letter abrev. and geom as WKT'''
	reader = csv.DictReader(file_obj, delimiter='|')
	for line in reader:
		''' TRYING TO ADD GEOM CHECKER 
		if len(line["state"])==2:
			testObj = CreateGeometryFromWkt(line["geometry"])
			attempt = testObj.GetGeometryName()
			if attempt['geography'] == "MULTIPOLYGON":
				continue
		else:
			print "Unexpected format ", line
		'''
		statesDict[line["state"]] = StateObj(line["id"], line["state"], line["geometry"])


def point_reader(file_obj):
	'''takes in a csv with header id|geometry, geom as WKT'''
	reader = csv.DictReader(file_obj, delimiter='|')
	for line in reader:
		'''testObj = CreateGeometryFromWkt(line["geometry"])
		if testObj.GetGeometryName() == "POINT":
			continue
		else:
			print "Unexpected format ", line'''
		pointsDict["point"+line["id"]] = PointObj(line["id"], line["geometry"])

def take_file_inputs(inPointsCSV,inStatesCSV):
		
#check file type: https://docs.python.org/2/library/mimetypes.html
		print "Ingesting CSV files"
		
		with open(workDir+inStatesCSV) as file:
			state_reader(file)
			file.close()
		print "States complete"

		with open(workDir+inPointsCSV) as file:
			point_reader(file)
			file.close()
		print "Points complete"

def points_writer(pointsDict, path):
	"""
	Write pointsDict to CSV in id|state|geometry format, state as 2-letter abrev. and geom as WKT
	"""
	with open(path, 'w') as csvfile:
		fieldnames = ['id', 'state', 'geometry']
		
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

		writer.writeheader()
		for point in pointsDict:
   			writer.writerow({fieldnames[0]: pointsDict[point].ident, fieldnames[1]: pointsDict[point].state, fieldnames[2]:pointsDict[point].coords})


#----------------------------------------------------------------------

#Analysis
def pointInPolyTest(pointsDict, statesDict):
	for item in pointsDict:
		testPoint = pointsDict[item].coords
		
		for statePoly in statesDict:
			testPoly = statesDict[statePoly].coords
			thing1 =CreateGeometryFromWkt(testPoint)
			thing2=CreateGeometryFromWkt(testPoly)
			#check = thing1.Within(thing2)
			check = thing1.Intersects(thing2)

			if check == True:
				pointsDict[item].state = statesDict[statePoly].state
				print "Point changed to "+pointsDict[item].state

		if pointsDict[item].state=="...":
			pointsDict[item].state = "NA"
			print "Point out of area"
#----------------------------------------------------------------------
'''
# Master Input Method
def autoPointInPolyMethod(workingDirectory,pointInputCSV,polygonInputCSV,pointOutCSV): 
	workDir = str(workingDirectory.encode('ascii','ignore').decode('utf8'))
	print type(workDir)
	inPointsCSV = str(pointInputCSV.encode('ascii','ignore').decode('utf8'))
	print type(inPointsCSV)
	inStatesCSV = str(polygonInputCSV.encode('ascii','ignore').decode('utf8'))
	outFile = str(pointOutCSV.encode('ascii','ignore').decode('utf8'))

autoPointInPolyMethod(wD,iPC,iSC,oFile)
File error 
	Traceback (most recent call last):
  File "improvedTabPy.py", line 140, in <module>
    take_file_inputs(inPointsCSV,inStatesCSV)
  File "improvedTabPy.py", line 71, in take_file_inputs
    os.chdir(workDir)
WindowsError: [Error 123] The filename, directory name, or volume label syntax i
s incorrect: '''


#=======================================================
"""
Processing/Workflow below
"""



take_file_inputs(inPointsCSV,inStatesCSV)

pointInPolyTest(pointsDict, statesDict)

points_writer(pointsDict, outFile)

print "Processing complete"
