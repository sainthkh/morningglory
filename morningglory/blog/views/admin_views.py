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

def post_list(request):
	pass

def series_list(request):
	pass

def category_list(request):
	pass

def write_new_post(request):
	empty = {
		"slug": "",
		"title": "",
		"content": "",
	}
	return render(request, 'blog-admin/write.html', {
		"post" : empty,
		"page_title" : "Add New Post"
	})

def comments(request):
	comments = Comment.objects
	return render(request, 'blog-admin/comments.html', {
		"page_title": "Comments",
		"comments" : comments
	})

def spam_comments(request):
	return render(request, 'blog-admin/comments.html', {
		"page_title": "Spam Comments",
	})
	
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

def edit_post(request, slug):
	posts = Post.objects(slug=normalize_slug(slug))
	post = posts[0]

	return render(request, 'blog-admin/write.html', {
		"post": post,
		"page_title": "Edit Post : " + post.title
	})

def save_post(request):
	if (request.POST['slug'] != ""):
		post = Post.objects(slug=request.POST['slug'])[0] 
		post.last_modified_date = datetime.now()
	else:
		post = Post()
		post.published_date = datetime.now()
		post.last_modified_date = post.published_date
		slug_base = slugify(request.POST['title'])
		print(Post.objects(slug=slug_base).count())
		exist = Post.objects(slug=slug_base).count() != 0
		if exist:
			num = 1
			while True:
				final_slug = slug_base + '-' + str(num)
				exist = Post.objects(slug=final_slug).count() != 0
				if not exist:
					break
			post.slug = final_slug
		else:
			post.slug = slug_base        
			  
	
	post.title = request.POST['title']
	post.content = request.POST['content']
	post.compiled_content = expand_content(request.POST['content'])
	post.post_type = 'post'
	post.excerpt = request.POST['excerpt']
	post.key_points = request.POST['key-points']
	post.save()
	
	return redirect('blog:edit-post', slug=unquote(post.slug))

def save_comment(request, slug):
	return redirect('blog:distribute-post', slug=unquote(slug))

def save_comment_ajax(request, slug):
	response_data = {}

	if not (request.POST['name']).strip():
		response_data['success'] = False
		response_data['msg'] = 'Name should not be empty.'
	else:
		response_data['success'] = True
		comment = __save_comment(request, slug)
		response_data['html'] = template_to_html('blog/comment.html', {
				"comment": comment,
				"pending": True,
			})

	return JsonResponse(response_data)

def __save_comment(request, slug):
	comment = Comment()
	comment.name = request.POST['name']
	comment.email = request.POST['email']
	comment.website = request.POST['website'].strip()
	if comment.website != '' and re.match('https?://.+', comment.website) == None:
		comment.website = 'http://' + comment.website
	comment.content = request.POST['comment']
	comment.time = datetime.now()
	comment.status = 'pending'
	comment.post_slug = slug
	comment.save()
	return comment

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
			'is_test': 1,
		})
	