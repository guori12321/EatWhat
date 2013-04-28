from django.http import HttpResponse
import datetime

def hello(request):
	return HttpResponse("EatWhat?")

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttoResponse(html)

