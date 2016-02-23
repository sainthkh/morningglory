from django import template
from django.core.urlresolvers import reverse
from django.conf import settings

from urllib.parse import quote, unquote
import math
import re

from blog.utils.urls import get_post_url_by_slug
from blog.utils.markdown import *
from blog.models import *
from blog.expanders import template_to_html
from .common_tags import pager

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
	r = Renderer(escape=False)
	markdown = Markdown(renderer=r)
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
	return '/uploads/' + quote(str(filename))
	
@register.inclusion_tag('blog/blog-categories.html')
def blog_categories():
	categories = [
		{'title':'Words', 'slug':'words'}, 
		{'title':'Grammar', 'slug':'grammar'}, 
		{'title':'5분 한국어', 'slug':'5%eb%b6%84-%ed%95%9c%ea%b5%ad%ec%96%b4'},
		{'title':'Entertainment', 'slug':'entertainment'},
	]
	
	category_list = []
	for c in categories:
		cat = {
			"category": c,
			"series": Series.objects(category_slug=c['slug']), 
		}
		category_list.append(cat)
	return {
		"categories": category_list,
	}

@register.inclusion_tag('blog/writing-summary.html')
def writing_summary(writing):
	return {
		"writing": writing,
	}

@register.filter
def remove_tags(content):
	content = re.sub(r"<.*?>", r"", content)
	content = re.sub(r"\(\$.*?\$\)", '', content)
	return content

@register.filter
def remove_audio_headline(content):
	content = re.sub(r"# Korean Only", r'', content)
	content = re.sub(r"# With English( Translations)?", r'', content)
	return content

@register.filter
def simpleformat(value, arg):
	return value.format(arg)

@register.filter(name='unquote')
def unquote_url(value):
	return unquote(value)