from django.conf.urls import url
import blog.views as views
from blog.feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
	#
	# Front Pages
	#
	##################################################
	url(r'^$', views.index, name='index'),
	url(r'^blog$', views.list_post, name='list-post'),
	url(r'^page/(?P<page>[0-9]+)', views.list_post_paged, name='list-post-paged'),
	url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<date>[0-9]+)/(?P<slug>[%-_\w]+)/$', views.single_post, name='single-post-legacy'),
	url(r'^categories/(?P<slug>[%-_\w]+)(?:/page/(?P<page>[0-9]+))?$', views.category, name='category'),
	url(r'^series/(?P<slug>[%-_\w]+)/list(?:/page/(?P<page>[0-9]+))?$', views.series_list, name='series-list'),
	url(r'^series/(?P<slug>[%-_\w]+)$', views.series, name='series'),
	url(r'^upload-file$', views.upload_file, name='upload-file'),
	url(r'^rss$', LatestPostsFeed(), name='post-rss'),
	url(r'^feed$', LatestPostsFeed(), name='post-feed'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
	url(r'^store/(?P<slug>[%-_\w]+)$', views.product, name='product'),
	
	# email 
	url(r'^susbscribe$', views.subscribe, name="subscribe"),
	url(r'^unsubscribe$', views.unsubscribe, name="unsubscribe"),
	url(r'^unsubscribe-this$', views.unsubscribe_this, name="unsubscribe-this"),
	url(r'^unsubscribe-all$', views.unsubscribe_all, name="unsubscribe-all"),
	url(r'^test-landing-page$', views.test_landing_page, name="test-landing-page"),
	
	#
	# sitemap
	#
	############################################################
	url(r'^sitemap(?:\-(?P<type_string>[a-z]+))\.xml$', views.sitemap, name='sitemap'),
	
	#
	# Admin Pages.
	#
	##############################################################
	url(r'^admin$', views.dashboard, name='admin-dashboard'),
]

admin_views = [
	views.PostAdmin(),
	views.PageAdmin(),
	views.SeriesAdmin(),
	views.CategoryAdmin(),
	views.EmailAdmin(),
	views.EmailListAdmin(),
	views.LinkAdmin(),
	views.ProductAdmin(),
]

for admin_view in admin_views:
	urlpatterns += admin_view.urls()

urlpatterns = urlpatterns + [
	# activities
	url(r'^admin/activities$', views.activities, name='admin-activities'),
	url(r'^admin/comments/approve/(?P<pos>[0-9]+)$', views.approve_comment, name='admin-approve-comment'),
	
	# settings
	url(r'^admin/settings', views.settings, name='admin-settings'),
	url(r'^admin/save-settings', views.save_settings, name='admin-save-settings'),
	
	# save comments
	url(r'^(?P<slug>[%-_\w]+)/comment$', views.save_comment, name='save-comment'),
	url(r'^(?P<slug>[%-_\w]+)/comment/ajax$', views.save_comment_ajax, name='save-comment'),
	
	#
	# post distributor.
	#
	################################################################
	url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]