from django.db import models
import urllib
# http://docs.djangoproject.com/en/dev/ref/contrib/localflavor/#united-states-of-america-us
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
import string

class PersonEmail(models.Model):
	def __unicode__(self):
		return self.address
	address = models.EmailField(null=False, unique=True)
	contact = models.BooleanField()

class PersonPhone(models.Model):
	def __unicode__(self):
		return self.number
	PHONE_CHOICES = (
		('H', 'Home'),
		('W', 'Work'),
		('M', 'Mobile'),
		('O', 'Other')
	)
	number = PhoneNumberField(null=False, unique=True)
	type = models.CharField(max_length=1, choices=PHONE_CHOICES)
	contact = models.BooleanField()

class PersonInterest(models.Model):
	description = models.CharField(max_length=50)

class AgeGroup(models.Model):
	def __unicode__(self):
		return self.description
	description = models.CharField(max_length=30)

class Person(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	def __unicode__(self):
		return u"{0} {1}".format(self.firstname,self.lastname)
		#return self.firstname + " " + self.lastname
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	age_group = models.ForeignKey(AgeGroup, null=True, blank=True)
	phones = models.ManyToManyField(PersonPhone, null=True, blank=True)
	emails = models.ManyToManyField(PersonEmail, null=True, blank=True)
	interests = models.ManyToManyField(PersonInterest, null=True, blank=True)

# Create your models here.
class County(models.Model):
	def __unicode__(self):
		return u"{0}, {1}".format(self.name,self.state)
		#return self.name + " " + self.state
	name = models.CharField(max_length=50, null=False)
	state = USStateField(null=False)
	resicode = models.CharField(max_length=2, null=False)

class Street(models.Model):
	def __unicode__(self):
		return self.name +" " +self.county.name
		return u"{0} {1}".format(self.name,self.county.name)
	county = models.ForeignKey(County, null=False)
	name = models.CharField(max_length=50)

class Property(models.Model):
	def __unicode__(self):
		return "{0}{1} {2}".format(self.number, self.suffix, self.street.name)
		#return str(self.number) + " " + self.street.name
	number = models.IntegerField(null=False, blank=False)
	suffix = models.CharField(max_length=15, null=True, blank=True)
	street = models.ForeignKey(Street, null=False)
	residents = models.ManyToManyField(Person, null=True, blank=True)
	# Geography 
	# http://www.fairviewcomputing.com/blog/2008/04/16/django-geography-hacks/
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)

class UnitType(models.Model):
	description = models.CharField(max_length=30)

class Unit(models.Model):
	type = models.ForeignKey(UnitType, null=False)
	residents = models.ManyToManyField(Person, null=True, blank=True)

class ResiProperty(models.Model):
	def resiurl(self):
		url="http://sdatcert3.resiusa.org/rp_rewrite/details.aspx"
		return "{0}?AccountNumber={1}County={2}&SearchType=STREET".format(
			urllib.quote(self.account_number),
			self.property.street.county.resicode,
			url)
	property = models.ForeignKey(Property, null=False)
	account_number = models.CharField(max_length=50, null=False)
	owner_names = models.CharField(max_length=500, null=True, blank=True)
	owner_mailing = models.CharField(max_length=500, null=True, blank=True)
	owner_occupied = models.NullBooleanField(null=True, blank=True)

