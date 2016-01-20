from django import template
from django.utils.safestring import mark_safe
from urllib.parse import quote, unquote
import mistune

from blog.urls.shortcuts import get_post_url_by_slug

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