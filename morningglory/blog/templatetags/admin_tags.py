from django import template
from blog.models import *

register = template.Library()

@register.inclusion_tag('blog-admin/select-series.html')
def select_series(post):
	current_series = ''
	
	if isinstance(post, Post):
		current_series = post.series_slug
		
	series_list = Series.objects.only("title", "slug")
	
	return {
		"current_series": current_series,
		"series_list": series_list,
	}