from django.conf.urls import url
import blog.views as views
import blog.views.admin_views as admin_views
from blog.feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
	#
	# Front Pages
	#
	##################################################
	url(r'^$', views.index, name='index'),
	url(r'^blog(?:/page/(?P<page>[0-9]+))$', views.blog_main, name='blog-main'),
	url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<date>[0-9]+)/(?P<slug>[%-_\w]+)/$', views.single_post, name='single-post-legacy'),
	url(r'^categories/(?P<slug>[%-_\w]+)(?:/page/(?P<page>[0-9]+))?$', views.category, name='category'),
	url(r'^series/(?P<slug>[%-_\w]+)/list(?:/page/(?P<page>[0-9]+))?$', views.series_list, name='series-list'),
	url(r'^series/(?P<slug>[%-_\w]+)$', views.series, name='series'),
	url(r'^admin/upload-file$', views.upload_file, name='upload-file'),
	url(r'^rss$', LatestPostsFeed(), name='post-rss'),
	url(r'^feed$', LatestPostsFeed(), name='post-feed'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
	url(r'^contact$', views.ContactView.as_view(), name='contact'),
	url(r'^contact-success$', views.contact_success, name='contact-success'),
	
	#
	# Store
	#
	################################################################
	url(r'^store/(?P<slug>[%-_\w]+)/thank-you$', views.thank_you, name='thank-you'),
	url(r'^store/(?P<slug>[%-_\w]+)/special-offer$', views.special_offer, name='special-offer'),
	url(r'^store/(?P<slug>[%-_\w]+)$', views.product, name='product'),
	url(r'^payment/m/paypal/execute/(?P<order_id>\d+)$', views.paypal_execute, name='paypal-execute'),
	url(r'^payment/m/paypal/cancel/(?P<order_id>\d+)$', views.paypal_cancel, name='paypal-cancel'),
	url(r'^payment/m/paypal$', views.paypal_payment, name='paypal-payment'),
	url(r'^payment/m/credit-card$', views.credit_card_payment, name='credit-card-payment'),	
	url(r'^payment/(?P<slug>[%-_\w]+)$', views.payment, name='payment'),
	url(r'^admin/upload-to-restricted$', views.upload_to_restricted, name='upload-to-restricted'),
	url(r'^download/(?P<filename>[%-_.\w]+)$', views.download_product, name='download-product'),
	
	
	#
	# email
	#
	################################################################# 
	url(r'^newsletter$', views.newsletter, name='newsletter'),
	url(r'^susbscribe$', views.subscribe, name="subscribe"),
	url(r'^unsubscribe$', views.unsubscribe, name="unsubscribe"),
	url(r'^unsubscribe-this$', views.unsubscribe_this, name="unsubscribe-this"),
	url(r'^unsubscribe-all$', views.unsubscribe_all, name="unsubscribe-all"),
	url(r'^admin/send-test-mail$', views.send_test_mail, name="send-test-mail"),
	url(r'^admin/send-mail-now$', views.send_mail_now, name="send-mail-now"),
	url(r'^test-landing-page$', views.test_landing_page, name="test-landing-page"),
	
	#
	# sitemap
	#
	############################################################
	url(r'^sitemap(?:\-(?P<type_string>[a-z]+))?\.xml$', views.sitemap, name='sitemap'),
	
	#
	# Admin Pages.
	#
	##############################################################
	url(r'^admin$', views.admin_views.dashboard, name='admin-dashboard'),
]

admin_views_classes = [
	admin_views.PostAdmin(),
	admin_views.PageAdmin(),
	admin_views.SeriesAdmin(),
	admin_views.CategoryAdmin(),
	admin_views.EmailAdmin(),
	admin_views.EmailListAdmin(),
	admin_views.LinkAdmin(),
	admin_views.ProductAdmin(),
	admin_views.UserAdmin(),
	admin_views.MessageLoopAdmin(),
	admin_views.MessageGroupAdmin(),
]

for admin_view in admin_views_classes:
	urlpatterns += admin_view.urls()

urlpatterns = urlpatterns + [
	url(r'^admin/add-new-subscriber', admin_views.AddSubscriber.as_view(), name='add-new-subscriber'),
	
	# activities
	url(r'^admin/activities(?:/page/(?P<page>[0-9]+))?$', admin_views.activities, name='admin-activities'),
	url(r'^admin/comments/approve/(?P<pos>[0-9]+)$', admin_views.approve_comment, name='admin-approve-comment'),
	
	# settings
	url(r'^admin/settings', admin_views.settings, name='admin-settings'),
	url(r'^admin/save-settings', admin_views.save_settings, name='admin-save-settings'),
	
	# order
	url(r'^admin/order', admin_views.admin_order, name='admin-order'),
	
	# save comments
	url(r'^(?P<slug>[%-_\w]+)/comment$', views.save_comment, name='save-comment'),
	url(r'^(?P<slug>[%-_\w]+)/comment/ajax$', views.save_comment_ajax, name='save-comment'),
	
	#
	# post distributor.
	#
	################################################################
	url(r'^(?P<slug>[%-_\w]+)', views.distribute_post, name='distribute-post'),
]