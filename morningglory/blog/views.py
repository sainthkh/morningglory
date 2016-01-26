from django.shortcuts import render, redirect
from blog.models import *
from datetime import datetime
from blog.utils import slugify, template_to_html
from urllib.parse import quote, unquote
from blog.expanders import expand_content
from blog.utils.views import *

from .utils import *
import re

# Create your views here.

def index(request):
	dummy = {
		"category" : [
			{"link" : '/', "name" : 'RM Words' }
		],
		"link" : '/',
		"title" : '5 Words in RM 3000',
	}
	return render(request, 'blog/index.html', {
		"post" : dummy,
	})

def list_post(request):
	pass
   
def list_post_paged(request):
	pass

def single_post(request, year, month, date, slug):
	post = get_writing(Post, slug)
	return __view_single(request, post)

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
	posts = Post.objects(series_slug=slug)[(page-1)*5:page*5]
	return render(request, "blog/series-list.html", {
		"posts": posts,
		"slug" : slug,
		"page" : page,
	})

def distribute_post(request, slug):
	post = get_writing(Post, slug)
	
	if(post.post_type == "link"):
		return redirect(post.redirect_link)
	return __view_single(request, post)
	
def __view_single(request, post):
	return render(request, 'blog/single-post.html', {
			'post': post,
		})

# Email subscription

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
		
		send_mail('welcome', user.email, request, emaillist.slug)	
	
	# add list to subscriber
	if not emaillist.slug in user.subscribed_lists:
		user.subscribed_lists.append(emaillist.slug)
		user.save()
	
	# send lead magnet
	send_mail(emaillist.lead_magnet_slug, user.email, request, emaillist.slug)
	
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
	pass
	
def unsubscribe_all(request):
	pass	

def test_landing_page(request):
	return render(request, "test/email-subscribe.html", {
		"slug": "test",
	})	
# Admin Views

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
	
	def save_others(self, writing, POST):
		writing.compiled_content = expand_content(writing.content)
		writing.post_type = 'post'
		writing.series_slug = POST['series']

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

#
# Activity Views
#
##############################################################

def activities(request):
	activities = Activity.objects
	return render(request, 'admin/activities.html', {
		"activities": activities,
	})

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
	
def settings(request):
	if len(Secret.objects(name='akismet')) > 0:
		akismet_key = (Secret.objects(name='akismet')[0]).key
	else:
		akismet_key = ''
		
	return render(request, 'admin/settings.html', {
		"akismet_key": akismet_key,
	})
	
def save_settings(request):
	if len(Secret.objects(name='akismet')) > 0:
		secret = Secret.objects(name='akismet')[0]
	else:
		secret = Secret()
		secret.name = 'akismet'
	
	secret.key = request.POST['akismet-key']
	secret.save()
	
	return redirect('blog:admin-settings')

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
		save_comment_to_db(comment, slug)
		response_data['html'] = template_to_html('blog/comment.html', {
				"comment": comment,
			})

	return JsonResponse(response_data)