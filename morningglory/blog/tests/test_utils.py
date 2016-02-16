from django.test import TestCase

import mistune

from blog.utils import *
from blog.utils.views import *

class UtilTest(TestCase):
	def test__quote(self):
		test_set = [
			('세계', '%EC%84%B8%EA%B3%84'),
		]
		
		self.run_tests(test_set, quote)
		
	def test__slugify__correct_slug__in_any_language(self):
		test_set = [
			('세계 vs. 세상', '%EC%84%B8%EA%B3%84-vs-%EC%84%B8%EC%83%81'),
			('결정, 방법', '%EA%B2%B0%EC%A0%95-%EB%B0%A9%EB%B2%95'),
			('Learn English #1', 'learn-english-1'),
		]
		
		self.run_tests(test_set, slugify)
		
	def test__remove_non_letters_and_normalize__only_letters_space_dash__in_any_language(self):
		test_set = [
			("세계 vs. 세상", '세계 vs 세상'),
			('한글입니다', '한글입니다'),
			('Learn English #1', 'Learn English 1'),
			('こんにちは。', 'こんにちは'),
		]
		
		self.run_tests(test_set, remove_non_letters_and_normalize)
				
	def run_tests(self, test_set, f):
		for t in test_set:
			with self.subTest(input=t[0]):
				result = f(t[0])
				self.assertEqual(result, t[1])
	
	#
	# -- template_to_html tests --
	#
	######################################################
	
	def test__template_to_html__correct_file__correct_text(self):
		r = template_to_html('test/simple.html', {"content": "Hello" })
		
		self.assertEqual(r, "<div>Hello</div>")
	
	def test__process_content__newline__correct_br(self):
		test_set = [
			("Hi\n\nWorld", "Hi\n\nWorld"),
			("Hi\nWorld\n\nI am C.", "Hi  \nWorld\n\nI am C."),
			("Hi   \nWorld\n  \t\nI am C.", "Hi  \nWorld\n\nI am C."),
			("한글이 있다.\nThere is Hangeul.\n\n한글이 또 있다.\nThere is another Hangeul.",
				"한글이 있다.  \nThere is Hangeul.\n\n한글이 또 있다.  \nThere is another Hangeul."),
		]
		
		self.run_tests(test_set, process_content)