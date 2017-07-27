from rest_framework.serializers import ModelSerializer,ValidationError

from result.models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)

class StudentSerializers(ModelSerializer):
	class Meta:
		model=Marks
		fields='__all__'