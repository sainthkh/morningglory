from django.shortcuts import render, redirect
#from django.utils.text import slugify
from blog.models import *
from datetime import datetime
from blog.utils import slugify
from urllib.parse import quote, unquote
from blog.expanders import expand_content
from blog.urls.shortcuts import get_post_url_by_slug
from .utils import normalize_slug

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
	post_slug = slug
	post = Post.objects(slug=post_slug)
	return __view_single(request, post)

def category(request):
	pass

def category_paged(request):
	pass 

def series(request, slug):
	pass
	
def series_list(request, slug):
	pass
	
def series_list_paged(request, slug):
	pass
	
def distribute_post(request, slug):
	post = Post.objects.get(slug=normalize_slug(slug))
	
	if(post.post_type == "link"):
		return redirect(post.redirect_link)
	return __view_single(request, post)
	
def __view_single(request, post):
	share = {}
	share['title'] = quote(post.title)
	share['url'] = request.build_absolute_uri(quote(get_post_url_by_slug(post.slug)))
	comment_action = request.path + '/comment'
	return render(request, 'blog/single_post.html', {
			'post': post,
			'final_content': post.compiled_content,
			'share': share,
			'comment_action': comment_action,
		})