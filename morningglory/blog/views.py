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

def email_signup(request):
	pass
	
def distribute_post(request, slug):
	post = get_writing(Post, slug)
	
	if(post.post_type == "link"):
		return redirect(post.redirect_link)
	return __view_single(request, post)
	
def __view_single(request, post):
	return render(request, 'blog/single-post.html', {
			'post': post,
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

class CategoryAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Category, 'Category')

class EmailAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, Email, 'Email')

class EmailListAdmin(Admin):
	def __init__(self):
		Admin.__init__(self, EmailList, 'Email List')

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