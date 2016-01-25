from django.test import TestCase
from django.core.urlresolvers import resolve

class UrlTest(TestCase):
	def test__urls__url__correct_view_name(self):
		test_set = [
			('/admin/series', 'blog:admin-series'),
		]
		
		self.run_tests(test_set)
	
	def test__urls__url__correct_view_path(self):
		
				
	def run_tests(self, test_set):
		for t in test_set:
			with self.subTest(input=t[0]):
				result = resolve(t[0])
				self.assertEqual(result.view_name, t[1])