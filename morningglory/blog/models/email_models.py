from django.db import models
from mongoengine import *

class Subscriber(DynamicDocument):
    first_name = StringField(max_length=128)
    email = StringField(max_length=254, unique=True)

class Email(DynamicDocument):
    title = StringField(max_length=512)
    content = StringField(max_length=30000)
    def __str__(self):
        return self.title

class EmailList(DynamicDocument):
    name = StringField(max_length=128)
    subscribers = ListField(ReferenceField('Subscriber'))
