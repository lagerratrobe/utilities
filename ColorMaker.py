#! /usr/bin/python

# ColorMaker.py

__author__ = '(Roger Andre)'

"""Class to calculate continuous color values.  Designed to be invoked from
within another program.  Use in the following manner:
  from ColorMaker import MakeColor
  new_color = MakeColor(5) --> where "5" is the z value to be interpolated
  RGB = new_color.GetValues() --> will return an array of [R,G,B] values.

Based on C++ utility written by Paul Surgeon, 
http://perrygeo.googlecode.com/svn/trunk/demtools/color-relief.cpp

To Do: Needs to take an external .lut file as input.  .lut needs to specify
foreground and background colors.  Currently hard-coded.
"""

import sys

class MakeColor:

  def __init__(self, z_val):
    if `z_val` == 'nan':
      self.z_val = `z_val`
    else:
      self.z_val = z_val
    self.color_dict = {
     # standard ramp
         3:[102,0,255],
       3.6:[20,82,255],
       4.2:[0,194,224],
       4.8:[0,255,122],
        5.4:[41,255,0],
         6:[204,255,0],
       6.6:[245,194,0],
       7.2:[224,118,0],
        7.8:[168,46,0],
         8.4:[105,0,0],
            9:[64,0,0]}

    self.elevs = self.color_dict.keys()
    self.elevs.sort() 
    if self.z_val in self.elevs:  # value is an exact match
      self.rgb = self.color_dict[self.z_val]
    elif self.z_val > self.elevs[-1]: # assign a foreground color to any values above highest z_value
      self.rgb = self.color_dict[self.elevs[-1]]
    elif self.z_val < self.elevs[0]: # assign a background color to any values below lowest z_value
      self.rgb = self.color_dict[self.elevs[0]]
    elif self.z_val == 'nan':
      self.rgb = self.color_dict[self.elevs[0]]
    else:
      self.FindElev(self.z_val, self.elevs)
      self.low = self.low_high[0]
      self.high = self.low_high[1]
      self.FindRGB(self.z_val, self.low, self.high, self.color_dict[self.low], self.color_dict[self.high])

  def FindElev(self, z_val, elevs):
    high = elevs[-1]
    low = elevs[-2]
    if low < z_val < high:
      self.low_high = [low, high]
      return self.low_high
    else:
      elevs.remove(high)
      self.FindElev(z_val, elevs)

  def FindRGB(self, z_val, low_elev, high_elev, low_rgb, high_rgb):
    diff_factor = ( float(z_val) - float(low_elev) ) / ( float(high_elev) - float(low_elev) )

    [red_low, green_low, blue_low] = low_rgb
    [red_high, green_high, blue_high] = high_rgb

    new_red = int( ((red_high - red_low) * diff_factor) + red_low )
    new_green = int( ((green_high - green_low) * diff_factor) + green_low )
    new_blue = int( ((blue_high - blue_low) * diff_factor) + blue_low )

    self.rgb = [new_red, new_green, new_blue]

  def GetValues(self):
    return self.rgb
    
#def main():
  #RGB = MakeColor(10)
  #print RGB.GetValues()

#if __name__ == '__main__':
  #main()

