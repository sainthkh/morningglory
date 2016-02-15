from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings

from urllib.parse import quote, unquote
import mistune
import math

from blog.utils.urls import get_post_url_by_slug
from blog.models import *
from blog.expanders import template_to_html

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

@register.simple_tag(takes_context=True)
def unsubscribe_url(context, email, list_slug):
	request = context['request']
	url = request.build_absolute_uri(reverse('blog:unsubscribe'))
	return "{0}?email={1}&list-slug={2}".format(url, quote(email), quote(list_slug))

@register.simple_tag()
def google_analytics():
	if settings.DEBUG:
		return ''
	return template_to_html('blog/google-analytics.html', {})

@register.simple_tag(takes_context=True)
def absolute_url(context, url):
	return context['request'].build_absolute_uri(url)
	
@register.simple_tag(takes_context=True)
def absolute_url_reverse(context, url_name, slug):
	return context['request'].build_absolute_uri(reverse(url_name, kwargs={"slug":slug}))
	
@register.simple_tag(takes_context=True)
def absolute_url_legacy(context, url_name, slug, date):
	return context['request'].build_absolute_uri(reverse(url_name, kwargs={
		"slug": slug, 
		"year": str(date.year),
		"month": str(date.month),
		"date": str(date.day), 
		}))

@register.simple_tag
def uploads(filename):
	return '/uploads/' + filename
	
@register.inclusion_tag('blog/blog-categories.html')
def blog_categories():
	categories = Category.objects(slug__in=['words', 'grammar', '5%eb%b6%84-%ed%95%9c%ea%b5%ad%ec%96%b4'])
	
	category_list = []
	for c in categories:
		cat = {
			"category": c,
			"series": Series.objects(category_slug=c.slug), 
		}
		category_list.append(cat)
	return {
		"categories": category_list,
	}