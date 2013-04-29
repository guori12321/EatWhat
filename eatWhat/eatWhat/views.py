from django.http import HttpResponse
import views

from django.http import Http404, HttpResponse
import datetime


def hello(request):
	return HttpResponse("EatWhat?")

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttoResponse(html)

def hours_ahead(request, offset):
	try:
	offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now()+datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s),it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)
