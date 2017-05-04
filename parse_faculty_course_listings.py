import csv
import sys
import pprint
import operator

# Call this script with the csv file as the command line argument

outputfile = "faculty_listing.csv"


facultylist = dict()
allowableCourseTypes = ['Course','FY Seminar','Film Screening','Language','Performance','Seminar1','Studio Course','Workshop']



with open(sys.argv[1], 'rb') as csvfile:
	classreader = csv.DictReader(csvfile, dialect='excel')
	for row in classreader:
		
		bannerID = row['PRIMARY_INSTRUCTOR_ID']
		coursetitle = row['TITLE']
		crn = row['CRN']
		coursenumber = row['SUBJ'] + row['CRSE#'].zfill(3)
		type = row['DESC1']
		comment = row['COMMENT']
		email = row['PRIMARY_INSTRUCTOR_EMAIL']
		lastname = row['PRIMARY_INSTRUCTOR_LAST_NAME']
		firstname = row['PRIMARY_INSTRUCTOR_FIRST_NAME']
		crosslist_group = row['SSBXLST_XSLT_GROUP']
		
		# If info isn't present or not a course to survey, skip
		if firstname=="" or lastname=="" or email=="" or email=="@swarthmore.edu" or bannerID=="" or type not in allowableCourseTypes:
			continue


		# Build course dict
		course = {'crn':crn,'title':coursetitle, 'coursenumber':coursenumber, 'comment':comment}
		# Add crosslist info if this is a crosslisted course
		if crosslist_group != '':
			course['crosslistgroup'] = crosslist_group
		

		if bannerID in facultylist:
			# Faculty already has at least one course loaded
			
			# Check to make sure this course isn't already listed (if so, skip it)
			existingCourseNumbers = [item['coursenumber'] for item in facultylist[bannerID]['courses']]
			if coursenumber in existingCourseNumbers:
				continue
					

			# Check to see if this course is crosslisted with an existing course.  If so, merge them
			crosslistmatch = False	
			if crosslist_group != '':
				for existingCourse in facultylist[bannerID]['courses']:
					if 'crosslistgroup' in existingCourse and crosslist_group == existingCourse['crosslistgroup']:
						existingCourse['coursenumber'] = existingCourse['coursenumber'] + "/" + coursenumber
						crosslistmatch = True
						break;

			if crosslistmatch == False:	
				# A new course that doesn't match an existing crosslist group.  Add it			
				facultylist[bannerID]['courses'].append(course)
			
		else:
			# New faculty -- create an entry
			facultylist[bannerID] = {'lastname':lastname, 'firstname': firstname, 'email':email, 'bannerID':bannerID, 'courses':[course]}


#pp = pprint.PrettyPrinter(depth=6)
#pp.pprint(facultylist)

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
