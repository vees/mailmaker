import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

i1=Interest.objects.filter(description='Newsletter')[0]
i2=Interest.objects.filter(description='Social Events')[0]
i3=Interest.objects.filter(description='Crime Alerts')[0]

for p in Person.objects.all():
	p.interests.add(i1)
	p.interests.add(i2)
	p.interests.add(i3)
	p.save()

