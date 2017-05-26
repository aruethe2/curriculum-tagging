# Parse csv files with course reserves and clean up entries
import sys
import csv
import re
import requests
import feedparser
import pprint
import xml.etree.ElementTree as ET
import os 
from operator import attrgetter

rootDir = sys.argv[1]
worldcatapikey = sys.argv[2]


startrow = 0
endrow = 0
started = False

worldcat_url = "http://www.worldcat.org/webservices/catalog/search/opensearch"
worldcat_read_search = "http://www.worldcat.org/webservices/catalog/content/"




for dirName, subdirList, fileList in os.walk(rootDir):

	print('Found directory: %s' % dirName)
	for fname in fileList:
	
		# Only check pdfs
		if os.path.splitext(fname)[1] != ".csv":
			continue
	

		with open(os.path.join(dirName, fname)) as f:
			for i, line in enumerate(f):
				if not started and "title" in line.lower():
					startrow = i
				if endrow==0 and "new books" in line.lower():
					endrow = i
	
	
		# Start CSV output
		with open('reserve-readings.csv', 'a+') as csvfile:
			readingWriter = csv.writer(csvfile)	
			

			# Open file, stripping off everything before title row
			with open(os.path.join(dirName, fname), 'rb') as csvfile:
				reserveReader = csv.reader(csvfile)
				for index, row in enumerate(reserveReader):
		
					# Skip extraneous data
					if index <= startrow:
						continue

					# Skip on other known invalid data
					# Check for the position of McCabe -- this tells us the last column
					lastcol = 0
					for j, item in enumerate(row):
						if "mccabe" in item.lower():
							lastcol = j
				
					# Skip if can't find McCabe text		
					if lastcol == 0:
						continue
			
					title=""
					location = ""	
					authors = []
					if lastcol == 2:
						title = row[0]

					if lastcol == 3:
						title = "%s %s" % (row[0], row[1])

			
					# Remove newlines
					title = re.sub(r"\n", " ", title)	
						
					print title
		
					# Look up title in WorldCat
				
					payload = {'format': 'atom', 'cformat': 'mla', 'count':'1', 'wskey':worldcatapikey,'q':title}
					r = requests.get(worldcat_url, params=payload)	
					d = feedparser.parse(r.text)
					#print r.url
					pp = pprint.PrettyPrinter(depth=6)
					pp.pprint(d)
					subjects=[]
			
					if 'entries' in d and len(d.entries)>0:
						id = re.sub(r"http:\/\/worldcat\.org\/oclc\/","",d.entries[0].id)
						authors = d.entries[0]['author']	
						title = d.entries[0].title.encode('utf-8')
						
						
						singlelookup = requests.get(worldcat_read_search + id, params={'wskey':worldcatapikey, 'recordSchema': 'info:srw/schema/1/dc'})	
			
						#print singlelookup.url
						#print singlelookup.text
						root = ET.fromstring(singlelookup.text.encode('utf-8'))

						subjects = map(attrgetter('text'), root.findall('{http://purl.org/dc/elements/1.1/}subject'))   
						if subjects:
							for s in subjects:
								print "\t"+s
								
						# Write CSV output
						print os.path.splitext(os.path.basename(fname))[0]
						[coursenumber, semester] = (os.path.splitext(os.path.basename(fname))[0]).split("-")
						# Course, semester, title, subjects		
						readingWriter.writerow([coursenumber.upper(), semester.upper(), title, authors.encode('utf-8'), id,"|".join(subjects).encode('utf-8')])
		
								
					else:
						print "No entries found"
					print "==================="		
		
		
					
		
		
		
		
	