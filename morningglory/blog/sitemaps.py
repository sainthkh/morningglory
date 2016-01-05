from django.contrib.sitemaps import Sitemap
from blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.2

    def items(self):
        return Post.objects()

    def lastmod(self, obj):
        return obj.pub_date
    
