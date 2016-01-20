from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog.models import *
from datetime import datetime
from blog.utils import slugify, template_to_html
from urllib.parse import quote, unquote
from blog.expanders import expand_content
from blog.urls.shortcuts import get_post_url_by_slug
from .utils import normalize_slug

# Create your views here.
def dashboard(request):
	return render(request, 'blog-admin/dashboard.html', {
	})

#
# Post Views
#
###########################################################

def post_list(request):
	pass

def write_new_post(request):
	empty = {
		"slug": "",
		"title": "",
		"content": "",
	}
	return render(request, 'blog-admin/write-post.html', {
		"post" : empty,
		"page_title" : "Add New Post"
	})

def edit_post(request, slug):
	posts = Post.objects(slug=normalize_slug(slug))
	post = posts[0]

	return render(request, 'blog-admin/write-post.html', {
		"writing": post,
		"page_title": "Edit Post : " + post.title
	})

def save_post(request):
	post = setup_writing_for_save(Post, request)
	post.compiled_content = expand_content(post.content)
	post.post_type = 'post'
	post.save()
	
	return redirect('blog:edit-post', slug=unquote(post.slug))

#
# Series Views
#
################################################################

def series_list(request):
	pass

def write_new_series(request):
	return render(request, 'blog-admin/write-series.html', {
		"page_title": "Add New Series",
	})

def edit_series(request, slug):
	series = Series.objects(slug=normalize_slug(slug))[0]
	return render(request, 'blog-admin/write-series.html', {
		"writing": series, 
		"page_title": "Edit Series: " + series.title,
	})
	
def save_series(request):
	series = setup_writing_for_save(Series, request)
	series.save()

	return redirect('blog:edit-series', slug=unquote(series.slug))

#
# Category Views
#
##############################################################

def category_list(request):
	pass

#
# Writing Helpers
# 
# These are common helper functions for writing types like Post, Series, Views 
#
##############################################################

def setup_writing_for_save(writing_type, request):
	writing = get_writing(writing_type, request.POST["slug"])
	is_edit = request.POST['slug'] != ""
	setup_dates(writing, is_edit)
	
	if not is_edit:
		writing.slug = create_slug(writing_type, request.POST["title"]) 
	
	setup_basic_content(writing, request.POST)
	
	return writing

def get_writing(writing_type, slug):
	if slug != "":
		writing = writing_type.objects(slug=slug)[0]
	else:
		writing = writing_type()
	return writing

def setup_dates(writing, is_edit):
	if is_edit:
		writing.last_modified_date = datetime.now()
	else:
		writing.published_date = writing.last_modified_date = datetime.now()

def create_slug(writing_type, title):
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
		final_slug = slug_candidate
	
	return final_slug	

def setup_basic_content(writing, POST):
	writing.title = POST['title']
	writing.content = POST['content']
	writing.excerpt = POST['excerpt']
	writing.key_points = POST['key-points']

#
# Activity Views
#
##############################################################

def activities(request):
	activities = Activity.objects
	return render(request, 'blog-admin/activities.html', {
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
		
	return render(request, 'blog-admin/settings.html', {
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
	comment = __setup_comment(request)
	__save_comment(comment, slug)
	
	return redirect('blog:distribute-post', slug=unquote(slug))

def save_comment_ajax(request, slug):
	response_data = {}

	if not (request.POST['name']).strip():
		response_data['success'] = False
		response_data['msg'] = 'Name should not be empty.'
	else:
		response_data['success'] = True
		comment = __setup_comment(request)
		__save_comment(comment, slug)
		response_data['html'] = template_to_html('blog/comment.html', {
				"comment": comment,
			})

	return JsonResponse(response_data)

def __setup_comment(request):
	comment = Comment()
	comment.name = request.POST['name']
	comment.email = request.POST['email']
	comment.website = request.POST['website'].strip()
	if comment.website != '' and re.match('https?://.+', comment.website) == None:
		comment.website = 'http://' + comment.website
	comment.content = request.POST['comment']
	comment.time = datetime.now()
	return comment

def __save_comment(comment, slug):
	spam = is_spam(comment.name, comment.content)
	if not spam:
		activity = CommentActivity()
	else:
		activity = SpamCommentActivity()
	
	activity.comment = comment
	activity.date = comment.time
	
	post = Post.objects(slug=slug)[0]
	activity.slug = slug
	activity.title = post.title
	
	activity.save()
	
	if not spam:
		post.comments.append(comment)
		post.save()	

def is_spam(content, author):
	from pykismet3 import Akismet
	import os
	
	a = Akismet(blog_url="http://wiseinit.com",
				user_agent="WiseInit System/0.0.1")

	a.api_key=""
	
	return a.check({'user_ip': os.environ['REMOTE_ADDR'],
			'user_agent': os.environ['HTTP_USER_AGENT'],
			'referrer': os.environ.get('HTTP_REFERER', 'unknown'),
			'comment_content': content,
			'comment_author': author,
		})
	