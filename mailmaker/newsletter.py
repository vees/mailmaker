from mailmaker.models import *
import markdown
import datetime
import sys
sys.path.append("/home/rob/Projects/")
sys.path.append("/home/rob/Projects/hpcatools")
sys.path.append("/home/rob/Projects/hpcatools/mailmaker")

mdtext = ''
publish_type = 'preview'

for article in Article.objects.all():
	mdtext += u'**{0}**\n\n{1}\n\n'.format(article.title,article.text)
	if publish_type=='publish':
		article.posted_last = datetime.datetime.now()
		if article.posted_count == None:
			article.posted_count=1
		else:
			article.posted_count += 1
		#article.posted_last = None
		#article.posted_count = None
		article.save()

html = markdown.markdown(mdtext)

print html.encode('ascii','ignore')

