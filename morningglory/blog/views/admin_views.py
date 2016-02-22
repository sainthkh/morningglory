from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from blog.models import *
from blog.utils.views import *
from blog.utils.models import *


#
# Admin Views
#
####################################################################
@login_required
def dashboard(request):
	return render(request, 'admin/dashboard.html', {
	})

#
# Writing Views
#
###########################################################

class PostAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Post, 'Post')
	
	def list_context(self, request, context):
		return {
			"writings": context["writings"].order_by("-published_date")
		}
	
	def save_others(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = primary_level_slug(POST['title'])
			
		writing.series_slug = POST['series']

class PageAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Page, 'Page')
	
	def save_others(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = primary_level_slug(POST['title'])

		writing.layout = POST['layout']

class SeriesAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Series, 'Series')
	
	def save_others(self, writing, POST):
		writing.category_slug = POST['category']

class CategoryAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Category, 'Category')

class EmailAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Email, 'Email')

class EmailListAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, EmailList, 'Email List')
	
	def save_others(self, writing, POST):
		writing.lead_magnet_slug = POST['lead-magnet-slug']
		writing.thankyou_page = POST['thankyou-page']

class LinkAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Link, 'Link')
	
	def edit_context(self, request):
		return {
			"page_title": "Edit Link",
		}
	
	def save_others(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = primary_level_slug(POST['slug'])
		
		writing.url = POST['url']

class ProductAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Product, 'Product')
	
	def add_new_context(self, request):
		writing = {
			"files": ['', '', '', '', ''],
		}
		
		return {
			"writing": writing,
		}
	
	def save_others(self, writing, POST):
		writing.thank_you = POST['thank-you']
		writing.price = float(POST['price'])
		writing.thumbnail = POST['thumbnail']
		
		writing.files = []
		for i in range(0, 5):
			filename = POST['filename-' + str(i)].strip()
			writing.files.append(filename)

class AddSubscriber(View):
	def get(self, request):
		return render(request, "admin/email-list/subscriber.html", {
		})
	
	def post(self, request):
		user_email = request.POST['email']
		first_name = request.POST['first-name']
		
		# get email list
		emaillist = get_writing(EmailList, request.POST['slug'])
		
		# get user
		if User.objects(email=user_email).count() > 0:
			user = User.objects(email=user_email)[0]
		else:
			user = User()
			user.first_name = first_name
			user.email = user_email
			user.save()	
		
		# add list to subscriber
		if not emaillist.slug in user.subscribed_lists:
			user.subscribed_lists.append(emaillist.slug)
			user.save()
			
		return render(request, "admin/email-list/subscriber.html", {
		})
#
# Activity Views
#
##############################################################
@login_required
def activities(request):
	activities = Activity.objects
	return render(request, 'admin/activities.html', {
		"activities": activities,
	})

@login_required
def approve_comment(request, pos):
	activity = Activity.objects[int(pos)]
	
	post = Post.objects(slug=activity.slug)[0]
	post.comments.append(activity.comment)
	post.save()
	
	activity.status = 'approved'
	activity.save()
	
	return redirect('blog:admin-activities')	

#
# Setting Views
#
###############################################################

@login_required
def settings(request):
	akismet_key = get_setting('akismet')
	stripe_public_key = get_setting('stripe-public-key')
	stripe_private_key = get_setting('stripe-private-key')
	paypal_client_id = get_setting('paypal-client-id')
	paypal_client_secret = get_setting('paypal-client-secret')
	paypal_mode = get_setting('paypal-mode')
	
	return render(request, 'admin/settings.html', {
		"akismet_key": akismet_key,
		"stripe_public_key": stripe_public_key,
		"stripe_private_key": stripe_private_key,
		"paypal_client_id": paypal_client_id,
		"paypal_client_secret": paypal_client_secret,
		"paypal_mode": paypal_mode,
	})



@login_required	
def save_settings(request):
	save_setting('akismet', request.POST['akismet-key'])
	save_setting('stripe-private-key', request.POST['stripe-private-key'])
	save_setting('stripe-public-key', request.POST['stripe-public-key'])
	save_setting('paypal-client-id', request.POST['paypal-client-id'])
	save_setting('paypal-client-secret', request.POST['paypal-client-secret'])
	save_setting('paypal-mode', request.POST['paypal-mode'])
	
	return redirect('blog:admin-settings')

#
# Order
#
################################################################
def admin_order(request):
	orders = Order.objects.order_by("-date")
	return render(request, "admin/order/list.html", {
		"orders": orders,
	})
