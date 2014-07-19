from django.core.management.base import BaseCommand, CommandError
from potluck import views

class Command(BaseCommand):
	def handle(self, *args, **options):
		print views._generate_local()

