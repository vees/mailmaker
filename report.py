import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

def print_addr(p):
	print "{0} {1}".format(p.firstname, p.lastname)
	print p.household.property.address()
	print "{0}, {1} {2}".format(p.household.property.city,
		p.household.property.county.state,
		p.household.property.zip)
	print

def print_hh(hh):
	print "{0} Household".format(hh.name)
	print hh.property.address()
	print "{0}, {1} {2}".format(hh.property.city,
		hh.property.county.state,
		hh.property.zip)
	print

#news=Person.objects.filter(interests__description='Newsletter')
#for p in news:
#	if p.household != None:
#		print_addr(p)

print "Newsletter mailings to members with no email"
print "============================================"

news=Person.objects.filter(interests__description='Newsletter').filter(email='')
hhset = set([p.household for p in news])
for hh in hhset:
	if (hh != None):
		print_hh(hh)

print
print "Newsletter mailings to members with email"
print "============================================"

news=Person.objects.filter(interests__description='Newsletter').exclude(email='')
hhset = set([(p.firstname,p.lastname,p.email) for p in news])
for hh in hhset:
	if (hh != None):
		print "{0} {1} {2}".format(hh[0],hh[1],hh[2])
print

