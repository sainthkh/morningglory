from django.db import models
from mongoengine import *

# Create your models here.

class Comment(EmbeddedDocument):
	name = StringField(required=True)
	email = StringField()
	website = StringField()
	content = StringField()

class Post(DynamicDocument):
	slug = StringField(unique=True)
	post_type = StringField()
	published_date = DateTimeField()
	last_modified_date = DateTimeField() 
	title = StringField()
	content = StringField()
	comments = ListField(EmbeddedDocumentField('Comment'))

class Category(DynamicDocument):
	slug = StringField(unique=True)
	name = StringField()
	series_list = ListField(ReferenceField('Series'))
	
class Series(DynamicDocument):
	slug = StringField(unique=True)
	name = StringField()
	post_list = ListField(ReferenceField('Post'))