from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from blog.models import *
from data.models import *

from morningglory import settings
from datetime import datetime
import os
import re

def to_markdown(content):
	def extract_image_name(m):
		path, file_name = os.path.split(m.group(1))
		return "($ {0} $)".format(file_name)
	
	def extract_link(m):
		return "[{0}]({1})".format(m.group(2), m.group(1))

	content = re.sub(r"<h1>(.*?)</h1>", r"\n# \1", content)
	content = re.sub(r"<h2>(.*?)</h2>", r"\n# \1", content)
	content = re.sub(r"<h3>(.*?)</h3>", r"\n# \1", content)
	content = re.sub(r'<img(?:.*?)src="(.*?)"(?:.*?)/?>', extract_image_name, content)
	content = re.sub(r'<a(?:.*?)href="(.*?)"(?:.*?)>(.*?)</a>', extract_link, content)
	
	return content
	

class Command(BaseCommand):
	def handle(self, *arg, **options):
		print("Start Migration")
		
		if settings.DEBUG:
			print("Dropping current documents")
			Post.drop_collection()
			Category.drop_collection()
			Series.drop_collection()
			Comment.drop_collection()
		
		print("Started migration posts...")
		
		wp_pages =  WpPosts.objects.using('wpdb').filter(post_status='publish', post_type='page')
		
		for wp_post in wp_posts:
			page = Page()
			page.slug = wp_post.post_name
			page.published_date = wp_post.post_date
			page.last_modified_date = wp_post.post_modified
			page.title = wp_post.post_title
			page.content = to_markdown(wp_post.post_content)
			
			page.save()
		
		print("Ended migrating posts.")
		
		print("Started migration pages...")
		
		wp_posts =  WpPosts.objects.using('wpdb').filter(post_status='publish', post_type='post')
		
		for wp_post in wp_posts:
			post = Post()
			post.slug = wp_post.post_name
			post.published_date = wp_post.post_date
			post.last_modified_date = wp_post.post_modified
			post.title = wp_post.post_title
			post.content = to_markdown(wp_post.post_content)
			
			post.save()
		
		print("Ended migrating pages.")
		
		print("Started migrating comments...")
		
		wp_comments = WpComments.objects.using('wpdb').filter(comment_type='')
		
		for wp_comment in wp_comments:
			comment = Comment()
			comment.name = wp_comment.comment_author
			comment.email = wp_comment.comment_author_email
			comment.website = wp_comment.comment_author_url
			comment.time = wp_comment.comment_date
			comment.content = wp_comment.comment_content
			
			wp_post = WpPosts.objects.using('wpdb').get(id=wp_comment.comment_post_id)
			post = Post.objects.get(slug=wp_post.post_name)
			post.comments.append(comment)
			post.save()
		
		print("Ended migrating comments.")
		
		print("Started migrating categories...")
		
		wp_categories = WpTermTaxonomy.objects.using('wpdb').filter(taxonomy='category', parent=0)
		category_slugs = {}
		
		for wp_category in wp_categories:
			wp_term = WpTerms.objects.using('wpdb').get(term_id=wp_category.term_id)
			category = Category()
			category.slug = wp_term.slug
			category.title = wp_term.name
			category.save()
			
			category_slugs[wp_term.term_id] = category.slug
		
		print("Ended migrating categories.")
		
		print("Started migrating series...")
		
		wp_series_list = WpTermTaxonomy.objects.using('wpdb').filter(taxonomy='category').exclude(parent=0)
		series_slugs = {}
		
		for wp_series in wp_series_list:
			wp_term = WpTerms.objects.using('wpdb').get(term_id=wp_series.term_id)
			series = Series()
			series.slug = wp_term.slug
			series.title = wp_term.name
			series.category_slug = category_slugs[wp_series.parent]
			series.save()
			
			series_slugs[wp_term.term_id] = series.slug
		
		print("Ended migrating series.")
		
		print("Started migrating post-series relationship...")
		
		term_rels = WpTermRelationships.objects.using('wpdb').all()
		
		for term_rel in term_rels:
			wp_post = WpPosts.objects.using('wpdb').get(id=term_rel.object_id)
			if wp_post.post_type != 'post':
				continue
			post = Post.objects(slug=wp_post.post_name)
			
			if post.count() == 0:
				continue
			else:
				post = post[0]
			
			if term_rel.term_taxonomy_id in series_slugs.keys():
				post.series_slug = series_slugs[term_rel.term_taxonomy_id]
			
			post.save()
		
		series = Series()
		series.slug = 'etc'
		series.title = 'etc'
		series.save()
		
		Post.objects(series_slug='').update(series_slug='etc')
		
		print("Ended migrating post-series relationship.")
		
		print("End Migration")