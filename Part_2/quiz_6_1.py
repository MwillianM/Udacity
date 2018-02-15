#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
ok	- NoneType if the value is a string "NULL" or an empty string ""
ok	- list, if the value starts with "{"
ok	- int, if the value can be cast to int
ok	- float, if the value can be cast to float, but CANNOT be cast to int.
	 For example, '3.23e+07' should be considered a float because it can be cast
	 as float but int('3.23e+07') will throw a ValueError
ok	- 'str', for all other values
ok
The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
	....
}
ok
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.
ok
Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note(not?) be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
					"isPartOf_label", "areaCode", "populationTotal", "elevation",
					"maximumElevation", "minimumElevation", "populationDensity",
					"wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_datatype(data):
	if data == "NULL" or data == "":
		return type(None)
	elif data.startswith('{'):
		return type(list())
	elif data[:1] in '0123456789':
		try:
			return type(int(data))
		except:
			return type(float())
	else:
		return type(str())
	

def audit_file(filename, fields):
		fieldtypes = {}
		for field in fields:
				fieldtypes[field] = []
		
		with open(filename) as f:
				reader = csv.DictReader(f)
				for row in reader:
						for field in fields:
								if 'dbpedia.org' in row['URI']:
										fieldtypes[field].append(audit_datatype(row[field]))
		
		for field in fields:
				fieldtypes[field] = set(fieldtypes[field])
						
		return fieldtypes

def test():
		fieldtypes = audit_file(CITIES, FIELDS)

		pprint.pprint(fieldtypes)

		assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
		assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
		
if __name__ == "__main__":
		test()
