from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from urllib.parse import unquote
from datetime import datetime

from blog.models import *
from blog.utils.views import *
from blog.utils.models import *


class AdminViewBase:
	def __init__(self, writing_type, name):
		self.writing_type = writing_type
		self.name = name
		slug = name.lower().replace(' ', '-')
		
		self.__setup_paths(slug)
		
		self.trash_menu = {"name": "Trash", "url_name": 'blog:' + self.t['trash-name']}
	
	def __setup_paths(self, slug):
		self.t = {} # t is short for templates
		
		# list 
		self.t['list-url'] = r"^admin/{0}(?:/page/(?P<page>[0-9]+))?$"
		self.t['list-file-path'] = 'admin/{0}/list.html'
		self.t['list-name'] = "admin-{0}"
		self.t['list-redirect'] = 'blog:' + self.t['list-name']
		
		# add-new & edit
		self.t['add-new-url'] = r"^admin/add-new-{0}$"
		self.t['write-file-path'] = 'admin/{0}/write.html'
		self.t['add-new-name'] = 'add-new-{0}'
		self.t['edit-url'] = r"^admin/edit-{0}/(?P<slug>[%-_\w]+)$"
		self.t['edit-name'] = 'edit-{0}'
		self.t['save-redirect'] = 'blog:' + self.t['edit-name']
		
		# trash
		self.t['trash-url'] = r"^admin/trash-{0}/(?P<slug>[%-_\w]+)$"
		self.t['trash-name'] = 'trash-{0}'
		
		# delete
		self.t['delete-url'] = r"^admin/delete-{0}/(?P<slug>[%-_\w]+)$"
		self.t['delete-name'] = 'delete-{0}'
			
		for k, v in self.t.items():
			self.t[k] = v.format(slug)			  
	
	def urls(self):
		u = [
			url(self.t['list-url'], login_required(self.list), name=self.t['list-name']),
			url(self.t['add-new-url'], login_required(self.add_new), name=self.t['add-new-name']),
			url(self.t['edit-url'], login_required(self.edit), name=self.t['edit-name']),
			url(self.t['trash-url'], login_required(self.trash), name=self.t['trash-name']),
			url(self.t['delete-url'], login_required(self.delete), name=self.t['delete-name']),
		]
		
		return u
		
	def list(self, request, page=1):
		page = normalize_page(page)
		writings = self.page(page)
		
		context = {
			"writings": writings,
			"url_name": 'blog:{0}'.format(self.t['edit-name']),
			"page_context": {
				"count": self.writing_type.objects.count(),
				"current": page,
				"url-name": self.t['list-redirect'],
				"document-per-page": 20,
			},
			"menu_context": self.menu_context(),
		}
		
		context.update(self.list_context(request, context))
		
		return render(request, self.t['list-file-path'], context)
	
	def add_new(self, request):
		if request.method == "GET":
			return self.add_new_get(request)
		elif request.method == "POST":
			return self.add_new_post(request)
	
	def edit(self, request, slug):
		if request.method == "GET":
			return self.edit_get(request, slug)
		elif request.method == "POST":
			return self.edit_post(request, slug)
	
	def trash(self, request, slug):
		writing = self.get(slug)
		writing.status = 'trash'
		writing.save()
		
		return redirect(self.t['list-redirect'])
		
	def delete(self, request, slug):
		writing = self.get(slug)
		self.delete_or_alter_related(request, writing)
		
		writing.delete()
		return redirect(self.t['list-redirect'])
	
	def add_new_get(self, request):
		context = {
			"page_title" : "Add New " + self.name,
			"add_new": True,
		}
		context.update(self.add_new_context(request, context))
		
		return render(request, self.t['write-file-path'], context)
	
	def edit_get(self, request, slug):
		writing = self.get(slug)
		
		context = {
			"writing": writing,
			"add_new": False,
		}
		
		if hasattr(writing, 'title'):
			context["page_title"] = "Edit {0} : {1}".format(self.name, writing.title) 
		
		context.update(self.edit_context(request, context))
		
		return render(request, self.t['write-file-path'], context)
	
	def add_new_post(self, request):
		return self.handle_post(request, add_new=True)
	
	def edit_post(self, request, slug):
		return self.handle_post(request, add_new=False)
	
	def handle_post(self, request, add_new):
		errors = self.check_errors(request)
		writing = self.construct(request)
		
		if len(errors) == 0:
			writing.save()
			return redirect(self.t['save-redirect'], slug=unquote(writing.slug))
		else:
			return render(request, self.t['write-file-path'], {
				"errors": errors,
				"writing": writing,
				"add_new": add_new, 
			})
	
	def check_errors(self, request):
		errors = []
		
		if not request.POST['title'].strip():
			errors.append("Title should not be empty.")
		
		return errors
	
	def construct(self, request):
		add_new = request.POST['add-new'] == "True"
	
		if add_new:
			writing = self.writing_type()
			writing.published_date = writing.last_modified_date = datetime.now()
		else:
			writing = self.get(request.POST["slug"])

		if add_new and not 'slug' in request.POST:
			writing.slug = self.create_slug(request.POST["title"]) 

		self.setup_basic_content(writing, request.POST)
		self.construct_other_contents(writing, request.POST)
		
		return writing
	
	def get(self, slug):
		return get_writing(self.writing_type, slug)
	
	def create_slug(self, title, writing_type=None):
		if not writing_type:
			writing_type = self.writing_type 

		slug_base = slugify(title)
		final_slug = slug_base
		exist = writing_type.objects(slug=slug_base).count() != 0

		if exist:
			num = 1
			while True:
				slug_candidate = slug_base + '-' + str(num)
				exist = writing_type.objects(slug=slug_candidate).count() != 0
				if not exist:
					break
				num = num + 1
			final_slug = slug_candidate

		return final_slug
	
	def primary_level_slug(self, title):
		return self.create_slug(title, PrimarySlug)
	
	def setup_basic_content(self, writing, POST):
		if 'title' in POST:
			writing.title = POST['title']

		if 'content' in POST:
			writing.content = POST['content']

		if 'excerpt' in POST:
			writing.excerpt = POST['excerpt']

		if 'key-points' in POST:
			writing.key_points = POST['key-points']		
	
	def page(self, page):
		return self.writing_type.objects(status__ne='trash')[(page-1)*20:page*20]
	
	def construct_other_contents(self, writing, POST):
		pass
		
	def list_context(self, request, context):
		return {}
	
	def menu_context(self):
		return []
	
	def add_new_context(self, request, context):
		return {}
	
	def edit_context(self, request, context):
		return {}
	
	def delete_or_alter_related(self, request, writing):
		pass

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

class PostAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Post, 'Post')

	def list_context(self, request, context):
		return {
			"writings": context["writings"].order_by("-published_date")
		}
	
	def menu_context(self):
		return [
			self.trash_menu,
			{"name": "View", "url_name": 'blog:distribute-post', "new":True },
		]
	
	def construct_other_contents(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = self.primary_level_slug(POST['title'])
			
		writing.series_slug = POST['series']

class PageAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Page, 'Page')
	
	def menu_context(self):
		return [
			self.trash_menu,
			{"name": "View", "url_name": 'blog:distribute-post', "new":True },
		]
	
	def construct_other_contents(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = self.primary_level_slug(POST['title'])

		writing.layout = POST['layout']

class SeriesAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Series, 'Series')
	
	def menu_context(self):
		return [
			self.trash_menu,
			{"name": "View", "url_name": 'blog:series-list', "new":True },
		]
	
	def contstruct_other_contents(self, writing, POST):
		writing.category_slug = POST['category']
	
	def delete_or_alter_related(self, request, writing):
		Post.objects(series_slug=writing.slug).update(series_slug='etc')
	

class CategoryAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Category, 'Category')
	
	def menu_context(self):
		return [
			self.trash_menu,
			{"name": "View", "url_name": 'blog:category', "new":True },
		]
	
	def delete_or_alter_related(self, request, writing):
		Series.objects(category_slug=writing.slug).update(category_slug='etc')

class EmailAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Email, 'Email')
	
	def menu_context(self):
		return [
			self.trash_menu,
		]

class EmailListAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, EmailList, 'Email List')
	
	def menu_context(self):
		return [
			self.trash_menu,
		]
	
	def contstruct_other_contents(self, writing, POST):
		writing.lead_magnet_slug = POST['lead-magnet-slug']
		writing.thankyou_page = POST['thankyou-page']

class LinkAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Link, 'Link')
	
	def menu_context(self):
		return [
			self.trash_menu,
		]
	
	def edit_context(self, request):
		return {
			"page_title": "Edit Link",
		}
	
	def contstruct_other_contents(self, writing, POST):
		if POST['add-new'] == 'True':
			writing.slug = primary_level_slug(POST['slug'])
		
		writing.url = POST['url']

class ProductAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, Product, 'Product')
	
	def menu_context(self):
		return [
			self.trash_menu,
			{"name": "View", "url_name": 'blog:product', "new":True },
		]
	
	def add_new_context(self, request):
		writing = {
			"files": ['', '', '', '', ''],
		}
		
		return {
			"writing": writing,
		}
	
	def contstruct_other_contents(self, writing, POST):
		writing.thank_you = POST['thank-you']
		writing.price = float(POST['price'])
		writing.thumbnail = POST['thumbnail']
		
		writing.files = []
		for i in range(0, 5):
			filename = POST['filename-' + str(i)].strip()
			writing.files.append(filename)

class UserAdmin(AdminViewBase):
	def __init__(self):
		AdminViewBase.__init__(self, User, 'User')
	
	def menu_context(self):
		return [
			self.trash_menu,
		]
	
	def list_context(self, request, context):
		return {
			"users": context["writings"]
		}
	
	def add_new_context(self, request, context):
		return {
			"user": context["writing"]
		}
		
	def edit_context(self, request, context):
		return {
			"user": context["writing"]
		}
	
	def get(self, email):
		try:
			return User.objects.get(email=unquote(email))
		except:
			raise Http404
	

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
def activities(request, page):
	page = normalize_page(page)
	document_per_page = 50
	
	activities = Activity.objects.order_by("-date")[document_per_page*(page-1):document_per_page*page]
	return render(request, 'admin/activities.html', {
		"activities": activities,
		"page_context": {
			"count": Activity.objects.count(),
			"current": page,
			"url-name": "blog:admin-activities",
			"document-per-page": document_per_page,
		}
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
