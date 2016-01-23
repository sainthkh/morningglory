from django.db import models
from mongoengine import *

class Subscriber(DynamicDocument):
	first_name = StringField(max_length=128)
	email = StringField(max_length=254, unique=True)

class Email(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	content = StringField()

class EmailList(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	subscribers = ListField(ReferenceField('Subscriber'))
