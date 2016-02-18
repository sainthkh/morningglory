from django.test import TestCase

import mistune
import re

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
			('세계 vs. 세상', '%ec%84%b8%ea%b3%84-vs-%ec%84%b8%ec%83%81'),
			('결정, 방법', '%ea%b2%b0%ec%a0%95-%eb%b0%a9%eb%b2%95'),
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
			("Hi   \nWorld\n  \t\nI am C.", "Hi  \nWorld\n  \t\nI am C."),
			("한글이 있다.\nThere is Hangeul.\n\n한글이 또 있다.\nThere is another Hangeul.",
				"한글이 있다.  \nThere is Hangeul.\n\n한글이 또 있다.  \nThere is another Hangeul."),
			("# What is in this Book?\n\n30 useful idioms\n90+ example sentences\n150+ Korean word definitions\n90+ practice sentences\n\n",
				"# What is in this Book?\n\n30 useful idioms  \n90+ example sentences  \n150+ Korean word definitions  \n90+ practice sentences\n\n"),
			("<<buy>>korean-idioms<</buy>>\n\n# What is in this Book?\n\n30 useful idioms\n90+ example sentences\n150+ Korean word definitions\n90+ practice sentences\n\n",
				'<a href="/payment/korean-idioms" class="btn btn-buy btn-lg"><i class="fa fa-shopping-cart"></i>  Buy Now</a>\n\n# What is in this Book?\n\n30 useful idioms  \n90+ example sentences  \n150+ Korean word definitions  \n90+ practice sentences\n\n'),
		]
		
		self.run_tests(test_set, process_content)
		
	def test__process_content__over23matches__work(self):
		for i in range(5, 6):
			c = []
			r = []
			for i in range(i-1):
				c.append('aaaa\n')
				r.append('aaaa  \n')
			
			dummy_long = ''.join(c) + 'aaaa\n'
			dummy_long_answer = ''.join(r) + 'aaaa\n'

			with self.subTest(input=i):
				self.assertEqual(process_content(dummy_long), dummy_long_answer)
	
	def test__process_content_stage1__over23matches__work(self):
		for i in range(1, 23):
			c = []
			r = []
			for i in range(i):
				c.append('aaaa \n')
				r.append('aaaa \n')
			
			text = ''.join(c)
			result = ''.join(r) 

			with self.subTest(input=i):
				text = re.sub(r" *?\n *?\n", r"$$newline$$", text, re.M|re.S)
				self.assertEqual(text, result)
	
	def test__process_content_stage2__over23matches__work(self):
		for i in range(1, 100):
			c = []
			r = []
			for i in range(i):
				c.append('aaaa \n')
				r.append('aaaa  \n')
			
			text = ''.join(c)
			result = ''.join(r) 

			with self.subTest(input=i):
				text = re.sub(r" *?\n", r"  \n", text)
				self.assertEqual(text, result)
	
	
	