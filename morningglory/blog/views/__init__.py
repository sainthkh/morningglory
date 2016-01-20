from django.shortcuts import render, redirect
from blog.models import *
from datetime import datetime
from blog.utils import slugify, template_to_html
from urllib.parse import quote, unquote
from blog.expanders import expand_content

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

def category(request):
	pass

def category_paged(request):
	pass 

def series(request, slug):
	series = get_writing(Series, slug)
	return render(request, "blog/series.html", {
		"series" : series,
	})
	
def series_list(request, slug):
	return render(request, "blog/series-list.html", {
		
	})
	
def series_list_paged(request, slug):
	pass
	
def distribute_post(request, slug):
	post = get_writing(Post, slug)
	
	if(post.post_type == "link"):
		return redirect(post.redirect_link)
	return __view_single(request, post)
	
def __view_single(request, post):
	return render(request, 'blog/single-post.html', {
			'post': post,
			'final_content': post.compiled_content,
		})