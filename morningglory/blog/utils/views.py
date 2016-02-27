from django.conf.urls import url
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import re
import hashlib

from urllib.parse import quote, unquote
from blog.models import *
from blog.utils import slugify
from datetime import datetime
from blog.expanders import template_to_html, expand_content, expand_image_tags

def normalize_slug(slug):
	if "%" not in slug:
		slug = quote(slug)
	
	return slug.lower()

def normalize_page(page):
	if not page:
		page = 1
	return int(page)

#
# Writing Helpers
# 
# These are common helper functions for writing types like Post, Series, Views 
#
##############################################################
def get_content(content_type, slug):
	try:
		content = content_type.objects(slug=normalize_slug(slug))[0]
	except IndexError:
		raise Http404

	return content	

def process_content(text):
	text = text.replace("\r\n", "\n")
	text = re.sub(r"([^\s])[ \t]*?\n[ \t]*?([^\s*])", r'\1  \n\2', text)
	text = expand_image_tags(expand_content(text))
	return text

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

def save_comment_to_db(comment, slug, spam):
	if not spam:
		activity = CommentActivity()
	else:
		activity = SpamCommentActivity()
	
	activity.comment = comment
	activity.date = comment.time
	
	post = get_content(Post, slug)
	activity.slug = slug
	activity.title = post.title
	
	activity.save()
	
	if not spam:
		post.comments.append(comment)
		post.save()	

def is_spam(request):
	from pykismet3 import Akismet
	import os
	
	a = Akismet(blog_url="http://wiseinit.com",
				user_agent="WiseInit System/0.0.1")

	a.api_key= get_setting('akismet')
	
	check = {
		'user_ip': request.META['REMOTE_ADDR'],
		'user_agent': request.META['HTTP_USER_AGENT'],
		'referrer': request.META.get('HTTP_REFERER', 'unknown'),
		'comment_content': request.POST['comment'],
		'comment_author': request.POST['name'],
	}
	
	if request.POST['email'].strip():
		check['comment_author_email'] = request.POST['email']
	
	if request.POST['website'].strip():
		website = request.POST['website'].strip()
		if website and not re.match('https?://.+', website):
			website = 'http://' + website
			
		check['comment_author_url'] = website
	
	return a.check(check)

#
# Email functions
#
###################################################################

def send_to_subscriber(address, email_slug, list_slug, request):
	e = get_content(Email, email_slug)
	content = template_to_html("blog/email-template.html", {
		"content": e.content,
		"email": address,
		"list_slug": list_slug,
		"request": request,
	})
	
	send_mail(address, e.title, content) 

def send_receipt(order, request):
	product = get_content(Product, order.product_slug)
	
	file_links = []
	for file in product.files:
		if not file.strip():
			continue
		
		quoted_filename = quote(file)
		url = "{0}?order-id={1}&secret={2}".format(
				request.build_absolute_uri(reverse("blog:download-product", kwargs={"filename": quoted_filename })),
				order.number,
				create_download_secret(order.number, quoted_filename)
			)
		link = {
			"name": file,
			"url": url,
		}
		file_links.append(link)
	
	content = template_to_html("admin/order/complete-email.html", {
		"product": product,
		"order": order,
		"file_links": file_links,
	})
	
	send_mail(order.email, 'Your Order is Complete' ,content)

def create_download_secret(order_id, filename):
	md5 = hashlib.md5()
	md5.update(settings.SECRET_KEY.encode('utf-8'))
	md5.update(str(order_id).encode('utf-8'))
	md5.update(filename.encode('utf-8'))
	md5.update('download'.encode('utf-8'))
	
	return md5.hexdigest()

def send_mail(address, title, content):
	message = EmailMessage(title, content, "WiseInit <info@wiseinit.com>",
			[address], [], reply_to=['sainthkh@gmail.com'])
	message.content_subtype = "html"
	message.send()

#
# Setting functions
#
##################################################################
def get_setting(name):
	if len(Setting.objects(name=name)) > 0:
		value = (Setting.objects(name=name)[0]).value
	else:
		value = ''
	
	return value

def save_setting(name, value):
	if len(Setting.objects(name=name)) > 0:
		setting = Setting.objects(name=name)[0]
	else:
		setting = Setting()
		setting.name = name
	
	setting.value = value
	setting.save()