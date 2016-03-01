from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from datetime import datetime

from scheduler.models import *

class Command(BaseCommand):
	def handle(self, *arg, **options):
		if settings.DEBUG == False:
			return
		
		Schedule.drop_collection()