from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap
from blog import views

sitemaps = {
    "blog": BlogSitemap
}

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog$', views.list_post, name='list-post'),
    url(r'^page/(?P<page>[0-9]+)', views.list_post_paged, name='list-post-paged'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<date>[0-9]+)/(?P<slug>[-_\w]+)/$', views.single_post, name='single-post'),
    url(r'^categories/(?P<slug>[%-_\w]+)/$', views.category, name='category'),
    url(r'^categories/(?P<slug>[%-_\w]+)/page/(?P<page>[0-9]+)$', views.category_paged, name='category-paged'),
	url(r'^series/(?P<slug>[%-_\w]+)$', views.series, name='series'),
	url(r'^series/(?P<slug>[%-_\w]+)/list$', views.series_list, name='series-list'),
    url(r'^series/(?P<slug>[%-_\w]+)/list/page/(?P<page>[0-9]+)$', views.series_list_paged, name='series-list-paged'),
	
    #sitemap
    url(r'^sitemap.xml$', sitemap, { "sitemaps": sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
    
    # Admin Pages.
    url(r'^admin/write-new-post', views.write_new_post, name='write-new-post'),
    url(r'^admin/save-post', views.save_post, name='save-post'),
    url(r'^admin/edit-post/(?P<slug>[%-_\w]+)', views.edit_post, name='edit-post'),
    
    url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]