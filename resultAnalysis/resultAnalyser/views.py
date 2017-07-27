from django.db.models import Avg, Max, Min
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from result.models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)
from .forms import CompareForm
# Create your views here.

def studentResulAnalysis(request,rollNo=None):
	if rollNo:
		student=Student.objects.filter(rollNo=rollNo)
		if student.exists():
			student = student.first()
			semester=Marks.objects.filter(student__rollNo=rollNo).aggregate(max=Max('subjectCode__semester'),min=Min('subjectCode__semester'))
			semesterList=[i for i in range(int(semester['min']),int(semester['max'])+1)]

			#CODE FOR SEM WISE RANKING
			collegeObject = student.college
			branchObject = student.branchCode
			yearOfJoining = student.yearOfJoining

			internalRanks = []
			externalRanks = []
			totalRanks = []
			for sem in semesterList:
				totalMarksObj = TotalMarks.objects.filter(student=student,semester=sem).first()
				internal = totalMarksObj.internal
				external = totalMarksObj.external
				total = totalMarksObj.totalMarks
				rankingInternal = TotalMarks.objects.filter(student__college=collegeObject,\
					student__branchCode=branchObject,student__yearOfJoining=yearOfJoining
				,semester=sem,internal__gt = internal).count() + 1
				rankingExternal = TotalMarks.objects.filter(semester=sem,student__college=collegeObject,\
					student__branchCode=branchObject,student__yearOfJoining=yearOfJoining,
				external__gt = external).count() + 1
				rankingTotal = TotalMarks.objects.filter(semester=sem,student__college=collegeObject,\
					student__branchCode=branchObject,student__yearOfJoining=yearOfJoining,
				totalMarks__gt = total).count() + 1

				internalRanks.append(rankingInternal)
				externalRanks.append(rankingExternal)
				totalRanks.append(rankingTotal)
				print("Sem ",sem)
				print("rankingInternal ",rankingInternal)
				print("rankingExternal ",rankingExternal)
				print("rankingTotal ",rankingTotal)
			
			content={
				'title':student.name+' RESULT ANALYSIS',
				'semester':semesterList,
				'student':student,
				'rollNo':rollNo,
				'graph':True,
				'internalRanks':internalRanks,
				'externalRanks':externalRanks,
				'totalRanks':totalRanks
			}
			#END
		else:
			content={
				'error':"Sorry this roll no. does not exists in our database",
				'graph':False
			}
	else:
		content = {
		'graph':False
		}
	return render(request,'chart/analysisChart.html',content)

def compareResult(request):
	form=CompareForm(request.POST or None)
	if  request.method == 'POST':
		if form.is_valid():
			baseStudent=form.cleaned_data.get('baseStudent')
			otherStudent=form.cleaned_data.get('otherStudent')
			baseTotalMarks=TotalMarks.objects.filter(student__rollNo=baseStudent)
			otherTotalMarks=TotalMarks.objects.filter(student__rollNo=otherStudent)
			semester=Marks.objects.filter(student__rollNo=baseStudent).aggregate(max=Max('subjectCode__semester'),min=Min('subjectCode__semester'))
			otherStudentSemester=Marks.objects.filter(student__rollNo=otherStudent).aggregate(max=Max('subjectCode__semester'),min=Min('subjectCode__semester'))
			print(otherStudentSemester)
			# semester['min'] = int(semester['min'])
			# semester['max'] = int(semester['max'])
			otherStudentSemester['min'] = int(otherStudentSemester['min'])
			otherStudentSemester['max'] = int(otherStudentSemester['max'])

			lowerRange = min(semester['min'],otherStudentSemester['min'])
			upperRange = max(semester['max'],otherStudentSemester['max'])
			semesterList=[i for i in range(lowerRange,upperRange+1)]
			# otherTotalMarks=otherTotalMarks.filter(semester__in=semesterList)

			baseMarks=baseTotalMarks.values_list('internal','external','totalMarks').order_by('semester')
			baseInternalList=[]
			baseExternalList=[]
			baseTotalList=[]
			if semester['min'] > 1:
				baseInternalList += [0]*(semester['min']-1)
				baseExternalList += [0]*(semester['min']-1)
				baseTotalList  += [0]*(semester['min']-1)


			for i in baseMarks:
				baseInternalList.append(i[0])
				baseExternalList.append(i[1])
				baseTotalList.append(i[2])

			otherMarks=otherTotalMarks.values_list('internal','external','totalMarks').order_by('semester')
			otherInternalList=[]
			otherExternalList=[]
			otherTotalList=[]
			if otherStudentSemester['min'] > 1:
				otherInternalList += [0]*(otherStudentSemester['min']-1)
				otherExternalList += [0]*(otherStudentSemester['min']-1)
				otherTotalList  += [0]*(otherStudentSemester['min']-1)
		#	print(otherInternalList)
			for i in otherMarks:
				otherInternalList.append(i[0])
				otherExternalList.append(i[1])
				otherTotalList.append(i[2])
		#	print(otherInternalList)
			content={
				'title':baseTotalMarks[0].student.name+' VS '+otherTotalMarks[0].student.name+' RESULT COMPARE ',
				'baseStudent':baseTotalMarks[0].student,
				'otherStudent':otherTotalMarks[0].student,
				'semesterList':semesterList,
				'baseInternalList':baseInternalList,
				'baseExternalList':baseExternalList,
				'baseTotalList':baseTotalList,
				'otherInternalList':otherInternalList,
				'otherExternalList':otherExternalList,
				'otherTotalList':otherTotalList,
			}
			return render(request,'chart/compareChart.html',content)

	content={
		'title':'STUDENTS RESULT COMPARE',
		'form':form,
	}
	return render(request,'compareForm.html',content)


