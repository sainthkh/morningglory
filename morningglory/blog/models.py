from django.db import models
from mongoengine import *

# Create your models here.

class Comment(EmbeddedDocument):
    name = StringField(required=True)
    email = StringField()
    website = StringField()
    content = StringField()

class Post(Document):
    slug = StringField(unique=True)
    title = StringField(required=True)
    content = StringField()
    comments = ListField(EmbeddedDocumentField('Comment'))
