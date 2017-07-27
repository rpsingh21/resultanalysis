from django.db import models
from django.urls import reverse

# MODEL FOR COLLEGE AND COLLEGE CODE
class College(models.Model):
	collegeCode=models.PositiveSmallIntegerField(unique=True)
	collegeName=models.CharField(max_length=256)

	def __str__(self):
		return self.collegeName

	def __unicode__(self):
		return self.collegeName

# MODEL FOR  COURCE 
class Course(models.Model):
	courseCode=models.PositiveSmallIntegerField()
	courseName=models.CharField(max_length=100)
	noOfSemester=models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.courseName

	def __unicode__(self):
		return self.courseName

# MODEL FOR BRANCH AND BRANCHCODE
class Branch(models.Model):
	course=models.ForeignKey(Course)
	branchCode=models.PositiveSmallIntegerField(unique=True)
	branchName=models.CharField(max_length=100)

	def __str__(self):
		return self.branchName

	def __unicode__(self):
		return self.branchName


# MODEL FOR STUDENTS DETAILS
class Student(models.Model):
	rollNo=models.CharField(max_length=20,unique=True)
	yearOfJoining=models.PositiveSmallIntegerField()
	college=models.ForeignKey(College)
	branchCode=models.ForeignKey(Branch)
	name=models.CharField(max_length=100,)
	image=models.TextField()
	url=models.URLField(max_length=512)
	fatherName=models.CharField(max_length=100)
	enrollmentNo=models.CharField(max_length=20,null=True)	
	gender=models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.rollNo

	def __unicode__(self):
		return self.rollNo



# MODEL FOR TOTAL MARKS AND INTERNAL AND EXTERNAL
class TotalMarks(models.Model):
	student=models.ForeignKey(Student)
	semester=models.PositiveSmallIntegerField(null=True)
	totalMarks=models.IntegerField(null=True)
	internal=models.IntegerField(null=True)
	external=models.IntegerField(null=True)
	resultStatus = models.CharField(max_length=250,null=True)
	def __str__(self):
		return self.student.rollNo

	def __unicode__(self):
		return self.student.rollNo

	# ABS URL FOR SEMESTER RESULT
	def get_urlSemester(self):
		return reverse('result:studentSemesterResult',kwargs={'rollNo':self.student,'semester':self.semester})

	class Meta:
		verbose_name_plural = "TotalMarks"


# MODEL FOR SUBJECT AND SUBJECT CODE  
class Subject(models.Model):
	branchCode=models.ForeignKey(Branch)
	subjectCode=models.CharField(max_length=20)
	subjectName=models.CharField(max_length=100,null=True)
	subjectType=models.CharField(max_length=100,null=True)
	semester=models.PositiveSmallIntegerField(null=True)
	subjectMaxIntenal=models.PositiveSmallIntegerField(null=True,blank=True)
	subjectMaxExtenal=models.PositiveSmallIntegerField(null=True,blank=True)

	def __str__(self):
		return self.subjectCode

	def __unicode__(self):
		return self.subjectCode

#MODEL FROM DIFFRENTS SUBJECTS MARKS 
class Marks(models.Model):
	student=models.ForeignKey(Student)
	subjectCode=models.ForeignKey(Subject)
	internal=models.IntegerField(null=True)
	external=models.IntegerField(null=True)
	totalMarks=models.IntegerField(null=True)
	backMarks=models.IntegerField(default=-1)
	backStatus=models.NullBooleanField()

	def __str__(self):
		return self.student.rollNo

	def __unicode__(self):
		return self.student.rollNo

	def get_urlSemester(self):
		return reverse('result:studentSemesterResult',kwargs={'rollNo':self.student,'semester':self.subjectCode.semester})

	class Meta:
		verbose_name_plural = "Marks"

class ContactUs(models.Model):
	name = models.CharField(max_length=120,blank=True)
	mobNo = models.CharField(max_length=12,blank=True)
	email = models.EmailField()
	comment = models.TextField()
	seen = models.BooleanField(default=False)
	createdAt = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-createdAt']

	def __str__(self):
		return self.email

class ReportBug(models.Model):
	email = models.EmailField()
	description = models.TextField()
	resolved = models.BooleanField(default=False)
	createdAt = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-createdAt']

	def __str__(self):
		return self.email

class ReportError(models.Model):
	rollNo = models.CharField(max_length=20)
	url = models.URLField()
	resolved = models.BooleanField(default=False)
	createdAt = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-createdAt']

	def __str__(self):
		return self.rollNo
		