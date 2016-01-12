from django.test import TestCase
from django.utils.html import strip_tags

# Create your tests here.

from .utils import *

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