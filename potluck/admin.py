from harfordpark.potluck.models import *
from django.contrib import admin

admin.site.register(Community)
admin.site.register(County)
admin.site.register(Interest)
admin.site.register(Industry)
admin.site.register(Household)
admin.site.register(Business)

class PropertyAdmin(admin.ModelAdmin):
	list_display= ('address','community','county','city','zip')
	list_editable= ('community','county','city','zip')
	ordering = ['house']
	list_filter=('community','street')

class PersonAdmin(admin.ModelAdmin):
	list_display = ('firstname','lastname','phone','email','gender','household','in_good_standing')
	list_editable = ('phone','email','gender','household')
	list_per_page = 10
	save_on_top = True
	#radio_fields = { "gender": admin.HORIZONTAL }
	filter_horizontal = ['interests']

admin.site.register(Property, PropertyAdmin)
admin.site.register(Person, PersonAdmin)

