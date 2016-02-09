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

def get_order(id):
	try:
		order = Order.objects.get(id=id)
	except:
		raise Http404
	
	return order