from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings as django_setting
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail as django_send_mail

from datetime import datetime, date
from urllib.parse import quote, unquote
import re
import os
import paypalrestsdk
import stripe

from blog.models import *
from blog.utils import slugify, template_to_html
from blog.utils.views import *
from blog.utils.models import *

def index(request):
	return blog_main(request, 1)	

def blog_main(request, page):
	page = int(page)
	posts = Post.objects.order_by("-published_date")[(page-1)*5:page*5]
	products = Product.objects
	
	return render(request, 'blog/index.html', {
		"posts": posts,
		"products": products,
		"page": page,
	})
	
def single_post(request, year, month, date, slug):
	return redirect(reverse('blog:distribute-post', kwargs={"slug":unquote(slug)}))

def category(request, slug, page):
	series_list = Series.objects(category_slug=slug)
	
	return render(request, "blog/category.html", {
		"series_list": series_list,
	})

def series(request, slug):
	series = get_writing(Series, slug)
	return render(request, "blog/series.html", {
		"series" : series,
	})
	
def series_list(request, slug, page=None):
	if not page:
		page = 1
	page = int(page)
	posts = Post.objects(series_slug=normalize_slug(slug)).order_by("-published_date")[(page-1)*5:page*5]
	return render(request, "blog/series-list.html", {
		"posts": posts,
		"slug" : slug,
		"page" : page,
	})

def distribute_post(request, slug):
	post_queryset = Post.objects(slug=normalize_slug(slug))
	if post_queryset.count() > 0:
		post = post_queryset[0]
		return render(request, 'blog/single-post.html', {
			'post': post,
			'content': process_content(post.content),
		}) 
	
	page_queryset = Page.objects(slug=normalize_slug(slug))
	if page_queryset.count() > 0:
		page = page_queryset[0]
		return render(request, 'blog/single-post.html', {
			'post': page,
			'content': process_content(page.content),
		}) 
	
	link_queryset = Link.objects(slug=normalize_slug(slug))
	if link_queryset.count() > 0:
		link = link_queryset[0]
		return redirect(link.url)
	
	raise Http404  

def upload_file(request):
	files = upload_files(django_setting.MEDIA_ROOT, request.FILES)
	filetext = ' '.join("($ {0} $)".format(f) for f in files)

	data = {}
	data['success'] = True
	data['filetext'] = filetext
	return JsonResponse(data)

def upload_to_restricted(request):
	files = upload_files(django_setting.RESTRICTED_ROOT, request.FILES)
	filetext = ''.join("{0}".format(f) for f in files)
	
	data = {}
	data['success'] = True
	data['filetext'] = filetext
	return JsonResponse(data)
	
def upload_files(upload_folder, FILES):
	files = []
	
	for f in FILES.getlist('files'):
		final_path = upload_folder + f.name
		
		if os.path.isfile(final_path):
			name, ext = os.path.splitext(f.name)
			num = 1
			
			while True:
				name_candidate = name + '-' + str(num) + ext
				
				if not os.path.isfile(upload_folder + name_candidate):
					break
				
				num = num + 1
				
			final_file_name = name_candidate
			final_path = upload_folder + final_file_name
		else:
			final_file_name = f.name 

		with open(final_path, 'wb') as dest:
			for chunk in f.chunks():
				dest.write(chunk)
		
		files.append(final_file_name)
	
	return files

class LoginView(View):
	def get(self, request):
		return render(request, 'blog/login.html', {
		})
	
	def post(self, request):
		'''
		Temporary Code
		
		user_queryset = User.objects(email=request.POST['email'])
		if user_queryset.count() > 0:
			user = user_queryset[0]
		else:
			return render(request, 'blog/login.html', {
				"error_message": "Email doesn't exist.",
			})
			
		django_user = authenticate(username=user.id, password=request.POST['password'])
		'''
		django_user = authenticate(username=request.POST['email'], password=request.POST['password'])
		
		if not django_user:
			return render(request, 'blog/login.html', {
				"error_message": "Password is not correct.",
			})
		else:
			login(request, django_user)
		
		if 'next' in request.GET:
			next = unquote(request.GET['next'])
		else:
			next = '/'	 
		
		return redirect(next)

class ContactView(View):
	def get(self, request):
		return render(request, "blog/contact.html", {
		})
	
	def post(self, request):
		errors = []
		required = [
				{'name':'title', 'error-message':'Title field should not be empty.'},
				{'name':'content', 'error-message':'Content field should not be empty.'},
				{'name':'email', 'error-message':'Email field should not be empty.'},
			]
		
		for r in required:
			if not request.POST[r['name']].strip():
				errors.append(r['error-message'])
		
		if len(errors) > 0:
			return render(request, "blog/contact.html", {
				"errors": errors,
			})
		
		django_send_mail(request.POST['title'], request.POST['content'], request.POST['email'], ['sainthkh@gmail.com'])
		
		return redirect(reverse("blog:contact-success"))

def contact_success(request):
	return render(request, "blog/contact-success.html", {
	})	

def product(request, slug):
	product = get_writing(Product, slug)
	return render(request, "blog/product.html", {
		'post': product,
		'content': process_content(product.content),
	})

def thank_you(request, slug):
	product = get_writing(Product, slug)
	return render(request, "blog/thank-you.html", {
		"product": product,
		'content': process_content(product.thank_you),
	})

def special_offer(request, slug):
	product = get_writing(Product, slug)
	return render(request, "blog/special-offer.html", {
		"product": product,
		"content": process_content(product.special_offer),
	})

def payment(request, slug):
	product = get_writing(Product, slug)
	stripe_pub_key = get_setting('stripe-public-key')
	return render(request, "blog/payment.html", {
		"product": product,
		"stripe_pub_key": stripe_pub_key,
	})

def configure_paypal_api():
	paypalrestsdk.configure({
		"mode": get_setting('paypal-mode'),
		"client_id": get_setting('paypal-client-id'),
		"client_secret": get_setting('paypal-client-secret'),
	})

def paypal_payment(request):
	configure_paypal_api()

	product = get_writing(Product, request.POST['slug'])
	
	order = create_order(request.POST['email'], 'paypal', product, status='pending')
	
	price = "{0}".format(product.price)
	payment = paypalrestsdk.Payment({
		"intent": "sale",
		"payer": {
			"payment_method": "paypal",
		},
		"transactions": [
			{
				"item_list": {
					"items": [
						{
							"name": product.title,
							"sku": product.slug,
							"price": price,
							"currency": "USD",
							"quantity": 1
						}
					]
				},
				"amount": {
					"total": price,
					"currency": "USD",
				},
				"description": "Thank you for your purchase"
			}
		],
		"redirect_urls": {
			"return_url": request.build_absolute_uri(reverse("blog:paypal-execute", kwargs={"order_id":str(order.number)})),
			"cancel_url": request.build_absolute_uri(reverse("blog:paypal-cancel", kwargs={"order_id":str(order.number)})),
		},
	})
	
	payment.create()
	
	for link in payment['links']:
		if link['rel'] == 'approval_url':
			url = link['href']
			break;
	
	order.paypal_payment_id = payment.id
	order.save()
	
	return redirect(url)

def paypal_execute(request, order_id):
	configure_paypal_api()

	order = Order.objects.get(paypal_payment_id=request.GET['paymentId'])
	order.status = 'complete'
	order.save()

	payment = paypalrestsdk.Payment.find(request.GET['paymentId'])
	payment.execute({"payer_id": request.GET['PayerID']})
	
	send_receipt(order, request)
	
	return redirect(reverse("blog:thank-you", kwargs={ "slug":order.product_slug }))
	
def paypal_cancel(request, order_id):
	configure_paypal_api()

	order = get_order(request.GET['paymentId'])
	order.status = 'cancel'
	order.save()
	
	return redirect('/')

def credit_card_payment(request):
	stripe.api_key = get_setting('stripe-private-key')

	product = get_writing(Product, request.POST['slug'])
	
	order = create_order(request.POST['email'], 'credit-card', product)
	
	try:
		charge = stripe.Charge.create(
			amount=int(product.price * 100), 
			currency="usd",
			source=request.POST['stripeToken'],
			description="Thank you for your purchase"
		)
	except stripe.error.CardError as e:
		pass
	
	send_receipt(order, request)
	
	return redirect(reverse("blog:thank-you", kwargs={ "slug": order.product_slug}))

def download_product(request, filename):
	if not "order-id" in request.GET or not "secret" in request.GET:
		raise Http404
	
	if Order.objects(number=request.GET['order-id']).count() < 0:
		raise Http404
	
	secret = request.GET['secret']
	correct_secret = create_download_secret(request.GET['order-id'], filename)
	if secret != correct_secret:
		raise Http404

	filename = unquote(filename)
	
	with open(django_setting.RESTRICTED_ROOT + filename, "rb") as f:
		name, ext = os.path.splitext(filename)
		content_types = {
			".mobi": "application/x-mobipocket-ebook",
			".epub": "application/epub+zip",
			".pdf": "application/PDF",
			".png": "image/png",
		}
		response = HttpResponse(f, content_type=content_types[ext.lower()])
		response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
	
	return response
	
# Email subscription

def newsletter(request):
	return render(request, "blog/newsletter.html", {
	})

def subscribe(request):
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
		
		send_to_subscriber(user.email, 'welcome', emaillist.slug, request)	
	
	# add list to subscriber
	if not emaillist.slug in user.subscribed_lists:
		user.subscribed_lists.append(emaillist.slug)
		user.save()
	
	# send lead magnet
	if emaillist.lead_magnet_slug.strip():
		send_to_subscriber(user.email,  emaillist.lead_magnet_slug, emaillist.slug, request)
	
	return redirect('blog:distribute-post', emaillist.thankyou_page)

def unsubscribe(request):
	if 'email' in request.GET:
		email = request.GET['email']
	else:
		email = ''
	
	if 'list-slug' in request.GET:
		list_slug = request.GET['list-slug']
	else:
		list_slug = ''
	
	return render(request, "blog/unsubscribe.html", {
		"email": email,
		"list_slug": list_slug,
	})

def unsubscribe_this(request):
	email = request.POST['email']
	list_slug = request.POST['list-slug']
		
	try:
		user = User.objects(email=email)[0]
	except IndexError:
		return render(request, "blog/error-page.html", {
			"error_message": "User doesn't exist."
		})
	
	try:
		user.subscribed_lists.remove(list_slug)
	except ValueError:
		pass
		
	user.save()
	
	return render(request, "blog/unsubscribed-successfully.html", {
		
	})
	
def unsubscribe_all(request):
	email = request.POST['email']
	
	try:
		user = User.objects(email=email)[0]
	except IndexError:
		return render(request, "blog/error-page.html", {
			"error_message": "User doesn't exist."
		})
	
	user.subscribed_lists = []
	user.save()
	
	return render(request, "blog/unsubscribed-successfully.html", {
		
	})
		
def test_landing_page(request):
	return render(request, "test/email-subscribe.html", {
		"slug": "test",
	})	

def sitemap(request, type_string=None):
	if not type_string:
		types = [Post, Page]
		last_mod_dates = []
		
		for t in types:
			writing = t.objects().order_by("-last_modified_date")[0:0]
			last_mod = writing[0].last_modified_date
			
			last_mod_dates.append(last_mod)
			
		return TemplateResponse(request, 'sitemap/main.xml', {
			"post_last_mod": last_mod_dates[0],
			"page_last_mod": last_mod_dates[1],
		}, content_type='application/xml')
	elif type_string == "legacy":
		posts = Post.objects(published_date__lte=date(2016, 2, 26)).order_by("-last_modified_date").only("slug", "last_modified_date")
		return TemplateResponse(request, 'sitemap/legacy.xml', {
			"writings" : posts,
			"url_name" : "blog:single-post-legacy",
			"changefreq": "never",
			"priority": "0.1",
		}, content_type='application/xml')
	else:
		types = {
			"post": { "class": Post, "url_name": 'blog:distribute-post'},
			"page": { "class": Page, "url_name": 'blog:distribute-post'},
		}
		
		return TemplateResponse(request, 'sitemap/type.xml', {
			"writings": types[type_string]["class"].objects.order_by("-last_modified_date").only("slug", "last_modified_date"),
			"url_name": types[type_string]["url_name"],
			"changefreq": "monthly",
			"priority": "0.2",
		}, content_type='application/xml')

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

#
# Save Comments
#
#################################################################

def save_comment(request, slug):
	comment = setup_comment(request)
	save_comment_to_db(comment, slug)
	
	return redirect('blog:distribute-post', slug=unquote(slug))

def save_comment_ajax(request, slug):
	response_data = {}

	if not (request.POST['name']).strip():
		response_data['success'] = False
		response_data['msg'] = 'Name should not be empty.'
	else:
		response_data['success'] = True
		comment = setup_comment(request)
		save_comment_to_db(comment, slug, is_spam(request))
		
		response_data['html'] = template_to_html('blog/comment.html', {
				"comment": comment,
			})

	return JsonResponse(response_data)