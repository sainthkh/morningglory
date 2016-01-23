from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog.models import *
from blog.models.email_models import *
from blog.utils import template_to_html
from urllib.parse import unquote
from blog.expanders import expand_content
from .utils import *

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
	return render(request, 'blog-admin/writing/write-post.html', {
		"page_title" : "Add New Post"
	})

def edit_post(request, slug):
	post = get_writing(Post, slug)

	return render(request, 'blog-admin/writing/write-post.html', {
		"writing": post,
		"page_title": "Edit Post : " + post.title
	})

def save_post(request):
	post = setup_writing_for_save(Post, request)
	setup_extra_fields(post, request)
	post.compiled_content = expand_content(post.content)
	post.post_type = 'post'
	post.series_slug = request.POST['series']
	post.save()
	
	return redirect('blog:edit-post', slug=unquote(post.slug))

#
# Series Views
#
################################################################

def series_list(request):
	return render(request, 'blog-admin/writing/series.html', {
		
	})

def write_new_series(request):
	return render(request, 'blog-admin/writing/write-series.html', {
		"page_title": "Add New Series",
	})

def edit_series(request, slug):
	series = get_writing(Series, slug)
	return render(request, 'blog-admin/writing/write-series.html', {
		"writing": series, 
		"page_title": "Edit Series: " + series.title,
	})
	
def save_series(request):
	series = setup_writing_for_save(Series, request)
	setup_extra_fields(series, request)
	series.save()

	return redirect('blog:edit-series', slug=unquote(series.slug))

#
# Category Views
#
##############################################################

def category_list(request):
	return render(request, 'blog-admin/writing/category.html', {
		
	})

def write_new_category(request):
	return render(request, 'blog-admin/writing/write-category.html', {
		"page_title": "Add New Category",
		"hide_extra": True, 
	})

def edit_category(request, slug):
	category = get_writing(Category, slug)
	return render(request, 'blog-admin/writing/write-category.html', {
		"writing": category, 
		"page_title": "Edit Category: " + category.title,
		"hide_extra": True,
	})
	
def save_category(request):
	category = setup_writing_for_save(Category, request)
	category.save()

	return redirect('blog:edit-category', slug=unquote(category.slug))

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
# Email Views
#
#################################################################

def emails(request):
	emails = Email.objects
	return render(request, "blog-admin/email/emails.html", {
		"emails": emails,
	})

def write_new_email(request):
	return render(request, "blog-admin/email/write-email.html", {
		"page_title": "Write New Email",
	})

def edit_email(request, slug):
	email = get_writing(Email, slug)
	return render(request, "blog-admin/email/write-email.html", {
		"page_title": "Edit Email: " + email.title,
		"writing": email,
	})

def save_email(request):
	email = setup_writing_for_save(Email, request)
	email.save()
	return redirect('blog:edit-email', slug=email.slug)

#
# Email List Views
#
#################################################################

def email_lists(request):
	email_lists = EmailList.objects
	return render(request, "blog-admin/email/email-lists.html", {
		"email_lists": email_lists,
	})

def email_list_detail(request):
	pass

def add_new_email_list(request):
	pass
	
def edit_email_list(request):
	pass
	
def save_email_list(request):
	pass

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