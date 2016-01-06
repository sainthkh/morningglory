from django.test import TestCase
from django.utils.html import strip_tags

# Create your tests here.

from .utils import *

class UtilTest(TestCase):
	def test__sanitize_title__correct_string__korean(self):
		r = sanitize_title('세계 vs. 세상')
		self.assertEqual(r, '%EC%84%B8%EA%B3%84-vs-%EC%84%B8%EC%83%81')
	
	def test__sanitize_title__correct__korean_with_commas(self):
		r = sanitize_title('결정, 방법')
		self.assertEqual(r, '%EA%B2%B0%EC%A0%95-%EB%B0%A9%EB%B2%95')
		
	def test__sanitize_title__correct__hash_in_title(self):
		r = sanitize_title('Learn English #1')
		self.assertEqual(r, 'learn-english-1')
		
	def test__remove_accents__return_constructed_hangul__hangul_as_argument(self):
		r = remove_accents('한글입니다')
		self.assertEqual(r, '한글입니다')
		
	def test__remove_accents__return_constructed_hangul_with_english_alphabet__hangul_and_alphabet_as_argument(self):
		r = remove_accents('세계 vs. 세상')
		self.assertEqual(r, '세계 vs. 세상')
		
	def test__strip_tags__return_hangul__input_hangul(self):
		r = strip_tags('세계 vs. 세상')
		self.assertEqual(r, '세계 vs. 세상')