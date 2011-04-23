# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponseRedirect

from models import *

def index(request):
	response = HttpResponse()
	response.write("Public and Private Reports")
	return response

def public(request, report_id):
	if report_id=='1':  # all addresses
		return all_addresses(request)
	if report_id=='2': # businesses
		return businesses(request)
 	else:
			response = HttpResponse()
			response.write("Public {0} not written yet".format(report_id))
			return response

def private(request, report_id):
	if report_id=='1': # Paid up members
		return members(request)
 	else:
			response = HttpResponse()
			response.write("Private {0} not written yet".format(report_id))
			return response

def businesses(request):
	output=''
	all = Business.objects.all()
	for b in all:
		output += b.name + '\n'
		output += "=" * len(b.name) + '\n'
		output += "Phone: " + b.phone + '\n'
		output += "Email: " + b.email + '\n'
		output += "Web: " + b.website + '\n'
		output += b.location.__unicode__() + '\n'
		for i in b.industries.all():
			output += i.description + '\n'
		if b.owner != None:
			output += b.owner.firstname + ' ' + b.owner.lastname + '\n'
		output += '\n'
	return pre_html(output)

def pre_html(output):
	response = HttpResponse()
	response.write("<pre>")
	response.write(output)
	response.write("</pre>")
	return response

def members(request):
	memberprop = Property.objects.filter(community__name='Harford Park').filter(household__isnull=False).filter(household__last_renewal__gte='2010-01-01')
	return address_out(memberprop)

def all_addresses(request):
	allprop=Property.objects.filter(community__name='Harford Park')
	return address_out(allprop)

def address_out(query):
	output=''
	pre = ''
	for p in query.order_by('street', 'house'):
		if pre!=p.street:
			output += '\n'
			output += p.street + '\n'
			output += "=" * len(p.street) + '\n'
			pre=p.street
		output += p.__unicode__() + '\n'
	return pre_html(output)

