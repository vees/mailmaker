# Create your views here.

import json
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponseRedirect
import csv

from models import *

def index(request):
	response = HttpResponse()
	response.write("Harford Park Neighborhood Data API")
	return response

def _generate_local():
	import csv
	import codecs
	sourcefile = '/home/harfordpark/harfordpark.com/harfordpark/codecomplaincsv130826.csv'
	with codecs.open(sourcefile, 'rb', 'utf-8-sig') as f:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		headers = reader.next()
		print headers
		complained = {}
		for x in reader:
			complained[x[0]] = x

	mystreets = [x.house + " " + x.street.upper() for x in Property.objects.filter(community__name='Harford Park')]
	
	both = dict([(x,complained[x][1:]) for x in list(set(mystreets) & set(complained.keys()))])

	output = { 'Source': sourcefile, 'Harford Park': mystreets, "Complaints": complained, "Local": both }
	#output = { 'Source': sourcefile, "Complaints": both }
	return output

def complaints_csv(request):
	output = ""
	complaints = _generate_local()
	for key in complaints["Local"]:
		address = key
		cdata = complaints["Local"][key]
		if cdata[5] != "Closed":
			output += "%s:\nCase %s (%s)\nOpened %s - Status: %s\n\n" % (address, cdata[0], cdata[1], cdata[2], cdata[5])
	return HttpResponse(output, content_type='text/ascii')

def complaints(request):
	output = _generate_local()
	callback = request.GET.get('callback')
	json_output=json.dumps( output, sort_keys=True, indent=4)
 	if callback:
		json_output = '%s(%s)' % (callback, json_output)
	return HttpResponse(json_output, content_type='application/json')

def properties(request):
	mystreets = [x.house + " " + x.street.upper() for x in Property.objects.filter(community__name='Harford Park').order_by('street','house')]
	callback = request.GET.get('callback')
	output = { 'Harford Park': mystreets }
	json_output=json.dumps( output, sort_keys=True, indent=4)
 	if callback:
		json_output = '%s(%s)' % (callback, json_output)
	return HttpResponse(json_output, content_type='application/json')


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
		output += p.shortlink() + '\n'
	return pre_html(output)

