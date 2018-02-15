# -*- coding: utf-8 -*-
'''
  For the attributes of the tag elements:
  - [x] Change key 'endereço' to 'addr:street' and 'Futsal' to 'sport'.
  - [x] Change multi_colon to colon keys.
  - [x] Expand abbreviations on values.
  - [x] Show all changed tags.
'''

keys = {'endereço':'addr:street','Futsal':'sport'}
values = {'Cond.':'Condomínio '
          ,'Av.':'Avenida '
          ,'AV.':'Avenida '
          ,'Ed.':'Edifício '
          ,'ED.':'Edifício '
          ,'A.E.':'Área Especial '
          ,'Bl.':'Bloco '
          ,'BL.':'Bloco '
          ,'Qd.':'Quadra '
          ,'Q. ':'Quadra '
          ,'Conj.':'Conjunto '
          ,'Cj.':'Conjunto '
          ,'Ch.':'Chácara '
          ,'Lt.':'Lote '
         }

def fix_tag(attr):
  for k in keys:
    if k == attr['k']:
      attr['k'] = keys[k]
  
  for v in values:
    if v in attr['v']:
      attr['v'] = attr['v'].replace(v, values[v]).replace('  ',' ')
    
    if attr['k'].count(':') > 1:
      comma = attr['k'].find(':')+1 
      attr['k'] = attr['k'][:comma] + attr['k'][comma:].replace(':','_')
  
  return attr

if __name__ == '__main__':
  import xml.etree.ElementTree as ET
  for _,element in ET.iterparse('area.osm'):
    if element.tag == 'tag':
      tag2 = element.attrib.copy()
      fix_tag(element.attrib)
      if tag2 != element.attrib:
        print(element.attrib)
  
  print('Done!!!')
