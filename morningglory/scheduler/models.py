from mongoengine import *

#
# Schedule Models
#
################################################################
class Schedule(DynamicDocument):
	slug = StringField(unique=True)
	type = StringField()
	time = DateTimeField()
	content = DictField()
