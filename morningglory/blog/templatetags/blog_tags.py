from django import template
from django.utils.safestring import mark_safe
import mistune

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
	r = mistune.Renderer(escape=False)
	markdown = mistune.Markdown(renderer=r)
	return markdown(text)
