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
	url(r'^categories/(?P<slug>[%-_\w]+)(?:/page/(?P<page>[0-9]+))?$', views.category, name='category'),
	url(r'^series/(?P<slug>[%-_\w]+)/list(?:/page/(?P<page>[0-9]+))?$', views.series_list, name='series-list'),
	url(r'^series/(?P<slug>[%-_\w]+)$', views.series, name='series'),
	url(r'^rss$', LatestPostsFeed(), name='post-rss'),
	url(r'^feed$', LatestPostsFeed(), name='post-feed'),
	url(r'^email/signup$', views.email_signup, name="signup"),
	
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
	
	# posts
	url(r'^admin/posts', admin_views.post_list, name='admin-posts'),
	url(r'^admin/write-new-post', admin_views.write_new_post, name='write-new-post'),
	url(r'^admin/edit-post/(?P<slug>[%-_\w]+)', admin_views.edit_post, name='edit-post'),
	url(r'^admin/save-post', admin_views.save_post, name='save-post'),
	
	# series
	url(r'^admin/series', admin_views.series_list, name='admin-series'),
	url(r'^admin/write-new-series', admin_views.write_new_series, name='write-new-series'),
	url(r'^admin/edit-series/(?P<slug>[%-_\w]+)', admin_views.edit_series, name='edit-series'),
	url(r'^admin/save-series', admin_views.save_series, name='save-series'),
	
	# categories	
	url(r'^admin/categories', admin_views.category_list, name='admin-categories'),
	url(r'^admin/write-new-category', admin_views.write_new_category, name='write-new-category'),
	url(r'^admin/edit-category/(?P<slug>[%-_\w]+)', admin_views.edit_category, name='edit-category'),
	url(r'^admin/save-category', admin_views.save_category, name='save-category'),
	
	# activities
	url(r'^admin/activities$', admin_views.activities, name='admin-activities'),
	url(r'^admin/comments/approve/(?P<pos>[0-9]+)$', admin_views.approve_comment, name='admin-approve-comment'),
	
	# emails
	url(r'^admin/emails$', admin_views.emails, name='admin-emails'),
	url(r'^admin/write-new-email$', admin_views.write_new_email, name="write-new-email"),
	url(r'^admin/edit-email/(?P<slug>[%-_\w]+)$', admin_views.edit_email, name='edit-email'),
	url(r'^admin/save-email$', admin_views.save_email, name='save-email'),
	
	# email lists
	url(r'^admin/email-lists$', admin_views.email_lists, name='admin-email-lists'),
	url(r'^admin/email-list/(?P<slug>[%-_\w]+)$', admin_views.email_list_detail, name='admin-email-list'),
	url(r'^admin/add-new-email-list$', admin_views.add_new_email_list, name="add-new-email-list"),
	url(r'^admin/edit-email-list/(?P<slug>[%-_\w]+)$', admin_views.edit_email_list, name='edit-email-list'),
	url(r'^admin/save-email-list$', admin_views.save_email_list, name='save-email-list'),
	
	# settings
	url(r'^admin/settings', admin_views.settings, name='admin-settings'),
	url(r'^admin/save-settings', admin_views.save_settings, name='admin-save-settings'),
	
	# save comments
	url(r'^(?P<slug>[%-_\w]+)/comment$', admin_views.save_comment, name='save-comment'),
	url(r'^(?P<slug>[%-_\w]+)/comment/ajax$', admin_views.save_comment_ajax, name='save-comment'),
	
	#
	# post distributor.
	#
	################################################################
	url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]