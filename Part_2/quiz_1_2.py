#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format

"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"

def open_zip(datafile):
	with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
		myzip.extractall()

def parse_file(datafile):
	workbook = xlrd.open_workbook(datafile)
	sheet = workbook.sheet_by_index(0)
	sheet_data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
	coast_data = (sheet.col_values(1))
	coast_data.pop(0)
	maxvalue = max(coast_data)
	minvalue = min(coast_data)
	avgcoast = sum(coast_data)/float(len(coast_data))
	r = 1
	#should have used coast_data.index(max(coast_data))
	for value in coast_data:
		if value == maxvalue:
			maxtime = xlrd.xldate_as_tuple(sheet.cell_value(r, 0), 0)
		if value == minvalue:
			mintime = xlrd.xldate_as_tuple(sheet.cell_value(r, 0), 0)
		
		r += 1
	
	data = {
			'maxtime': maxtime,
			'maxvalue': maxvalue,
			'mintime': mintime,
			'minvalue': minvalue,
			'avgcoast': avgcoast
	}
	return data


def test():
	open_zip(datafile)
	data = parse_file(datafile)
	
	assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
	assert round(data['maxvalue'], 10) == round(18779.02551, 10)

test()
