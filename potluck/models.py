from django.db import models
#from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
import datetime

class County(models.Model):
	def __unicode__(self):
		return u"{0}, {1}".format(self.name,self.state)
	name = models.CharField(max_length=50, null=False)
	state = models.CharField(null=False)
	resicode = models.CharField(max_length=2, null=False)
	class Meta:
		verbose_name_plural = "Counties"

class Community(models.Model):
	def __unicode__(self):
		return self.name	
	name = models.CharField(max_length=50, null=False, blank=False)
	class Meta:
		verbose_name_plural = "Communities"

class Property(models.Model):
	def __unicode__(self):
		return u"{0} {1} {2} ({3} County) {4} {5}".format(
			self.house, self.street, self.city, self.county.name, self.county.state, self.zip)
	def shortlink(self):
		return u"{0} {1}".format(self.house,self.street)
	def resiurl(self):
		url="http://sdatcert3.resiusa.org/rp_rewrite/details.aspx"
		return "{0}?AccountNumber={1}County={2}&SearchType=STREET".format(
			url,
			urllib.quote(self.account),
			self.county.resicode)
	def address(self):
		return "{0} {1}".format(self.house, self.street)
	address.short_description = 'Address'
	house = models.CharField(max_length=10, null=False)
	street = models.CharField(max_length=50, null=False)
	community = models.ForeignKey(Community, null=True, blank=True)
	county = models.ForeignKey(County, null=False, blank=False)
	city = models.CharField(max_length=50, null=False)
	#zip = us.forms.USZipCodeField(null=False)
	zip = models.CharField(max_length=10, null=False)
	account = models.CharField(max_length=50, null=True, blank=True)
	owner_occupied = models.NullBooleanField(blank=True)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	class Meta:
		verbose_name_plural = "Properties"

class Interest(models.Model):
	def __unicode__(self):
		return self.description
	description = models.CharField(max_length=50)
	class Meta:
		ordering = ['description']

class Industry(models.Model):
	def __unicode__(self):
		return self.description
	description = models.CharField(max_length=50, null=False, blank=False)
	class Meta:
		verbose_name_plural = "Industries"

# Membership is stored interally to a household
# since a membership can travel from Property to 
# Property with the household
class Household(models.Model):
	def __unicode__(self):
		# Also need to code for the case where the name is not
		# defined and we need to use the name of the head instead.
		return u"{0} Household at {1}".format(self.name, self.property.street)
	def in_good_standing(self):
		return self.last_renewal.year>=datetime.datetime.now().year
	MEMBERSHIP_CHOICES = (
		('R', 'Resident'),
		('A', 'Auxiliary'),
	)
  	name = models.CharField(max_length=50, null=True, blank=True)
	property = models.ForeignKey(Property, unique=False, null=True, blank=True)
	address_append = models.CharField(max_length=50, null=True, blank=True) 
	# Head of household must also be a member of the household
	activated = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
	last_renewal = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
	type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, null=True, blank=True)
	class Meta:
		ordering = ['name']

class Person(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	def __unicode__(self):
		return u"{0} {1}".format(self.firstname,self.lastname)
	def in_good_standing(self):
		if self.household == None:
			return False
		if self.household.last_renewal == None:
			return False
		else:
			return self.household.in_good_standing()
	in_good_standing.boolean=True
	head = models.NullBooleanField()
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	phone = models.CharField(null=True, blank=True, unique=False, max_length=15)
	phone_backup = models.CharField(null=True, blank=True, unique=False)
	email = models.EmailField(null=True, blank=True, unique=False)
	email_backup = models.EmailField(null=True, blank=True, unique=False)
	birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, unique=False)
	website = models.URLField(max_length=200, null=True, blank=True, unique=False)
	interests = models.ManyToManyField(Interest, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, unique=False)
	household = models.ForeignKey(Household, unique=False, null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	last_modified = models.DateField(auto_now=True)
	created_on = models.DateField(auto_now_add=True)
	class Meta:
		ordering = ['lastname','firstname']
		verbose_name_plural = 'People'

class Business(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=50, null=True, blank=True)
	owner = models.ForeignKey(Person, unique=True, null=True, blank=True,
		related_name='owner_set')
	phone = models.CharField(null=True, blank=True, unique=False)
	email = models.EmailField(null=True, blank=True, unique=False)
	website = models.URLField(null=True, blank=True, max_length=200)
	location = models.ForeignKey(Property, unique=False, null=False, blank=False)
	address_append = models.CharField(max_length=50, null=True, blank=True)
	industries = models.ManyToManyField(Industry, null=True, blank=True)
	employees = models.ManyToManyField(Person, null=True, blank=True)
	class Meta:
		verbose_name_plural = 'Businesses'

