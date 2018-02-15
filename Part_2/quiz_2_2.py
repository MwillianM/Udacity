# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"

def open_zip(datafile):
	with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
		myzip.extractall()

def parse_file(datafile):
	# Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
	# Excel date to Python tuple of (year, month, day, hour, minute, second)
	workbook = xlrd.open_workbook(datafile)
	sheet = workbook.sheet_by_index(0)
	header = sheet.row_values(0)[1:-1]
	data = [["Station","Year","Month","Day","Hour","Max Load"]]
	
	for i in range(len(header)):
		col = sheet.col_values(i+1,start_rowx=1)
		maxpos = col.index(max(col))+1
		maxtime = sheet.cell_value(maxpos,0)
		y,m,d,h,_,_=xlrd.xldate_as_tuple(maxtime, 0)
		data.append([header[i],y,m,d,h,max(col)])
	
	return data

def save_file(data, filename):
	with open("2013_Max_Loads.csv","w",newline='') as f:
	#with open("2013_Max_Loads.csv","w") as f:
		writer = csv.writer(f,delimiter="|")
		for i in data:
			writer.writerow(i)

def test():
	open_zip(datafile)
	data = parse_file(datafile)
	save_file(data, outfile)
	
	number_of_rows = 0
	stations = []
	
	ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
						'Year': '2013',
						'Month': '6',
						'Day': '26',
						'Hour': '17'}}
	correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
						'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
	fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']
	
	with open(outfile) as of:
		csvfile = csv.DictReader(of, delimiter="|")
		for line in csvfile:
			station = line['Station']
			if station == 'FAR_WEST':
				for field in fields:
					# Check if 'Max Load' is within .1 of answer
					if field == 'Max Load':
						max_answer = round(float(ans[station][field]), 1)
						max_line = round(float(line[field]), 1)
						assert max_answer == max_line
					
					# Otherwise check for equality
					else:
						assert ans[station][field] == line[field]
			
			number_of_rows += 1
			stations.append(station)
		
		# Output should be 8 lines not including header
		assert number_of_rows == 8
		
		# Check Station Names
		assert set(stations) == set(correct_stations)


if __name__ == "__main__":
	test()
