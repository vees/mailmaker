import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

for a in [a for a in set([p.email for p in Person.objects.exclude(email='').filter(interests__description="Newsletter")])]:
	print a
