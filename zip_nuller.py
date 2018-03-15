#! /usr/local/bin/python

'''Quick ditty to remove leading zeros from all-numeric Postal Codes that are zero-padded'''

# SAMPLE INPUT '-852300120|3164670|00120|0' 3RD FIELD IS THE ONE TO EVALUATE


class ZipReader:

  def __init__(self, input_file):
    self.zip_dict = {}
    data = open(input_file, 'r').readlines()
    for line in data[1:]:
      line = line.strip()
      [zip_id, parent_id, name, map_code] = line.split("|")
      self.zip_dict[zip_id] = [parent_id, name, map_code]

  def NullZips(self):
    '''Cast the name to int. If it fails (because it's not convertible to int),
       leave the name as-is.'''
    for zip_id in self.zip_dict:
      name = self.zip_dict[zip_id][1]
      try:
        name = int(name)
      except ValueError:
        pass
      self.zip_dict[zip_id][1] = name
    return self.zip_dict

def PrintZips(new_zips):
  for zip_id in new_zips:
    [parent_id, name, map_code] = new_zips[zip_id]
    pretty_line = "%s|%s|%s|%s" % (zip_id, parent_id, name, map_code)
    print pretty_line

def main():
  zip_factory = ZipReader("ZipCode.csv")
  new_zips = zip_factory.NullZips()
  PrintZips(new_zips)
  

if __name__ == '__main__':
  main()



