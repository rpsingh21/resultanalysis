from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import (
	College,
	Branch,
	TotalMarks,
	Subject,
	Student,
	Marks,
	Course,
	ContactUs,
	ReportBug,
	ReportError,
	)
#Register your models here.
class MarksAdminModel(admin.ModelAdmin):
	list_display=['student','backStatus','subjectCode','internal','external']
	search_fields=['student__rollNo','student__name','subjectCode__subjectName','internal','external']

class TotalMarksAdminModel(admin.ModelAdmin):
	list_display=['student','semester','totalMarks','internal','external']
	search_fields=['student__rollNo','student__name','semester','totalMarks','internal','external']

class StudentAdminModel(admin.ModelAdmin):
	list_display=['rollNo','name','college','branchCode','yearOfJoining']
	search_fields=['rollNo','name','college__collegeName','branchCode__branchCode','yearOfJoining']

class ContactUsAdminModel(admin.ModelAdmin):
	list_display=['name','mobNo','email','seen','createdAt']
	search_fields=['name','mobNo','email','seen','createdAt']

class ReportErrorAdminModel(admin.ModelAdmin):
	list_display=['rollNo','resolved','createdAt']
	search_fields=['email','description','resolved','createdAt']

class ReportBugAdminModel(admin.ModelAdmin):
	list_display=['resolved','createdAt']
	search_fields=['resolved','createdAt']


admin.site.register(College)
admin.site.register(Branch)
admin.site.register(Student,StudentAdminModel)
admin.site.register(TotalMarks,TotalMarksAdminModel)
admin.site.register(Subject)
admin.site.register(Marks,MarksAdminModel)
admin.site.register(Course)
admin.site.register(ContactUs,ContactUsAdminModel)
admin.site.register(ReportError,ReportErrorAdminModel)
admin.site.register(ReportBug,ReportBugAdminModel)


