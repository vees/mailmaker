import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

p=Property.objects.filter(street='Moore Ave')

c=Community.objects.filter(name='North Harford Road')[0]

for pp in p:
	if int(pp.house) % 2 == 1:
		print pp.__unicode__()
		pp.community=c
		pp.save()

