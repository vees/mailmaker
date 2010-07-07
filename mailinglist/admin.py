from harfordpark.mailinglist.models import *
from django.contrib import admin

#http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal
class PersonAdmin(admin.ModelAdmin):
	#list_display = ['firstname','lastname']
	filter_horizontal = ['phones','emails']
	#fields = [ 'firstname','lastname','gender','age_group','phones','emails','interests' ]

class StreetAdmin(admin.ModelAdmin):
	ordering = ['name','county']

admin.site.register(PersonEmail)
admin.site.register(PersonPhone)
admin.site.register(PersonInterest)
admin.site.register(AgeGroup)
admin.site.register(Person, PersonAdmin)
admin.site.register(County)
admin.site.register(Street, StreetAdmin)
admin.site.register(Property)
admin.site.register(UnitType)
admin.site.register(Unit)
admin.site.register(ResiProperty)

