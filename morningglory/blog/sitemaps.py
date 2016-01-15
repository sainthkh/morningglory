from django.contrib.sitemaps import Sitemap
from blog.models import Post
from blog.urls.shortcuts import get_post_url_by_slug

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.2

    def items(self):
        return Post.objects()

    def lastmod(self, obj):
        return obj.last_modified_date
        
    def location(self, obj):
        return get_post_url_by_slug(obj.slug)
    
