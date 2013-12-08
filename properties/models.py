from django.db import models

# Create your models here.
class Street(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=50)

class Property(models.Model):
	def __unicode__(self):
		return str(self.number) + " " + self.street.name
	number = models.IntegerField(null=False, blank=False)	
	street = models.ForeignKey(Street, null=False)

class Listing(models.Model):
	def __unicode__(self):
		return self.mls + " " + self.property.__unicode__()
	mls = models.CharField(max_length=30)
	property = models.ForeignKey(Property, null=False)
	first_seen = models.DateField(null=False)
	sold_on = models.DateField(null=True, blank=True)
	active = models.BooleanField()

class ListingWebPage(models.Model):
	def __unicode__(self):
		return self.listing.mls + " " + self.listing.property.__unicode__() + " " + self.url[7:40]
	listing = models.ForeignKey(Listing)
	url = models.URLField(max_length=200)
	active = models.BooleanField()

