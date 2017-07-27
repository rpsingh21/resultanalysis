from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from result.models import ContactUs,ReportBug,ReportError
from .serializer import (
	ContactUsSerializer,
	ReportBugSerializer,
	ReportErrorSerializer,
	)

class ContactUsCreateAPIView(CreateAPIView):
	queryset = ContactUs.objects.all()
	serializer_class = ContactUsSerializer

class ReportErrorCreateAPIView(CreateAPIView):
	queryset = ReportBug.objects.all()
	serializer_class = ReportBugSerializer

class ReportBugCreateAPIView(CreateAPIView):
	queryset = ReportError.objects.all()
	serializer_class = ReportErrorSerializer