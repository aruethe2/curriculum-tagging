import csv
import sys
import pprint
import operator
import string
import json

# Call this script with the Qualtrics csv file as the command line argument

outputfile = "parsed_tag_responses.json"


taglist = []


with open(sys.argv[1], 'rb') as csvfile:
	classreader = csv.DictReader(csvfile, dialect='excel')
	for index, row in enumerate(classreader):
		
		# Skip first two extra rows
		if index<2:
			continue		
		
		
		

		for coursenum in range(1, 4):
		
			# If no course, skip
			if row["COURSE" + str(coursenum)] == "":
				continue
		
			# Get all social justice tags
			socialjusticetags = [];
			
			# Fix tags with commas in them
			tags = string.replace(row[str(coursenum) + "_Tags"], "identity (e.g. race, ethnicity, gender, class, differently-abled, sexual orientation)", "identity")
			
			
			for i in tags.split(","):
				j = i.lstrip()
				socialjusticetags.append(j)

			othertags = [];
			for i in row[str(coursenum) + "_Q4"].split(","):
				j = i.lstrip()
				if j != '':
					othertags.append(j)
				
				
			# Calculate course number and title from combined field
			coursedetails = row["COURSE" + str(coursenum)].split(": ",1)	
				
			taglist.append( {"coursenumber":coursedetails[0], "coursetitle":coursedetails[1], "social_justice_tags":socialjusticetags, "percent_social_justice_tags": row[str(coursenum) + "_Q6"], "other_tags": othertags})

pp = pprint.PrettyPrinter(depth=6)
pp.pprint(taglist)




# List of other tags
othertaglist = []
for c in taglist:
	othertags
	othertaglist += c['other_tags']
print othertaglist

with open(outputfile, 'w') as outfile:
    json.dump(taglist, outfile)


exit()
