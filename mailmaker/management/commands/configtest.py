from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('simple.ini')

print parser.get('wordpress', 'username')
print parser.get('wordpress', 'password')

print parser.get('mailchimp', 'from_email')
print parser.get('mailchimp', 'server')

