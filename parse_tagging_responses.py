import csv
import sys
import pprint
import operator

# Call this script with the Qualtrics csv file as the command line argument

outputfile = "parsed_tag_responses.csv"


taglist = dict()


with open(sys.argv[1], 'rb') as csvfile:
	classreader = csv.DictReader(csvfile, dialect='excel')
	for row in classreader:
		
		taglist[row["COURSE1"]] = {"social_justice_tags":row["1_Tags"].split(",").lstrip(), "percent_social_justice_tags": row["1_Q6"], "other_tags": row["1_Q4"].split(",").lstrip()}



pp = pprint.PrettyPrinter(depth=6)
pp.pprint(taglist)

exit()

with open(outputfile, 'w') as csvfile:
	fieldnames = ['FirstName', 'LastName', 'Email', 'RecipientID', 'CRN1', 'COURSE1' ,'COMMENT1' ,'CRN2', 'COURSE2', 'COMMENT2', 'CRN3', 'COURSE3', 'COMMENT3','CRN4', 'COURSE4', 'COMMENT4','CRN5', 'COURSE5', 'COMMENT5']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	for f in facultylist:
			crn1 = crn2 = crn3 = crn4 = crn5 = course1 = course2 = course3 = course4 = course5 = comment1 = comment2 = comment3 = comment4 = comment5 = ""
				
			for i, c in enumerate(facultylist[f]['courses']):
				if i==0:
					crn1 = c['crn']
					course1 = c['coursenumber'] + ": " + c['title']
					comment1 = c['comment']
				elif i==1:
					crn2 = c['crn']
					course2 = c['coursenumber'] + ": " + c['title']
					comment2 = c['comment']
				elif i==2:	
					crn3 = c['crn']
					course3 = c['coursenumber'] + ": " + c['title']
					comment3 = c['comment']
				elif i==3:	
					crn4 = c['crn']
					course4 = c['coursenumber'] + ": " + c['title']
					comment4 = c['comment']				
				elif i==4:	
					crn5 = c['crn']
					course5 = c['coursenumber'] + ": " + c['title']
					comment5 = c['comment']	
				else:
					# future expansion!
					print "** Too many courses! **"
					print facultylist[f]

			writer.writerow({'FirstName': facultylist[f]['firstname'], 'LastName': facultylist[f]['lastname'], 'Email': facultylist[f]['email'], 'RecipientID': facultylist[f]['bannerID'], 'CRN1': crn1, 'COURSE1':course1, 'COMMENT1':comment1, 'CRN2': crn2, 'COURSE2':course2, 'COMMENT2':comment2, 'CRN3': crn3, 'COURSE3':course3, 'COMMENT3':comment3, 'CRN4': crn4, 'COURSE4':course4, 'COMMENT4':comment4,'CRN5': crn5, 'COURSE5':course5, 'COMMENT5':comment5});
