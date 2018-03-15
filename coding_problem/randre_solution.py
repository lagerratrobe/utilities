#! /usr/local/bin/python

'''Re-write of Nick's code'''

from osgeo.ogr import *

class StateObj(object):
  def __init__(self, ident, state, coords):
    self.ident = ident
    self.state = state
    self.coords = coords


class PointObj(object):
  def __init__(self, ident, coords):
    self.ident = ident
    self.state = str
    self.coords = coords


#################################
def state_reader(state_file):
  states = []
  reader = open(state_file, 'r').readlines()
  for line in reader[1:]:
    line = line.strip()
    [ident, state, coords] = line.split("|")
    states.append(StateObj(ident, state, coords))
  return states

def point_reader(point_file):
  points = []
  reader = open(point_file, 'r').readlines()
  for line in reader[1:]:
    line = line.strip()
    [ident, coords] = line.split("|")
    points.append(PointObj(ident, coords))
  return points

def testPoints(points_list, states_list):
  new_points = []
  for point_obj in points_list:
    point_geom = CreateGeometryFromWkt(point_obj.coords)
    for state_obj in states_list:
      state_geom = CreateGeometryFromWkt(state_obj.coords)
      if point_geom.Within(state_geom):
        point_obj.state = state_obj.state
        new_points.append(point_obj)
  return new_points

def printPoints(points):
  for point_obj in points:
    pretty_line = "%s|%s|%s" % (point_obj.ident, point_obj.state, point_obj.coords)
    print pretty_line
####################################

def main():
  points = "zip.csv"
  states = "states.csv"

  # STORAGE FOR point AND state OBJECTS
  states_features = state_reader(states)
  points_features = point_reader(points)

  # SINCE EACH PointObj HAS A "state" ATTRIBUTE, PASS BOTH SETS OF OBJECTS INTO 
  # METHOD AND UPDATE PointObj IN PLACE
  new_points = testPoints(points_features, states_features)
  printPoints(new_points)

if __name__ == '__main__':
  main()


