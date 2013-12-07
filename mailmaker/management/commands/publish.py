from django.core.management.base import BaseCommand, CommandError
import mailmaker.listcheck

class Command(BaseCommand):
    args = ''
    help = 'Checks configuration file'

    def handle(self, *args, **options):
        lc = mailmaker.listcheck.Do()

