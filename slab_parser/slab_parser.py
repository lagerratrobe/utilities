#! /usr/bin/python

import yaml

class SlabParser:
  
  def __init__(self, slab_yaml):
    # Clean Ruby types out of response
    if slab_yaml.startswith("--- !ruby/object"):
      eol_index = slab_yaml.find("\n")
      self.slab_yaml = slab_yaml[eol_index:]
    else:
      self.slab_yaml = slab_yaml

  def ParseYaml(self):
    '''Load yaml and create new dictionary of info needed to create GeoTiff'''
    parsed_results = yaml.load(self.slab_yaml, Loader=yaml.CLoader)
    image_data = {}
    image_data['pixel_size'] = parsed_results['resolution']
    image_data['ul_x'] = parsed_results['west'] - (image_data['pixel_size'] / 2)
    image_data['ul_y'] = parsed_results['north'] + (image_data['pixel_size'] / 2)
    image_data['y_span'] = len(parsed_results['values'])
    image_data['x_span'] = len((parsed_results['values'][0]))
    image_data['values'] = parsed_results['values']
    return image_data

