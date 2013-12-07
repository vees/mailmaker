from django.core.management.base import BaseCommand, CommandError
from ConfigParser import SafeConfigParser

class Command(BaseCommand):
    args = ''
    help = 'Checks configuration file'

    def handle(self, *args, **options):
        self.configtest()

    def configtest(self):
        parser = SafeConfigParser()
        parser.read('/home/rob/Projects/hpcatools/mailmaker/simple.ini')

        print parser.get('wordpress', 'username')
        print parser.get('wordpress', 'password')

        print parser.get('mailchimp', 'from_email')
        print parser.get('mailchimp', 'server')

