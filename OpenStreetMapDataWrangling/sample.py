# -*- coding: utf-8 -*-
'''
  For the OpenStreetMap file:
  - [x] Open the chosen area file that you downloaded.
  - [x] Count first level elements that are in the xml.
  - [x] Find children and attributes for each tag and so on with children.
  - [x] Remove elements that just appears once.
  - [x] Create a sample file for each main element.
'''

import xml.etree.ElementTree as ET
from pprint import pprint

FILE = "area.osm"
K = 100 #1 of K sample proportion

def open_xml(file):
  print('Openning the file...')
  return ET.parse(FILE).getroot()

def count_elements(root):
  print('Counting first level tags...')
  tags = {}
  for elem in root:
    if elem.tag not in tags:
      tags[elem.tag] = 1
    else:
      tags[elem.tag] += 1
  
  return tags

def rm_unused_elements(root,tags):
  print('Removing unsed tags...')
  for tag in tags.copy():
    if tags[tag] == 1:
      del tags[tag]
      root.remove(root.find(tag))
  
  return root, tags

def genealogy(root,gen={}):
  for elem in root:
    if elem.tag not in gen:
      gen[elem.tag] = {'attributes': list(elem.attrib.keys())
                        ,'children':{}
                       }
    else:
      genealogy(elem,gen[elem.tag]['children'])
  
  return gen

def sample(root,tags,k):
  print('Creating samples...')
  for tag in tags:
    i = 0
    filename = tag+"_sample"+".osm" 
    with open(filename, "wb") as f:
      f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
      f.write(b"<osm>\n  ")
      for elem in root.findall(tag):
        if list(elem) and i%k==0:
          f.write(ET.tostring(elem, encoding="utf-8"))
        
        i += 1
      
      f.write(b"</osm>")
      print("Created "+filename+" with "+str(i//k)+" samples.")

if __name__ == "__main__":
  root = open_xml(FILE)
  tags = count_elements(root)
  print('First Level Elements:')
  pprint(tags)
  print('Children and Attributes:')
  pprint(genealogy(root))
  root,tags = rm_unused_elements(root,tags)
  sample(root,tags.keys(),K)
  print('Done!!!')
