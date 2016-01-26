from django import template
from django.utils.safestring import mark_safe
from urllib.parse import quote, unquote
import mistune
import math

from blog.utils.urls import get_post_url_by_slug
from blog.models import *

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
	r = mistune.Renderer(escape=False)
	markdown = mistune.Markdown(renderer=r)
	return markdown(text)

@register.inclusion_tag('blog/share.html', name="share", takes_context=True)
def share_div(context, writing):
	request = context['request']

	share = {}
	share['title'] = quote(writing.title)
	share['url'] = request.build_absolute_uri(quote(get_post_url_by_slug(writing.slug)))
	
	return {
		"share": share
	}

@register.simple_tag(takes_context=True)
def comment_action(context):
	return context['request'].path + '/comment'

@register.inclusion_tag('blog/pagination.html', takes_context=True)
def pagination(context, slug, page):
	page_count = math.ceil(Post.objects(series_slug=slug).count() / 5)
	pager = {
		"current": page,
		"slug": slug,
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


@register.inclusion_tag('blog/email-modal.html')
def email_modal(slug, popup_button="Download Now", title="Free Offer", 
	message="", submit="Give me RIGHT NOW"):
	pass

@register.inclusion_tag('blog/email-form.html')
def email_form(slug):
	return {
		"slug": slug,
	}