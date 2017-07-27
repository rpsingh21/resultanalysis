from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from result.models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)
from .serializers import(
	StudentSerializers,
	)

#API FOR USER SEMESTER RESULT
class StudentSemesterResultAPIView(APIView):
	authentication_classes = []
	permission_classes = []
	def get(self,request,rollNo,semester):
		marks=Marks.objects.filter(student__rollNo=rollNo,subjectCode__semester=semester).values_list('subjectCode__subjectCode','internal','external','totalMarks').order_by('subjectCode__subjectCode')
		subjectList=[]
		internal=[]
		external=[]
		totalMarks=[]
		for i in marks:
			subjectList.append(i[0])
			if(i[1]==-1):
				internal.append('0')
			else:
				internal.append(i[1])
			if(i[2]==-1):
				external.append('0')
			else:
				external.append(i[2])
			if(i[3]==-1):
				totalMarks.append('0')
			else:
				totalMarks.append(i[3])
		data={
		'subjectList':subjectList,
		'internal':internal,
		'external':external,
		'totalMarks':totalMarks,
		}
		return Response(data)

# API FOR USER TOTAL RESULT VIEW
class StudentResultAPIView(APIView):
	authentication_classes=[]
	permission_classes=[]
	def get(self,request,rollNo):
		marks=TotalMarks.objects.filter(student__rollNo=rollNo).values_list('semester','internal','external','totalMarks').order_by('semester')
		subjectList=[]
		internal=[]
		external=[]
		totalMarks=[]
		for i in marks:
			subjectList.append('semester-'+str(i[0]))
			if(i[1]==-1):
				internal.append('0')
			else:
				internal.append(i[1])
			if(i[2]==-1):
				external.append('0')
			else:
				external.append(i[2])
			if(i[3]==-1):
				totalMarks.append('0')
			else:
				totalMarks.append(i[3])
		data={
		'subjectList':subjectList,
		'internal':internal,
		'external':external,
		'totalMarks':totalMarks,
		}
		return Response(data)
	
		