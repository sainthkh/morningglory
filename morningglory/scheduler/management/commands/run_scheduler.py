from django.core.management.base import BaseCommand, CommandError

from datetime import datetime

from scheduler.models import *
from scheduler.sns import * 

class Command(BaseCommand):
	def handle(self, *arg, **options):
		schedules = Schedule.objects(time__lte = datetime.now())
			
		for s in schedules:
			handler = self.create_handler(s)
			handler.run()
	
	def create_handler(self, schedule):
		if schedule.type == "twitter":
			return TwitterUploader(schedule)
		elif schedule.type == "facebook":
			return FacebookUploader(schedule)
