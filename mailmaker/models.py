from django.db import models
import datetime

# Create your models here.
class Category(models.Model):
	def __unicode__(self):
		return self.shortname
	shortname = models.CharField(max_length=100)
	longname = models.CharField(max_length=100)
	priority = models.IntegerField(null=False, blank=False)

class Article(models.Model):
	def __unicode__(self):
		return self.title
	title = models.CharField("Title", max_length=100, blank=False)
	text = models.TextField("Article Text", blank=False)
	category = models.ForeignKey(Category)
	embargo_date = models.DateField(null=True, blank=True)
	expires_date = models.DateField(null=True, blank=True)
	repeat_limit = models.IntegerField(null=True, blank=True, default=0)
	days_between = models.IntegerField(null=True, blank=True, default=7)
	posted_last = models.DateField(null=True, blank=True)
	posted_count = models.IntegerField(null=True, blank=True)
	def is_new(self):
		if (self.posted_last is None):
			return "(*New!*)"
		return ""
	def next_post(self):
		if (self.days_between is None):
			return datetime.date.today()
		if (self.posted_last is None):
			return datetime.date.today()
		else:
			return self.posted_last + datetime.timedelta(days=self.days_between)
	def throttled(self):
		return self.next_post() <= datetime.date.today()

