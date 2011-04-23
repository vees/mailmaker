import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

output=''
allprop=Property.objects.filter(community__name='Harford Park').order_by('street', 'house')
pre = ''
for p in allprop:
	if pre!=p.street:
		output += '\n'
		output += p.street + '\n'
		output += "=" * len(p.street) + '\n'
		pre=p.street
	output += p.__unicode__() + '\n'

print output
