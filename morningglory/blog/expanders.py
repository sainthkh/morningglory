import re
from django.template.loader import get_template 
from django.template.context import Context

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

def template_to_html(file, context):
	t = get_template(file)
	return t.render(context)

def example_template(content):
	return template_to_html('expander/example.html', {"content" : content})

add_custom_tag("example", example_template)