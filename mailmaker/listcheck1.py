from mailmaker.models import *
from django.db.models import F
import markdown
import datetime
import sys
import wordpresslib
from ConfigParser import SafeConfigParser
sys.path.append("/home/rob/Projects/")
sys.path.append("/home/rob/Projects/hpcatools")
sys.path.append("/home/rob/Projects/hpcatools/mailmaker")

parser = SafeConfigParser()
parser.read('simple.ini')

#print parser.get('wordpress', 'username')
#print parser.get('wordpress', 'password')
#print parser.get('mailchimp', 'email')
#print parser.get('mailchimp', 'server')

mdtext = ''
publish_type = 'preview'
target_date = datetime.date(2013,3,27)

articles = Article.objects \
	.exclude(embargo_date__gt=datetime.datetime.now(), embargo_date__isnull=False) \
	.exclude(expires_date__lt=datetime.datetime.now(), expires_date__isnull=False) \
	.exclude(repeat_limit__lt=F('posted_count')-1, repeat_limit__isnull=False, posted_count__isnull=False)

#mdtext = "In this update:\n\n";
#for article in articles:
#	mdtext += "* {0}\n".format(article.title)
#mdtext += "\n\n";

for category in Category.objects.all().order_by('priority'):
	articlesubset = articles.filter(category=category)
	if len(articlesubset)>0:
		mdtext += u'##{0}\n\n'.format(category.longname)
	for article in articlesubset:
		mdtext += u'**{0}**: {1}\n\n'.format(article.title,article.text)
		if publish_type=='publish':
			article.posted_last = datetime.datetime.now()
			if article.posted_count == None:
				article.posted_count=1
			else:
				article.posted_count += 1
			article.save()

title = "Updates for {0}".format(datetime.date.strftime(datetime.date.today(), "%B %-d, %Y"))
html = markdown.markdown(mdtext)

url = parser.get('wordpress', 'xmlrpc')
wp = wordpresslib.WordPressClient(url, parser.get('wordpress', 'username'), parser.get('wordpress', 'password'))
wp.selectBlog(0)
post = wordpresslib.WordPressPost()
post.title = title
post.description = html
idPost = wp.newPost(post, False)

#print title
#print html.encode('ascii','ignore')

html = html.encode('ascii','ignore')
mdtext = mdtext.encode('ascii','ignore')

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = parser.get('mailchimp', 'from_email')
you = parser.get('mailchimp', 'to_email')

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "{0} {1}".format(title, parser.get('mailchimp', 'assoc_name'))
msg['From'] = me
msg['To'] = you
msg['Reply-To'] = me

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(mdtext, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP(parser.get('mailchimp', 'server'))
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()

