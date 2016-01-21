from django.db import models
from mongoengine import *

# Create your models here.

class Comment(DynamicDocument):
	name = StringField(required=True)
	email = StringField()
	website = StringField()
	time = DateTimeField()
	content = StringField()

class Post(DynamicDocument):
	slug = StringField(unique=True)
	post_type = StringField()
	published_date = DateTimeField()
	last_modified_date = DateTimeField()
	series_slug = StringField()
	title = StringField()
	content = StringField()
	compiled_content = StringField()
	excerpt = StringField()
	key_points = StringField()
	splash_image_path = StringField()
	comments = ListField(EmbeddedDocumentField('Comment'))

class Category(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	content = StringField()
	
class Series(DynamicDocument):
	slug = StringField(unique=True)
	category_slug = StringField()
	title = StringField()
	content = StringField()
	key_points = StringField()
	excerpt = StringField()

class Secret(Document):
	name = StringField(required=True, unique=True)
	key = StringField()

class Activity(DynamicDocument):
	date = DateTimeField()
	template = ''
	
	meta = {
		"allow_inheritance": True,
	}

class CommentActivity(Activity):
	comment = EmbeddedDocumentField('Comment')
	slug = StringField()
	title = StringField()
	template = 'activity/comment.html'
	

class SpamCommentActivity(CommentActivity):
	template = 'activity/spam-comment.html'
	status = StringField(default='spam')