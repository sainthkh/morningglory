from django import template
from django.core.urlresolvers import reverse
from blog.models import *
from blog.utils import random_string

register = template.Library()

@register.inclusion_tag('admin/post/select.html')
def select_series(post):
	current_series = ''
	
	if isinstance(post, Post):
		current_series = post.series_slug
		
	series_list = Series.objects.only("title", "slug")
	
	return {
		"current_series": current_series,
		"series_list": series_list,
	}

@register.inclusion_tag('admin/series/select.html')
def select_category(series):
	current = ''
	
	if isinstance(series, Series):
		current = series.category_slug
		
	series_list = Category.objects.only("title", "slug")
	
	return {
		"current_series": current,
		"category_list": series_list,
	}

@register.inclusion_tag('admin/upload-button.html')
def upload_button(name, folder='uploads', multiple=True, text_target="writing-content"):
	target_urls = {
		"uploads": reverse('blog:upload-file'),
		"restricted": reverse('blog:upload-to-restricted'),
	}
	
	return {
		"id": random_string(16),
		"target_url": target_urls[folder],
		"text_target": text_target,
		"multiple": multiple,
		"name": name,
	}
