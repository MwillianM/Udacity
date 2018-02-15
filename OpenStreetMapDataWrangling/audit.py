# -*- coding: utf-8 -*-
'''
  For the main elements:
  - [x] Test the types of attributes according to the data_types.
  - [x] Find special chars on string attributes.
  - [x] Count the type of key values from tag elements.
  - [x] Show "other" key values (for the cleaning process).
'''

import xml.etree.cElementTree as ET
import re
from pprint import pprint
from datetime import datetime

FILE = "area.osm"
data_types={'int':['id','version','changeset','uid','ref']
             ,'float':['lat','lon']
             ,'timestamp':['timestamp']
             ,'string':['type','role','k']
             ,'unaudited':['user','v']
            }
schars = '!"#$%&\'()*+,./;<=>?@[\\]^`{|}~ç\t\r\n'

lower = re.compile(r'^([a-z]|-|_)*$')
lower_colon = re.compile(r'^([a-z]|-|_)*:([a-z]|-|_)*$')

def audit_attribs(attribs,types,schars):
  for attrib in attribs:
    try:
      if attrib in types['int']:
        int(attribs[attrib])
      elif attrib in types['float']:
        float(attribs[attrib])
      elif attrib in types['timestamp']:
        datetime.strptime(attribs[attrib],"%Y-%m-%dT%H:%M:%SZ")
      elif attrib in types['string']:
        for c in schars:
          if c in attribs[attrib]:
            print('Special char',c, 'found in : ',attribs[attrib])
      elif attrib in types['unaudited']:
        continue
      else:
        print('Attribute type not covered!\nAttr: '+attrib)
    except:
        print("Can't convert the value: ", attribs[attrib],'\nAttrib: ',attrib)

def audit_keys(k_value,keys):
  if lower.match(k_value):
    keys['lower'] += 1
  elif lower_colon.match(k_value):
    keys['lower_colon'] += 1
  elif k_value.count(':') > 1:
    keys['lower_multi_colon'] += 1
  else:
    keys['other'][0] += 1
    keys['other'][1].add(k_value)
  
  return keys

def audit(filename,types,schars):
  print("Auditing...")
  keys = {"lower": 0
          ,"lower_multi_colon": 0
          ,"lower_colon": 0
          ,"other": [0,set([])]
         }
  for _,element in ET.iterparse(filename):
    if element.tag not in ('osm','note','meta','bounds'):
      audit_attribs(element.attrib,types,schars)
    
    if element.tag == 'tag':
      keys=audit_keys(element.attrib['k'],keys)
  
  return keys

if __name__ == "__main__":
  keys = audit(FILE,data_types,schars)
  pprint(keys)
  print('Done!!!')
