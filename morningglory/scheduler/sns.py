from django.conf import settings

from threading import Thread
from datetime import timedelta, datetime
from twython import Twython, TwythonError
import random

from blog.models import *
from blog.utils.models import get_setting, save_setting

class SnsUploader(Thread):
	def __init__(self, schedule):
		self.schedule = schedule
	
	def run(self):
		loop_slug = self.schedule.content['loop-slug']
		loop = MessageLoop.objects.get(slug=loop_slug)

		message_group = MessageGroup.objects(message_loop_slug=loop_slug).order_by("created_date")[loop.current]
		message = message_group.messages[message_group.current]
		
		message.text = message.text.replace("%link%", message_group.link)
		hashtags = loop.hashtags + message_group.hashtags
		self.send_message(message, hashtags)
		
		current_time = datetime.now()
		message_group.last_published_date = current_time
		
		message_group.current = message_group.current + 1
		if len(message_group.messages) == message_group.current:
			message_group.current = 1 
		
		message_group.save()
		
		loop.last_published_date = current_time
		
		loop.current = loop.current + 1
		if MessageGroup.objects(message_loop_slug=loop_slug).count() == loop.current:
			loop.current = 0
		
		loop.save()
		
		self.schedule.time = self.schedule.time + timedelta(minutes=loop.term)
		self.schedule.save()
	
	def send_message(self, messsage, hashtags):
		pass

class TwitterUploader(SnsUploader):
	def __init__(self, schedule):
		SnsUploader.__init__(self, schedule)
	
	def send_message(self, message, hashtags):
		hashtag = hashtags[random.randint(0, len(hashtags) - 1)]
		
		tweet_message = message.text + ' ' + hashtag
		if len(tweet_message) > 140:
			tweet_message = message.text
		
		APP_KEY = get_setting('twitter-app-key')
		APP_SECRET = get_setting('twitter-app-secret')
		OAUTH_TOKEN = get_setting('twitter-oauth-token')
		OAUTH_TOKEN_SECRET = get_setting('twitter-oauth-token-secret')
		
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		
		image_ids = []
		
		if len(message.images) > 0:
			for i in message.images:
				photo = open(settings.MEDIA_ROOT + i)
				response = twitter.upload_media(media=photo)
				image_ids.append(response['media_id'])
		
		twitter.update_status(status=tweet_message, media_ids=image_ids)

class TestUploader(SnsUploader):
	def __init__(self, schedule):
		SnsUploader.__init__(self, schedule)
	
	def send_message(self, message, hashtags):
		print(message.text)