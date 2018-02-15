# -*- coding: utf-8 -*-
'''
  For the data:
  - [x] Fix multi-tags to just one tag with all values (sfields).
  - [x] Shape address information into a subfield.
  - [x] Clean tags according to clean.py.
  - [x] Drop all "other keys" remaining.
  - [x] Convert xml data to json.
'''

import xml.etree.ElementTree as ET
import re, json
import sample, clean
from datetime import datetime

FILE = "area.osm"
lower = re.compile(r'^([a-z]|-|_)*$')
lower_colon = re.compile(r'^([a-z]|-|_)*:([a-z]|-|_)*$')

def shape_tag(tag,json,sfields):
  if tag.attrib['k'].startswith('addr:'):
    '''
      Shape address information into:
      {'address':{'street':value,'number':value,...,'city':value}}
    '''
    if 'address' not in json:
      json['address'] = {tag.attrib['k'].replace('addr:',''):tag.attrib['v']}
    else:
      json['address'][tag.attrib['k'].replace('addr:','')] = tag.attrib['v']
    
    return
  elif any(tag.attrib['k'].startswith(f+'_') for f in sfields):
    '''
      Concatenate multifields ('field'+'_'+'number') values with ';'
      into one field ('field' = 'value_1;value_2;...;value_n')
    '''
    for item in json:
      if item == tag.attrib['k'][:tag.attrib['k'].find('_')]:
        json[tag.attrib['k'][:tag.attrib['k'].find('_')]] += ';'+tag.attrib['v']
    
    return
  elif lower.match(tag.attrib['k']) or lower_colon.match(tag.attrib['k']):
    pass
  else:
    return
  
  json[tag.attrib['k']]=tag.attrib['v']

def insert_child(child,json,sfields):
  if child.tag == 'member':
    json['member'] = {'type':child.attrib['type']
                      ,'ref':int(child.attrib['ref'])
                      ,'role':child.attrib['role']
                     }
  elif child.tag == 'nd':
    if 'nd' not in json:
      json['nd'] = [int(child.attrib['ref'])]
    else:
      json['nd'].append(int(child.attrib['ref']))
  elif child.tag == 'tag':
    clean.fix_tag(child.attrib)
    shape_tag(child,json,sfields)   
  else:
    print('Child unexpected!\nChild: ',child.tag)

def xml2json(root):
  print('Transforming xml to json...')
  data=[]
  sfields = ['sport','building:levels','landuse','natural','leisure','surface','water']
  for elem in root:
    json = {'_id':int(elem.attrib['id'])
            ,'element':elem.tag
            ,'created':{'version':int(elem.attrib['version'])
                        ,'changeset':int(elem.attrib['changeset'])
                        ,'timestamp':datetime.strptime(elem.attrib['timestamp'],"%Y-%m-%dT%H:%M:%SZ")\
                                             .strftime("%Y-%m-%d %H:%M:%S")
                        ,'user':elem.attrib['user']
                        ,'uid':int(elem.attrib['uid'])
                       }
           }
    if elem.tag == 'node':
      json['pos'] = [float(elem.attrib['lat']),float(elem.attrib['lon'])]
    
    for child in elem:
      insert_child(child,json,sfields)
    
    data.append(json)
  
  return data

def write_json(filename,data):
  print('Writing json...')
  with open(filename, 'w',encoding='utf8') as f:
    for i in data:
      f.write(json.dumps(i, ensure_ascii=False)+'\n')

if __name__ == '__main__':
  root = sample.open_xml(FILE)
  tags = sample.count_elements(root)
  root,_ = sample.rm_unused_elements(root,tags)
  data = xml2json(root)
  write_json('area.json',data)
  print('Done!!!')
