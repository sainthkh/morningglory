from django.core.management.base import BaseCommand, CommandError

from datetime import datetime

from scheduler.models import *

class Command(BaseCommand):
	def handle(self, *arg, **options):
		if Schedule.objects(slug="tweet").count() == 0:
			schedule = Schedule()
			schedule.slug = "tweet"
			schedule.time = datetime.now()
			schedule.type = "twitter"
			schedule.content = {
				'loop-slug':'twitter',
			}
			
			schedule.save()