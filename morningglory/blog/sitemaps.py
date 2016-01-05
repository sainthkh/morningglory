from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.core.urlresolvers import reverse

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.2

    def items(self):
        return Post.objects()

    def lastmod(self, obj):
        return obj.last_modified_date
        
    def location(self, obj):
        return reverse('blog:distribute-post', kwargs={"slug" : obj.slug})
    
