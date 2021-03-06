from django.http import Http404

from datetime import datetime

from blog.models import *

def create_order(email, payment_method, product, status='complete'):
	order = Order()
	
	order.email = email
	order.date = datetime.now()
	order.payment_method = payment_method
	order.product_slug = product.slug
	order.product_name = product.title
	order.status = status
	
	order.save()
	order.reload()
	
	return order

def get_order(id):
	if not isinstance(id, int):
		id = int(id)

	try:
		order = Order.objects.get(number=id)
	except:
		raise Http404
	
	return order

#
# Setting functions
#
##################################################################
def get_setting(name):
	if len(Setting.objects(name=name)) > 0:
		value = (Setting.objects(name=name)[0]).value
	else:
		value = ''
	
	return value

def save_setting(name, value):
	if len(Setting.objects(name=name)) > 0:
		setting = Setting.objects(name=name)[0]
	else:
		setting = Setting()
		setting.name = name
	
	setting.value = value
	setting.save()