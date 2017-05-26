# Convert the PDF with course reserves data to csv data

import os
import sys
import re
import pdftables_api
 
# Get the root dir from the command line
rootDir = sys.argv[1]
pdftables_apikey = sys.argv[2]

print rootDir

for dirName, subdirList, fileList in os.walk(rootDir):

	print('Found directory: %s' % dirName)
	for fname in fileList:
	
		# Only check pdfs
		if os.path.splitext(fname)[1] != ".pdf":
			continue
	
		subj =  os.path.basename(dirName);
	
		# Filename format should be SSSS-NNN-TTT.pdf
		# where SSSS is a 4 character subject
		# NNN is the course number (variable digits, starts with a number but can end in a string)
		# TTT is a 3 character term code (e.g. F17)
		coursearray = os.path.splitext(fname)[0].split("-")
	
		# If not enough elements in split filename -- skip
		if len(coursearray) < 3:
			continue
	
		subject = coursearray[0]
	
		# Make sure coursenumber has the right number of digits 
		splitcoursenumber = re.split("(\D)", coursearray[1],1)
		if splitcoursenumber[0] == "":
			continue
		coursenumber = splitcoursenumber[0].zfill(3)
	
		if len(splitcoursenumber) >1:
			coursenumber += splitcoursenumber[1]
	
		# semester code
		semester = coursearray[2]
    	

		print('\t%s %s%s-%s' % (fname, subj, coursenumber, semester))

		# Convert PDF course reserve data to CSV 
		coursecode = "%s%s-%s" % (subject, coursenumber, semester)
		
		c = pdftables_api.Client(pdftables_apikey)
		c.csv(os.path.join(dirName,fname), '%s.csv' % coursecode)	

