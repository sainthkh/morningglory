from django.core.management.base import BaseCommand, CommandError
from blog.models import *
from morningglory import settings
from datetime import datetime
import os

class Command(BaseCommand):
	def handle(self, *arg, **options):
		if settings.DEBUG == False:
			return
		Post.drop_collection()
		Category.drop_collection()
		Series.drop_collection()
		
		dir = os.path.dirname(os.path.realpath(__file__)) + '/'
		
		post = Post()
		post.slug = '1234'
		post.post_type = 'post'
		post.published_date = datetime.now()
		post.last_modified_date = datetime.now()
		post.title = "용어, 기간, 임기, 텀, 학기, 이용 약관 – Korean Words vs. Words S2 #11"
		with open(dir + 'real-data-1.html', encoding='utf-8') as f:
			post.content = f.read()
		
		post.save()