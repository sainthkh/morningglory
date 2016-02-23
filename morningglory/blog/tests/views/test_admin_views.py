from django.core.urlresolvers import resolve

from blog.tests.base import MorningGloryTestCase
from blog.views.admin_views import *

class TestAdminViews(MorningGloryTestCase):
		
	def test__urls__given_url__correct_name(self):
		def get_url_name(url):
			r = resolve(url)
			return r.url_name
		
		test_set = [
			('/admin/post', 'admin-post'),
			('/admin/add-new-post', 'add-new-post'),
			('/admin/edit-post/12322', 'edit-post'),
			('/admin/trash-post/ask', 'trash-post'),
			('/admin/delete-post/goo123-asf', 'delete-post'),
			
			#('/admin/page', 'admin-page'),
			#('/admin/add-new-page', 'add-new-page'),
		]
	
		self.run_tests(test_set, get_url_name)