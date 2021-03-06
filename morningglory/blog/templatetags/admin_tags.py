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
		
	category_list = Category.objects.only("title", "slug")
	
	return {
		"current": current,
		"category_list": category_list,
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

@register.inclusion_tag('admin/content-menu.html')
def content_menu(menu_context, slug):
	return {
		"menu_context": menu_context,
		"slug": slug,
	}

@register.filter
def comma_list(l):
	return ', '.join(l)

@register.inclusion_tag('admin/template_tags/horizontal-input.html', name='horizontal')
def horizontal_input(name, value, slug=''):
	if slug == '':
		slug = name.lower().replace(' ', '-')
	
	return {
		"name": name,
		"slug": slug,
		"value": value,
	}