from django.test import TestCase
from blog.templatetags.blog_tags import *

import re

class TagTest(TestCase):				
	def run_tests(self, test_set, f):
		for t in test_set:
			with self.subTest(input=t[0]):
				result = f(t[0])
				self.assertEqual(result, t[1])
	
	def test__markdown_format__test_test__correct_html(self):
		test_set = [
			("Hi   \nWorld\n  \t\nI am C.", "<p>Hi<br>\nWorld</p>\n<p>I am C.</p>\n"),
			# iframe test
			('<iframe id="audio_iframe" src="http://test.com"></iframe>\r\n\r\n# Hello\r\n\r\n<iframe id="audio_iframe" src="http://test2.com"></iframe>', 
				'<p><iframe id="audio_iframe" src="http://test.com"></iframe></p>\n<h1>Hello</h1>\n<p><iframe id="audio_iframe" src="http://test2.com"></iframe></p>\n'),
			('# Hello World\n\nThis is your world', '<h1>Hello World</h1>\n<p>This is your world</p>\n'),
			('# Hello\r\n\r\n<iframe id="audio_iframe" src="http://test2.com"></iframe>',
				'<h1>Hello</h1>\n<p><iframe id="audio_iframe" src="http://test2.com"></iframe></p>\n'),
			("# What is in this Book?\n\n30 useful idioms  \n90+ example sentences  \n150+ Korean word definitions  \n90+ practice sentences\n\n",
				"<h1>What is in this Book?</h1>\n<p>30 useful idioms<br>\n90+ example sentences<br>\n150+ Korean word definitions<br>\n90+ practice sentences</p>\n"),
			('<a href="/payment/korean-idioms" class="btn btn-buy btn-lg"><i class="fa fa-shopping-cart"></i>  Buy Now</a>\n\n# What is in this Book?\n\n30 useful idioms  \n90+ example sentences  \n150+ Korean word definitions  \n90+ practice sentences\n\n',
				'<p><a href="/payment/korean-idioms" class="btn btn-buy btn-lg"><i class="fa fa-shopping-cart"></i>  Buy Now</a></p>\n<h1>What is in this Book?</h1>\n<p>30 useful idioms<br>\n90+ example sentences<br>\n150+ Korean word definitions<br>\n90+ practice sentences</p>\n')
		]
		
		self.run_tests(test_set, markdown_format)
	
	def test__markdown_heading_regex__not_None(self):
		test_set = [
			'<iframe id="audio_iframe" src="http://test.com"></iframe>\r\n\r\n# Hello\r\n\r\n<iframe id="audio_iframe" src="http://test2.com"></iframe>',
			'# Hello\r\n\r\n<iframe id="audio_iframe" src="http://test2.com"></iframe>',
			'<iframe id="audio_iframe" src="http://test.com"></iframe>\r\n\r\n# Hello',
			'<p>Hi</p>\r\n# Hello',
			'# Hello World',
			'# Hello World\n\nThis is your world',
		]
		
		for t in test_set:
			with self.subTest(input=t):
				m = re.search(r'(?:\n|^) *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)', t)
				self.assertTrue(m != None)