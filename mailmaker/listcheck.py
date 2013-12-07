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

mdtext = ''
publish_type = 'publish'
target_date = datetime.date(2013,6,5)

articles = Article.objects \
	.exclude(embargo_date__gt=target_date, embargo_date__isnull=False) \
	.exclude(expires_date__lt=target_date, expires_date__isnull=False) \
	.exclude(repeat_limit__lte=F('posted_count')-1, repeat_limit__isnull=False, posted_count__isnull=False) \
	.order_by('id').reverse()

filter_list = []
for article in articles:
	if (article.next_post() > target_date):
		filter_list.append(article.id)
		print filter_list
articles = articles.exclude(id__in=filter_list)

#mdtext = "In this update:\n\n";
#for article in articles:
#	mdtext += "* {0}\n".format(article.title)
#mdtext += "\n\n";

title = "Updates for {0}".format(datetime.date.strftime(target_date, "%B %-d, %Y"))

#mdtext += u'#{0} {1}\n\n'.format(parser.get('mailchimp', 'assoc_name'), title)

#newthisweek = articles.filter(posted_last=None)
#if len(newthisweek)>0:
#	mdtext += u'##New This Week\n\n'
#for article in newthisweek:
#	mdtext += u'{0},'.format(article.title, article.category.longname)
#mdtext += 'and more.\n\n'

for category in Category.objects.all().order_by('priority'):
	articlesubset = articles.filter(category=category)
	if len(articlesubset)>0:
		if (category.shortname=='Alerts'):
			title="Alert: {0}".format(articlesubset[0].title)
		mdtext += u'##{0}\n\n'.format(category.longname)
	for article in articlesubset:
		mdtext += u'**{0}** {2}\n\n{1}\n\n'.format(article.title,article.text,article.is_new())
		if (publish_type=='publish' and article.posted_last != target_date):
			article.posted_last = target_date
			if article.posted_count == None:
				article.posted_count=1
			else:
				article.posted_count += 1
			article.save()

html = markdown.markdown(mdtext)

url = parser.get('wordpress', 'xmlrpc')
wp = wordpresslib.WordPressClient(url, parser.get('wordpress', 'username'), parser.get('wordpress', 'password'))
wp.selectBlog(0)
post = wordpresslib.WordPressPost()
post.title = title
post.description = html
if publish_type=='publish':
	idPost = wp.newPost(post, False)

if publish_type=='preview':
	print title
	print html.encode('ascii','ignore')

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
msg['Subject'] = "{0} {1}".format(parser.get('mailchimp', 'assoc_name'), title)
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
if publish_type=='publish':
	s.sendmail(me, you, msg.as_string())
s.quit()

