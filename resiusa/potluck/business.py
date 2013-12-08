import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

output=''
all = Business.objects.all()
for b in all:
	output += b.name + '\n'
	output += "=" * len(b.name) + '\n'
	output += b.phone + '\n'
	output += b.email + '\n'
	output += b.website + '\n'
	output += b.location.__unicode__() + '\n'
	for i in b.industries.all():
		output += i.description + '\n'
	if b.owner != None:
		output += b.owner.firstname + ' ' + b.owner.lastname + '\n'
	output += '\n'

print output
