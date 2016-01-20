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
	series = ReferenceField('Series')
	title = StringField()
	content = StringField()
	compiled_content = StringField()
	excerpt = StringField()
	key_points = StringField()
	splash_image_path = StringField()
	comments = ListField(EmbeddedDocumentField('Comment'))

class Category(DynamicDocument):
	slug = StringField(unique=True)
	name = StringField()
	series_list = ListField(ReferenceField('Series'))
	
class Series(DynamicDocument):
	slug = StringField(unique=True)
	category = ReferenceField('Catergory')
	title = StringField()
	introduction = StringField()
	key_points = StringField()
	excerpt = StringField()
	post_list = ListField(ReferenceField('Post'))

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