from django import template
from django.core.urlresolvers import reverse

import math

register = template.Library()

@register.inclusion_tag('common/pagination.html')
def pagination(page_context):
	page_count = math.ceil(page_context["count"] / page_context["document-per-page"])
	context = pager(page_count, page_context["current"])
	kwargs = {
		"page": "1002346871238491771293841234981112430987097234189", #dummy number that might not occur
	}
	if "slug" in page_context:
		kwargs["slug"] = page_context["slug"]
	
	context["url_format"] = reverse(page_context["url-name"], kwargs=kwargs).replace(kwargs["page"], "{0}")
	return context

def pager(page_count, page):
	pager = {
		"current": page,
	}
	
	if page_count <= 10:
		page_range = range(1, page_count+1)
	else:
		if page < 6:
			pager["next_page"] = 11
			page_range = range(1, 11)
		else:
			pager["previous_page"] = page - 5
			
			if page_count > page + 5:
				pager["next_page"] = page + 6
				page_range = range(page - 4, page + 6)
			else:
				page_range = range(page - 4, page_count + 1)
	
	pager["range"] = page_range
	return pager

@register.filter
def simpleformat(value, arg):
	return value.format(arg)