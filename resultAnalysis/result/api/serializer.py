from rest_framework.serializers import ModelSerializer,ValidationError
from result.models import (
	ContactUs,
	ReportBug,
	ReportError,
	)

class ContactUsSerializer(ModelSerializer):
	class Meta:
		model = ContactUs
		fields = [
			'name',
			'mobNo',
			'email',
			'comment',
		]
	def validate_email(self, email):
		allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"]
		domain = email.split("@")[1]
		if domain not in allowedDomains:
			raise ValidationError('Invalid email address')
		return email

class ReportBugSerializer(ModelSerializer):
	class Meta:
		model = ReportBug
		fields = [
			'email',
			'description',
		]
	def validate_email(self, email):
		allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]
		domain = email.split("@")[1]
		if domain not in allowedDomains:
			raise ValidationError('Invalid email address')
		return email

class ReportErrorSerializer(ModelSerializer):
	class Meta:
		model = ReportError
		fields = [
			'rollNo',
			'url',
		]