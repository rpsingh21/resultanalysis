from django import template

register = template.Library()

@register.filter(name="NA")
def nA(value):
	if value==-1:
		return "N/A"
	else:
		return value