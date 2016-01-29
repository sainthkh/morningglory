import re
import os
from django.template.context import Context
from blog.utils import template_to_html

expanders = {}

tag_regex = r"<<([a-zA-Z0-9\-]+)>>(.*?)<</\1>>"

def expand_content(content):
	return re.sub(tag_regex, expander, content, flags=re.M|re.S)
	
def expander(m):
	tag = m.group(1)
	content = m.group(2)
	if tag in expanders:
		f = expanders[tag]
		content = f(content)
	return content
	
def add_custom_tag(tag_name, tag_func):
	expanders[tag_name] = tag_func

def remove_custom_tag(tag_name):
	expanders.pop(tag_name)

def example_template(content):
	return template_to_html('expander/example.html', {"content" : content})

def eye_catch_template(content):
	return template_to_html('expander/eye-catch.html', {"content": content})

add_custom_tag("example", example_template)
add_custom_tag("eye-catch", eye_catch_template)

def expand_image_tags(content):
	return re.sub(r"(\$(.*?)\$)", expand_image, content, flags=re.M|re.S)
	
def expand_image(m):
	file = m.group(1)
	filename = os.path.splitext(file)
	return '<img src="{0}" alt="{1}" >'.format(file, filename)