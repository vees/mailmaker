from django.core.management.base import BaseCommand, CommandError
from harfordpark.potluck import views

class Command(BaseCommand):
    args = ''
    help = 'Checks configuration file'

    def handle(self, *args, **options):
				a= views._generate_local()
				print a
				return a	

