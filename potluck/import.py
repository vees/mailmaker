import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

hp = Community.objects.filter(pk=1)[0]
baco = County.objects.filter(pk=1)[0]

fsfr=csv.DictReader(open('HP-Only Load List.csv'), dialect='excel')
for row in fsfr:
	p = Property()
	p.house = row['House']
	p.street = row['Street']
	p.community = hp
	p.county = baco
	p.city = row['City']
	p.zip = row['Zip']
	p.save()


