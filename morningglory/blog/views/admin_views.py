from django.shortcuts import render, redirect
from blog.models import *
from datetime import datetime
from blog.utils import slugify
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