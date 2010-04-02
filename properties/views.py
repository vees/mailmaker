# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from models import Street, Property, Listing, ListingWebPage

def list(request):
	out = "<pre>"
	s=Street.objects.all().order_by('name')
	for st in s:
		out += st.name + "\n"
		p = Property.objects.filter(street=st)
		for pp in p:
			out += "  " + pp.__unicode__() + "\n"
			l = Listing.objects.filter(property=pp)
			for ll in l:
				ws = ListingWebPage.objects.filter(listing=ll)
				for ww in ws:
					out += "    " + ww.url + "\n"
	out += "</pre>"
	return HttpResponse(out)
