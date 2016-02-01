from django.conf.urls import url
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from urllib.parse import quote, unquote
from blog.models import *
from blog.utils import slugify
from datetime import datetime
from blog.expanders import template_to_html

def normalize_slug(slug):
	if "%" not in slug:
		slug = quote(slug)
	
	return slug

#
# Writing Helpers
# 
# These are common helper functions for writing types like Post, Series, Views 
#
##############################################################

def setup_writing_for_save(writing_type, request):
	add_new = request.POST['add-new'] == "True"
	writing = get_writing(writing_type, request.POST["slug"], add_new)
	setup_dates(writing, add_new)
	
	if add_new:
		writing.slug = create_slug(writing_type, request.POST["title"]) 
	
	setup_basic_content(writing, request.POST)
	
	return writing

def get_writing(writing_type, slug, add_new=False):
	if add_new:
		writing = writing_type()
	else:
		try:
			writing = writing_type.objects(slug=normalize_slug(slug))[0]
		except IndexError:
			raise Http404

	return writing

def setup_dates(writing, add_new):
	if add_new:
		writing.published_date = writing.last_modified_date = datetime.now()
	else:
		writing.last_modified_date = datetime.now()

def create_slug(writing_type, title):
	slug_base = slugify(title)
	final_slug = slug_base
	exist = writing_type.objects(slug=slug_base).count() != 0

	if exist:
		num = 1
		while True:
			slug_candidate = slug_base + '-' + str(num)
			exist = writing_type.objects(slug=slug_candidate).count() != 0
			if not exist:
				break
			num = num + 1
		final_slug = slug_candidate
	
	return final_slug	

def setup_basic_content(writing, POST):
	if 'title' in POST and POST['title'].strip():
		writing.title = POST['title']

	if 'content' in POST and POST['content'].strip():
		writing.content = POST['content']

	if 'excerpt' in POST and POST['excerpt'].strip():
		writing.excerpt = POST['excerpt']

	if 'key-points' in POST and POST['key-points'].strip():
		writing.key_points = POST['key-points']			

#
# Admin class
#
###################################################################

class Admin:	
	def __init__(self, writing, name):
		self.writing = writing
		self.name = name
		slug = name.lower().replace(' ', '-')
		
		self.__setup_paths(slug)
	
	def __setup_paths(self, slug):
		self.t = {} # short for templates
		
		# list 
		self.t['list-url'] = r"^admin/{0}$"
		self.t['list-file-path'] = 'admin/{0}/list.html'
		self.t['list-name'] = "admin-{0}"
		
		# add-new & edit
		self.t['add-new-url'] = r"^admin/add-new-{0}$"
		self.t['write-file-path'] = 'admin/{0}/write.html'
		self.t['add-new-name'] = 'add-new-{0}'
		self.t['edit-url'] = r"^admin/edit-{0}/(?P<slug>[%-_\w]+)$"
		self.t['edit-name'] = 'edit-{0}'
		
		# save
		self.t['save-url'] = r"admin/save-{0}$"
		self.t['save-name'] = "save-{0}"
		self.t['save-redirect'] = 'blog:edit-{0}'
		
		for k, v in self.t.items():
			self.t[k] = v.format(slug)			  
	
	def urls(self):
		u = [
			url(self.t['list-url'], login_required(self.list), name=self.t['list-name']),
			url(self.t['add-new-url'], login_required(self.add_new), name=self.t['add-new-name']),
			url(self.t['edit-url'], login_required(self.edit), name=self.t['edit-name']),
			url(self.t['save-url'], login_required(self.save), name=self.t['save-name']),
		]
		
		return u
		
	def list(self, request):
		writings = self.writing.objects
		
		context = {
			"writings": writings,
			"url_name": 'blog:{0}'.format(self.t['edit-name']),
		}
		
		context.update(self.list_context(request))
		
		return render(request, self.t['list-file-path'], context)
	
	def add_new(self, request):
		context = {
			"page_title" : "Add New " + self.name,
			"add_new": True,
		}
		context.update(self.add_new_context(request))
		
		return render(request, self.t['write-file-path'], context)
	
	def edit(self, request, slug):
		writing = get_writing(self.writing, slug)
		
		context = {
			"writing": writing,
			"page_title": "Edit {0} : {1}".format(self.name, writing.title),
			"add_new": False,
		}
		context.update(self.edit_context(request))
		
		return render(request, self.t['write-file-path'], context)
	
	def save(self, request):
		writing = setup_writing_for_save(self.writing, request)
		self.save_others(writing, request.POST)
		writing.save()
		
		return redirect(self.t['save-redirect'], slug=unquote(writing.slug))
	
	def save_others(self, writing, POST):
		pass
		
	def list_context(self, request):
		return {}
	
	def add_new_context(self, request):
		return {}
	
	def edit_context(self, request):
		return {}
#
# Comment Savers. 
#
#############################################################

def setup_comment(request):
	comment = Comment()
	comment.name = request.POST['name']
	comment.email = request.POST['email']
	comment.website = request.POST['website'].strip()
	if comment.website != '' and re.match('https?://.+', comment.website) == None:
		comment.website = 'http://' + comment.website
	comment.content = request.POST['comment']
	comment.time = datetime.now()
	return comment

def save_comment_to_db(comment, slug):
	spam = is_spam(comment.name, comment.content)
	if not spam:
		activity = CommentActivity()
	else:
		activity = SpamCommentActivity()
	
	activity.comment = comment
	activity.date = comment.time
	
	post = Post.objects(slug=slug)[0]
	activity.slug = slug
	activity.title = post.title
	
	activity.save()
	
	if not spam:
		post.comments.append(comment)
		post.save()	

def is_spam(content, author):
	if settings.DEBUG:
		return False
		
	from pykismet3 import Akismet
	import os
	
	a = Akismet(blog_url="http://wiseinit.com",
				user_agent="WiseInit System/0.0.1")

	a.api_key= Secret.objects(name='akismet')[0].key
	
	return a.check({'user_ip': os.environ['REMOTE_ADDR'],
			'user_agent': os.environ['HTTP_USER_AGENT'],
			'referrer': os.environ.get('HTTP_REFERER', 'unknown'),
			'comment_content': content,
			'comment_author': author,
		})

#
# Email functions
#
###################################################################

def send_mail(slug, addr, request, list_slug):
	e = get_writing(Email, slug)
	content = template_to_html("blog/email-template.html", {
		"content": e.content,
		"email": addr,
		"list_slug": list_slug,
		"request": request,
	})
	message = EmailMessage(e.title, content, "WiseInit <info@wiseinit.com>",
			[addr], [], reply_to=['sainthkh@gmail.com'])
	message.content_subtype = "html"
	message.send()