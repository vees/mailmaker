import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

hp = Community.objects.filter(pk=1)[0]
baco = County.objects.filter(pk=1)[0]

fsfr=csv.DictReader(open('Harford Park Email List For Import.csv'), dialect='excel')
for row in fsfr:
	p = Person()
	p.firstname = row['first']
	p.lastname = row['last']
	p.phone = row['phone']
	p.email = row['email']
	p.email_backup = row['email2']
	p.website = row['url']
	p.save()


