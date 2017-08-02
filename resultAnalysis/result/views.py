import requests
from bs4 import BeautifulSoup

from django.db.models import Avg, Max, Min
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import (
	UrlForm,
	SessionForm,
	OrderForm,
	)

from .models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)


def contactUs(request):
	return render(request,'contact.html',{})

def reportError(request):
	return render(request,'reporterror.html',{})

def reportBug(request):
	return render(request,'reportbug.html',{})
	
def getNewResult(request):
	urlForm =UrlForm(request.POST or None)
	successText = ""
	errorMessage=""
	if request.method == "POST":
		if urlForm.is_valid():
			url=urlForm.cleaned_data.get('url')
			try:
				name = getResult(url)
				successText = name+" is succefully added"
			except Exception as ex:
				print (ex)
				errorMessage = "Unexpected Error Occured. Please submit your Roll number and URL in Report the Error page"
			# try:
			# 	getResult(url)
			# except:
			# 	raise Http404("not vaild rollno")
	content={
		'title':'NEW RESULT',
		'form':urlForm,
		'success':successText,
		'error':errorMessage
	}
	return render(request,'addNewResult.html',content)

def getSessionAndsemester(request):
	sessionForm = SessionForm(request.POST or None)
	if request.method == "POST":
		if sessionForm.is_valid():
			session=sessionForm.cleaned_data.get('yearOfJoining')
			print("------------------",session)
			semester=sessionForm.cleaned_data.get('semester')
			college=sessionForm.cleaned_data.get('college')
			branch=sessionForm.cleaned_data.get('branch')
			url_r="/results/%s/%s/%s/%s/"%(college,branch,session,semester)
			return HttpResponseRedirect(url_r)
			## SAVE SESSION AND SEMESTER IN USER SESSION FIELD THEN REDIRECT RESULT PAGE	
	content={
		'title':'HOME',
		'form':sessionForm,
	}
	return render(request,'home.html',content)

## GETING RESULT OF SEMESTER AND COLLEGE BASED
def showSemesterResult(request,college,branch,yearOfJoining,semester):
	collegeObjects=get_object_or_404(College, collegeName= college)
	branchObjects=get_object_or_404(Branch,branchName=branch)
	results=TotalMarks.objects.filter(student__college=collegeObjects,student__branchCode=branchObjects,\
		student__yearOfJoining=yearOfJoining,semester=semester).order_by('student__name')

	# GETTING ALL SUBJECT LIST FOR SUBJECT OPTIONS
	subjects=Marks.objects.filter(student=results[0].student, subjectCode__semester=semester)

	content={
		'title':'Result of Students',
		'results':results,
		'subjects':subjects,
	}
	return render(request,'result.html',content)

## VIEW FOR SUBJECT WISE MARKS 
def showSubjectMarks(request,college,branch,yearOfJoining,semester,subjectCode):
	collegeObjects=get_object_or_404(College, collegeName= college)
	branchObjects=get_object_or_404(Branch,branchName=branch)
	subjectObject=get_object_or_404(Subject,subjectCode=subjectCode,semester=semester,branchCode=branchObjects)
	results=Marks.objects.filter(student__college=collegeObjects,student__branchCode=branchObjects,\
		student__yearOfJoining=yearOfJoining,subjectCode=subjectObject).order_by('student__name')

	# GETTING ALL SUBJECT LIST FOR OPTIONS
	subjects=Marks.objects.filter(student=results[0].student, subjectCode__semester=semester)
	
	aggregations = results.filter(internal__gte = 0, external__gte=0,totalMarks__gte=0).aggregate(Avg('internal'),Max('internal'),Min('internal'),Avg('external'),Max('external'),Min('external'),Avg('totalMarks'),Max('totalMarks'),Min('totalMarks'))
	content={
		'title':'Result of Students',
		'results':results,
		'subjects':subjects,
		'subjectCode':subjectCode,
		'aggregations':aggregations,
	}
	return render(request,'result.html',content)

def studentSemesterResult(request,rollNo,semester):
	student =get_object_or_404(Student,rollNo=rollNo)
	subjectCodes=Subject.objects.filter(branchCode=student.branchCode,semester=semester)
	marks=Marks.objects.filter(student=student,subjectCode__in=subjectCodes)
	content={
		'student':student,
		'marks':marks,
	}
	return render(request,'semesterResult.html',content)


###  CODE FOR SCRAP RESULT 

def getResult(url):
	user_agent = {'User-agent': 'Mozilla/5.0'}
	req=requests.get(url,headers = user_agent)
	soup=BeautifulSoup(req.content,'html.parser')

	# FIND GENRAL DETAILS OF USER
	collegeCode=(((soup.find(id='lblInstitute').text).split('(')[1]).split(')')[0]).strip()
	collegeName=(soup.find(id='lblInstitute').text).strip()
	courseCode=((soup.find(id='lblCourse').text).split('(')[1]).split(')')[0]
	courseName=(soup.find(id='lblCourse').text).strip()
	branchCode=((soup.find(id='lblBranch').text).split('(')[1]).split(')')[0]
	barnchName=(soup.find(id='lblBranch').text).strip()
	#print(int(branchCode),barnchName)

	## NOW CHECKING UNIVERSAL DETAILS OF STUDENTS
	collegeObjects=College.objects.get_or_create(collegeCode=int(collegeCode),collegeName=collegeName)
	courseObjects=Course.objects.get_or_create(courseCode=int(courseCode),courseName=courseName)
	#print(courseObjects[0])
	branchObjects=Branch.objects.get_or_create(course=courseObjects[0],branchCode=int(branchCode),branchName=barnchName)

	rollNo=(soup.find(id='lblRollNo').text).strip()
	enrollmentNo=soup.find(id='lblEnrollmentNo').text.strip()
	name=soup.find(id='lblFullName').text.strip()
	fatherName=soup.find(id='lblFatherName').text.strip()
	gender=soup.find(id='lblGender').text.strip()
	image=soup.find(id='imgphoto')['src'].strip()
	yearOfJoining=2000+int(rollNo[0:2])

	## IF STUDENT IS LATERAL THEN 
	lateral=soup.find(id='ctl03_lblSem').text.strip()
	if lateral == '3,4':
		print("------------------- lateral ------------------------ ")
		yearOfJoining-=1

	studentObject=Student.objects.get_or_create(
		rollNo=rollNo,
		yearOfJoining=yearOfJoining,
		college=collegeObjects[0],
		branchCode=branchObjects[0],
		name=name,
		image=image,
		url=url,
		fatherName=fatherName,
		)
	if not gender == "":
		studentObject[0].gender=gender
	studentObject[0].enrollmentNo=enrollmentNo
	studentObject[0].save()

	# FIND ALL RESULT TABLE  ID 
	tables=soup.find_all('table')
	for table in tables:
		tableId=table.get('id')
		if tableId:

			# IF TABLE CONTAIN RESULT TABLE 
			if tableId.split('_')[-1:][0]=='grdViewSubjectMarksheet':

				# THEN FIND GENRAL DETAIL LIKE SEM AND TOTAL SUBJECT
				coreId=tableId.split('_')
				topId=coreId[0]+'_'+coreId[1]+'_'
				semester=(soup.find(id=topId+'lblSemesterId').text).strip()
				# print("semesterId = ",semester)
				if semester !='0':
					totalSubject=int((soup.find(id=topId+'lblTotalSubjectsCount').text).strip())
					totalMarks=(soup.find(id=topId+'lblSemesterTotalMarksObtained').text).strip()
					totalInternal=0
					totalExternal=0
					SemesterResultStatus = "PASS"

					# NOW GETTING SEMESTER SUBJECT MARKS 
					for i in range(0,totalSubject):
						subjectCode=(soup.find(id=tableId+'_subCode_'+str(i)).text).strip()
						subjectName=(soup.find(id=tableId+'_subName_'+str(i)).text).strip()
						subjectType=(soup.find(id=tableId+'_subType_'+str(i)).text).strip()

						## CREATE OR GET SUBJECT OBJECT
						subjectObject= Subject.objects.get_or_create(
							subjectCode = subjectCode,
							branchCode=branchObjects[0],
							)
						if subjectObject[1]:
							subjectObject[0].semester=semester
							subjectObject[0].subjectName=subjectName
							subjectObject[0].subjectType=subjectType
							subjectObject[0].save()

						# FIND MARKS 
						parentTd=(soup.find(id=tableId+'_subCode_'+str(i))).parent.parent
						allTd=parentTd.find_all('td')
						subjectInternal=allTd[3].text.strip()
						subjectExternal=allTd[4].text.strip()
						backMarks=allTd[5].text.strip()
						subjectCredit=allTd[6].text.strip()
						backStatus = False

						## IF SUBJECT MARKS AND BACK STATUS NOT ABLABE THEN 
						try:
							i=int(subjectInternal)
						except:
							subjectInternal='-1'

						try:
							i=int(subjectExternal)
						except:
							subjectExternal='-1'

						try:
							backMarks=backMarks.replace('*','')
							i=int(backMarks)
						except:
							backMarks='-1'

						try:
							if subjectCredit=='0' or subjectCredit == 'F':
								backStatus=True
								SemesterResultStatus = "COP"
						except:
							backStatus=False
							

						## SAVING SUBJECT STUDENTS MARKS 
						marksObject=Marks.objects.get_or_create(
							student=studentObject[0],
							subjectCode=subjectObject[0],
							)
						marksObject[0].internal=subjectInternal
						marksObject[0].external=subjectExternal
						if marksObject[0].backMarks<int(backMarks):
							marksObject[0].backMarks=backMarks
						else:
							backMarks=marksObject[0].backMarks
						marksObject[0].backStatus=backStatus
						print(subjectCode,subjectInternal,subjectExternal,backMarks)

						## GETTING TOTALINTERNAL AND EXTERNAL MARKS
						if backMarks=='-1':
							backMarks='0'
						if subjectInternal=='-1':
							subjectInternal='0'
						if subjectExternal=='-1':
							subjectExternal='0'

						# SAVE SUBJECT MARKS 
						marksObject[0].totalMarks=int(subjectInternal)+int(subjectExternal)
						marksObject[0].save()

						if subjectType !='CA':
							if subjectType =='Theory':
								totalInternal+=int(subjectInternal)
								totalExternal+=max(int(subjectExternal),int(backMarks))
							elif subjectType == 'Practical':
								totalInternal+=(max(int(subjectExternal),int(backMarks))+int(subjectInternal))
							elif subjectType == 'GP':
								totalInternal+=int(subjectInternal)


					# print(subjectCode,subjectName,subjectType,subjectInternal,subjectExternal)

					# SAVING AND UPDATING TOTAL MARKS OF RESULT 
					totalObjects,p=TotalMarks.objects.get_or_create(
						student=studentObject[0],
						semester=semester,
						)
					totalObjects.internal=totalInternal
					totalObjects.external=totalExternal
					totalObjects.totalMarks=totalInternal+totalExternal
					totalObjects.resultStatus=SemesterResultStatus
					totalObjects.save()
	return name	

## FOR REFRESHING RESULT

def refreshResult(results):
	urls=Student.objects.all()
	for url in urls:
		try:
			getResult(url.url)
		except:
			pass

def a():
	students = Student.objects.all()
	for student in students:
		backs = Marks.objects.filter(student=student,backStatus=True)
		for back in backs:
			newData = TotalMarks.objects.get(student=student,semester=back.subjectCode.semester)
			newData.resultStatus = "COP"
			print(student.name)
			newData.save()

def b():
	urls=TotalMarks.objects.filter(resultStatus="COP")
	name='1445'
	for url in urls:
		try:
			if name != url.student.name:
				name=url.student.name
				print(url.student.name)
				getResult(url.student.url)
		except Exception as ex:
			print(ex)
			pass

def c():
	students = Student.objects.filter(yearOfJoining='2016')
	for student in students:
		try:
			getResult(student.url)
		except Exception as ex:
			print(ex)
			pass


