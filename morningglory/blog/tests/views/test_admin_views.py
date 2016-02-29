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

			('/admin/page', 'admin-page'),
			('/admin/add-new-page', 'add-new-page'),
			('/admin/edit-page/1as2322', 'edit-page'),
			('/admin/trash-page/ask-you', 'trash-page'),
			('/admin/delete-page/goo123-asf', 'delete-page'),
			
			('/admin/series', 'admin-series'),
			('/admin/add-new-series', 'add-new-series'),
			('/admin/edit-series/1as2322', 'edit-series'),
			('/admin/trash-series/ask-you', 'trash-series'),
			('/admin/delete-series/goo123-asf', 'delete-series'),
			
			('/admin/category', 'admin-category'),
			('/admin/add-new-category', 'add-new-category'),
			('/admin/edit-category/1as2322', 'edit-category'),
			('/admin/trash-category/ask-you', 'trash-category'),
			('/admin/delete-category/goo123-asf', 'delete-category'),
			
			('/admin/email', 'admin-email'),
			('/admin/add-new-email', 'add-new-email'),
			('/admin/edit-email/1as2322', 'edit-email'),
			('/admin/trash-email/ask-you', 'trash-email'),
			('/admin/delete-email/goo123-asf', 'delete-email'),
			
			('/admin/email-list', 'admin-email-list'),
			('/admin/add-new-email-list', 'add-new-email-list'),
			('/admin/edit-email-list/1as2322', 'edit-email-list'),
			('/admin/trash-email-list/ask-you', 'trash-email-list'),
			('/admin/delete-email-list/goo123-asf', 'delete-email-list'),
			
			('/admin/link', 'admin-link'),
			('/admin/add-new-link', 'add-new-link'),
			('/admin/edit-link/1as2322', 'edit-link'),
			('/admin/trash-link/ask-you', 'trash-link'),
			('/admin/delete-link/goo123-asf', 'delete-link'),
			
			('/admin/product', 'admin-product'),
			('/admin/add-new-product', 'add-new-product'),
			('/admin/edit-product/1as2322', 'edit-product'),
			('/admin/trash-product/ask-you', 'trash-product'),
			('/admin/delete-product/goo123-asf', 'delete-product'),
		]
		'''
			Saved for future tests
			('/admin/[type]', 'admin-[type]'),
			('/admin/add-new-[type]', 'add-new-[type]'),
			('/admin/edit-[type]/1as2322', 'edit-[type]'),
			('/admin/trash-[type]/ask-you', 'trash-[type]'),
			('/admin/delete-[type]/goo123-asf', 'delete-[type]'),
		'''
	
		self.run_tests(test_set, get_url_name)
	
	def test__MessageGroupAdmin_get_line_type__stars__return_new_message_string(self):
		test_set = [
			("*", "end message"),
			("**", "end message"),
			("*****", "end message"),
			("*******", "end message"),
			("**************", "end message"),
			("*******************", "end message"),
		]
		
		a = MessageGroupAdmin()
		
		self.run_tests(test_set, a.get_line_type)
	
	def test__MessageGroupAdmin_get_line_type__image_tag__return_images_string(self):
		test_set = [
			("<-image->", "images"),
			("<-----image--->", "images"),
			("<-------image--------->", "images"),
			("<--image-->", "images"),
			("<--------------image-->", "images"),
			("<---image------------------------->", "images"),
			
		]
		
		a = MessageGroupAdmin()
		
		self.run_tests(test_set, a.get_line_type)
	
	def test__MessageGroupAdmin_get_line_type__other_string__return_text_string(self):
		test_set = [
			("aasdfaaa", "text"),
			("* this is test", "text"),
			("<---test---->", "text"),
			("***** good! *****", "text"),			
		]
		
		a = MessageGroupAdmin()
		
		self.run_tests(test_set, a.get_line_type)
	
	def text_example(self):
		return ("Hello, World!\n"
			"Good to see you again\n"
			"<-----image----->\n"
			"/uploads/image1.jpg\n"
			"/uploads/img-awesome.png\n"
			"****************\n"
			"Second Message #2nd \n"
		)
	
	def test__MessageGroupAdmin_messages__messages_correct_format__correct_message_count(self):
		text = self.text_example() 
		
		a = MessageGroupAdmin()
		
		self.assertEqual(len(a.messages(text)), 2)
	
	def test__MessageGroupAdmin_messages__messages_correct_format__correct_message_text(self):
		text = self.text_example() 
		
		a = MessageGroupAdmin()
		m = a.messages(text)
		
		self.assertEqual(m[0].text, "Hello, World!\nGood to see you again")
		self.assertEqual(m[1].text, "Second Message #2nd \n")
	
	def test__MessageGroupAdmin_messages__messages_correct_format__correct_images_count(self):
		text = self.text_example() 
		
		a = MessageGroupAdmin()
		m = a.messages(text)
		
		self.assertEqual(len(m[0].images), 2)
		self.assertEqual(len(m[1].images), 0)
			
	def test__MessageGroupAdmin_messages__messages_correct_format__correct_images_path(self):
		text = self.text_example() 
		
		a = MessageGroupAdmin()
		m = a.messages(text)
		
		self.assertEqual(m[0].images[0], "/uploads/image1.jpg")
		self.assertEqual(m[0].images[1], "/uploads/img-awesome.png")
		