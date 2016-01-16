from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from blog.urls.shortcuts import get_post_url_by_slug
from .models import Post

class LatestPostsFeed(Feed):
	title = 'WiseInit Korean'
	link = '/blog'
	description = 'New posts of WiseInit Korean. '

	def items(self):
		return Post.objects[:5]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return truncatewords(item.content, 30)

	def item_link(self, item):
		return get_post_url_by_slug(item.slug)