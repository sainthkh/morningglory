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
    title = StringField()
    content = StringField()
    comments = ListField(EmbeddedDocumentField('Comment'))
