#! /usr/bin/python

import unittest
from slab_parser import SlabParser

class TestSlabParser(unittest.TestCase):
  
  def test_ParseRealData(self):
    data = open("solar_1x1.yaml").read()
    results = SlabParser(data).ParseYaml()
    self.assertEqual(results['y_span'], 32)
    self.assertEqual(results['x_span'], 32)
    self.assertAlmostEqual(results['ul_x'], -118.53333, 4)
    self.assertAlmostEqual(results['ul_y'], 35.80, 4)
    self.assertAlmostEqual(results['pixel_size'], .03333, 4) 
    self.assertEqual(len(results['values']), 32)

#### End TestSlabParser ####

if __name__ == '__main__':
    unittest.main()

    

