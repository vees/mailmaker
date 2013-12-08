from properties.models import *

s=Street.objects.all().order_by('name')
for st in s:
	print st.name
	p = Property.objects.filter(street=st)
	for pp in p:
		print "  " + pp.__unicode__()
		l = Listing.objects.filter(property=pp)
		for ll in l:
			ws = ListingWebPage.objects.filter(listing=ll)
			for ww in ws:
				print "    " + ww.url

