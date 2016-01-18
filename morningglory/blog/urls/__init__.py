from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap
import blog.views as views
from blog.views import admin_views
from blog.feeds import LatestPostsFeed

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
	url(r'^rss$', LatestPostsFeed(), name='post-rss'),
	url(r'^feed$', LatestPostsFeed(), name='post-feed'),
	
	#sitemap
	url(r'^sitemap.xml$', sitemap, { "sitemaps": sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
	
	# Admin Pages.
	url(r'^admin/$', admin_views.dashboard, name='admin-dashboard'),
	url(r'^admin/posts', admin_views.post_list, name='admin-posts'),
	url(r'^admin/write-new-post', admin_views.write_new_post, name='write-new-post'),
	url(r'^admin/series', admin_views.series_list, name='admin-series'),
	url(r'^admin/categories', admin_views.category_list, name='admin-categories'),
	url(r'^admin/save-post', admin_views.save_post, name='save-post'),
	url(r'^admin/edit-post/(?P<slug>[%-_\w]+)', admin_views.edit_post, name='edit-post'),
	
	# post distributor.
	url(r'^(?P<slug>[%-_\w]+)/comment$', views.save_comment, name='save-comment'),
	url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]