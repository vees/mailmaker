from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField

class County(models.Model):
	def __unicode__(self):
		return u"{0}, {1}".format(self.name,self.state)
	name = models.CharField(max_length=50, null=False)
	state = USStateField(null=False)
	resicode = models.CharField(max_length=2, null=False)

class Property(models.Model):
	def __unicode__(self):
		return u"{0} {1} {2} ({3} County) {4} {5}".format(
			self.house, self.street, self.city, self.county.name, self.county.state, self.zip)
	def resiurl(self):
		url="http://sdatcert3.resiusa.org/rp_rewrite/details.aspx"
		return "{0}?AccountNumber={1}County={2}&SearchType=STREET".format(
			url,
			urllib.quote(self.account_number),
			self.county.resicode)
	house = models.CharField(max_length=10, null=False)
	street = models.CharField(max_length=50, null=False)
	county = models.ForeignKey(County, null=False, blank=False)
	city = models.CharField(max_length=50, null=False)
	#zip = us.forms.USZipCodeField(null=False)
	zip = models.CharField(max_length=10, null=False)
	account = models.CharField(max_length=50, null=False)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)

class Interest(models.Model):
	description = models.CharField(max_length=50)

class Industry(models.Model):
	description = models.CharField(max_length=50, null=False, blank=False)

# Membership is stored interally to a household
# since a membership can travel from Property to 
# Property with the household
class Household(models.Model):
	def __unicode__(self):
		# Also need to code for the case where the name is not
		# defined and we need to use the name of the head instead.
		return u"{0} {1} Household".format()
	MEMBERSHIP_CHOICES = (
		('R', 'Resident'),
		('A', 'Auxiliary'),
	)
  	name = models.CharField(max_length=50, null=True, blank=True)
	property = models.ForeignKey(Property, unique=False, null=True, blank=True)
	address_append = models.CharField(max_length=50, null=True, blank=True) 
	# Head of household must also be a member of the household
	activated = models.DateField(auto_now=False, auto_now_add=False)
	last_renewal = models.DateField(auto_now=False, auto_now_add=False)
	type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES)

class Person(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	def __unicode__(self):
		return u"{0} {1}".format(self.firstname,self.lastname)
	head = models.NullBooleanField()
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	phone = PhoneNumberField(null=False, unique=False)
	phone_backup = PhoneNumberField(null=False, unique=False)
	email = models.EmailField(null=False, unique=False)
	email_backup = models.EmailField(null=False, unique=False)
	birthday = models.DateField(auto_now=False, auto_now_add=False)
	website = models.URLField(verify_exists=True, max_length=200)
	interests = models.ManyToManyField(Interest, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	household = models.ForeignKey(Household, unique=False, null=False, blank=False)

class Business(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	owner = models.ForeignKey(Person, unique=True, null=True, blank=True,
		related_name='owner_set')
	phone = PhoneNumberField(null=True, unique=False)
	email = models.EmailField(null=True, unique=False)
	website = models.URLField(verify_exists=True, max_length=200)
	location = models.ForeignKey(Property, unique=False, null=False, blank=False)
	address_append = models.CharField(max_length=50, null=True, blank=True)
	industries = models.ManyToManyField(Industry, null=True, blank=True)
	employees = models.ManyToManyField(Person, null=True, blank=True)

