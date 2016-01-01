from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog$', views.list_post, name='list_post'),
    url(r'^page/(?P<page>[0-9]+)', views.list_post_paged, name='list_post_paged'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<date>[0-9]+)/(?P<slug>[-_\w]+)/$', views.single_post, name='single_post'),
    url(r'^categories/(?P<slug>[-_\w]+)/$', views.category, name='category'),
    url(r'^categories/(?P<slug>[-_\w]+)/page/(?P<page>[0-9]+)$', views.category_paged, name='category_paged'),
    
    # Admin Pages.
    url(r'^admin/write-new-post', views.write_new_post, name='write-new-post'),
    url(r'^admin/save-post', views.save_post, name='save-post'),
    url(r'^admin/edit-post/(?P<id>[0-9]+)', views.edit_post, name='edit-post'),
]