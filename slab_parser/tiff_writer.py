#! /usr/bin/python

from osgeo import gdal
import numpy

class TiffWriter:

  def __init__(self, image_data):
    self.ul_x = image_data['ul_x']
    self.ul_y = image_data['ul_y']
    self.x_span = image_data['x_span']
    self.y_span = image_data['y_span']
    self.pixel_size = image_data['pixel_size']
    self.values = image_data['values']

  def WriteTiff(self, image_name):
    out_drv = gdal.GetDriverByName('GTiff')
    out_ds = out_drv.Create(image_name, self.x_span, self.y_span, 1, gdal.GDT_Float32)
    out_ds.SetGeoTransform([self.ul_x, self.pixel_size, 0, self.ul_y, 0, -(self.pixel_size)])
    out_band = numpy.zeros([out_ds.RasterYSize, out_ds.RasterXSize])
    for iY in range(out_ds.RasterYSize):
      for iX in range(out_ds.RasterXSize):
        pixel = self.values[iY][iX]
        out_band[abs(iY - self.y_span) - 1][iX] = pixel
    out_ds.GetRasterBand(1).WriteArray(out_band)
    out_ds = None

