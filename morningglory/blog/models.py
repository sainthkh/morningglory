from django.db import models
from mongoengine import *

#
# Writing Models
#
###############################################################

class Comment(EmbeddedDocument):
	name = StringField(required=True)
	email = StringField()
	website = StringField()
	status = StringField()
	time = DateTimeField()
	content = StringField()

class Post(DynamicDocument):
	slug = StringField(unique=True)
	published_date = DateTimeField()
	last_modified_date = DateTimeField()
	series_slug = StringField()
	title = StringField()
	content = StringField()
	excerpt = StringField()
	key_points = StringField()
	splash_image_path = StringField()
	status = StringField()
	comments = ListField(EmbeddedDocumentField('Comment'))

class Page(DynamicDocument):
	slug = StringField(unique=True)
	published_date = DateTimeField()
	last_modified_date = DateTimeField()
	title = StringField()
	content = StringField()
	splash_image_path = StringField()
	comments = ListField(EmbeddedDocumentField('Comment'))
	layout = StringField()
	status = StringField()

class Category(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	content = StringField()
	status = StringField()
	
class Series(DynamicDocument):
	slug = StringField(unique=True)
	category_slug = StringField()
	title = StringField()
	content = StringField()
	key_points = StringField()
	excerpt = StringField()
	status = StringField()

class Link(DynamicDocument):
	slug = StringField(unique=True)
	url = StringField()
	status = StringField()

class Product(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	content = StringField()
	thank_you = StringField()
	special_offer = StringField()
	price = FloatField()
	files = ListField(StringField())
	thumbnail = StringField()
	status = StringField()

# slug list for Post, Page, Link
class PrimarySlug(Document):
	slug = StringField(unique=True)

class Order(DynamicDocument):
	number = SequenceField()
	date = DateTimeField()
	email = StringField()
	payment_method = StringField()
	product_slug = StringField()
	product_name = StringField()
	status = StringField()
	paypal_payment_id = StringField()
	
#
# Admin Models
#
##############################################################

class Setting(Document):
	name = StringField(required=True, unique=True)
	value = StringField()

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

#
# Membership Models
#
##############################################################
class User(DynamicDocument):
	email = StringField(max_length=254, unique=True)
	first_name = StringField()
	family_name = StringField()
	subscribed_lists = ListField(StringField())

#
# Email Models
#
################################################################
class Email(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	content = StringField()

class EmailList(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	lead_magnet_slug = StringField()
	thankyou_page = StringField()

#
# Message Models
#
################################################################
class MessageLoop(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	term = IntField()
	platform = StringField()
	hashtags = ListField(StringField())
	current = IntField()
	created_date = DateTimeField()
	last_published_date = DateTimeField()

class Message(EmbeddedDocument):
	text = StringField(unique=True)
	images = ListField(StringField())	

class MessageGroup(DynamicDocument):
	slug = StringField(unique=True)
	title = StringField()
	current = IntField()
	hashtags = ListField(StringField())
	message_loop_slug = StringField()
	last_published_date = DateTimeField()
	created_date = DateTimeField()
	messages = ListField(EmbeddedDocumentField('Message'))
	messages_text = StringField()
	