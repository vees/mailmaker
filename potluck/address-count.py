import csv
from potluck.models import *
import sys
sys.path.append("/home/robvees/harfordpark.com") 

print len(Property.objects.filter(community__name='Harford Park'))
