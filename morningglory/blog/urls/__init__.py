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
	#
	# Front Pages
	#
	##################################################
	url(r'^$', views.index, name='index'),
	url(r'^blog$', views.list_post, name='list-post'),
	url(r'^page/(?P<page>[0-9]+)', views.list_post_paged, name='list-post-paged'),
	url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<date>[0-9]+)/(?P<slug>[-_\w]+)/$', views.single_post, name='single-post'),
	url(r'^categories/(?P<slug>[%-_\w]+)/$', views.category, name='category'),
	url(r'^categories/(?P<slug>[%-_\w]+)/page/(?P<page>[0-9]+)$', views.category_paged, name='category-paged'),
	url(r'^series/(?P<slug>[%-_\w]+)/list(/page/(?P<page>[0-9]+))?$', views.series_list, name='series-list'),
	url(r'^series/(?P<slug>[%-_\w]+)$', views.series, name='series'),
	url(r'^rss$', LatestPostsFeed(), name='post-rss'),
	url(r'^feed$', LatestPostsFeed(), name='post-feed'),
	
	#
	# sitemap
	#
	############################################################
	url(r'^sitemap.xml$', sitemap, { "sitemaps": sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
	
	#
	# Admin Pages.
	#
	##############################################################
	url(r'^admin$', admin_views.dashboard, name='admin-dashboard'),
	
	url(r'^admin/posts', admin_views.post_list, name='admin-posts'),
	url(r'^admin/write-new-post', admin_views.write_new_post, name='write-new-post'),
	url(r'^admin/edit-post/(?P<slug>[%-_\w]+)', admin_views.edit_post, name='edit-post'),
	url(r'^admin/save-post', admin_views.save_post, name='save-post'),
	
	url(r'^admin/series', admin_views.series_list, name='admin-series'),
	url(r'^admin/write-new-series', admin_views.write_new_series, name='write-new-series'),
	url(r'^admin/edit-series/(?P<slug>[%-_\w]+)', admin_views.edit_series, name='edit-series'),
	url(r'^admin/save-series', admin_views.save_series, name='save-series'),
	
	url(r'^admin/categories', admin_views.category_list, name='admin-categories'),
	
	url(r'^admin/activities$', admin_views.activities, name='admin-activities'),
	url(r'^admin/comments/approve/(?P<pos>[0-9]+)$', admin_views.approve_comment, name='admin-approve-comment'),
	
	url(r'^admin/settings', admin_views.settings, name='admin-settings'),
	url(r'^admin/save-settings', admin_views.save_settings, name='admin-save-settings'),
	
	url(r'^(?P<slug>[%-_\w]+)/comment$', admin_views.save_comment, name='save-comment'),
	url(r'^(?P<slug>[%-_\w]+)/comment/ajax$', admin_views.save_comment_ajax, name='save-comment'),
	
	#
	# post distributor.
	#
	################################################################
	url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]