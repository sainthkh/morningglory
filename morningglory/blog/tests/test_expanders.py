from django.test import TestCase
from blog.expanders import *

class ExpanderTest(TestCase):

	#
	# -- setup and teardown --
	#
	########################################
	def setUp(self):
		expanders = {} # Empty expanders
	
	def tearDown(self):
		pass
	
	def setUp_test_custom_tag(self):
		def test(content):
			content = '--' + content + '--'
			return content
		
		add_custom_tag('test', test)
	
	#
	# -- tag_regex tests --
	#
	##################################################
	
	def test__tag_regex__tags__match(self):
		m = re.match(tag_regex, "<<test>>\nHello, World\n<</test>>", re.M|re.S)
		self.assertNotEqual(m, None)
	
	def test__tag_regex__tags__content_match(self):
		m = re.match(tag_regex, "<<test>>\nHello, World\n<</test>>", re.M|re.S)
		self.assertEqual(m.group(2), "\nHello, World\n")
	
	#
	# -- expand_content tests --
	#
	##########################################################
	
	# test 1. simple unregistered tag
	
	def test__expand_content__unregistered_tag_name__same_string(self):
		text = "<<no_name>>Hello, World!<</no_name>>"
		
		self.assertEqual(expand_content(text), text)
	
	# test 2. tests with single registered tag
	
	def compare_texts(self, input, result):
		self.setUp_test_custom_tag()
		self.assertEqual(expand_content(input), result)
	
	def test__expand_content__tag_name__changed(self):
		self.compare_texts("<<test>>Hello, World!<</test>>", "--Hello, World!--")
		
	def test__expand_content__same_tags__all_changed(self):
		self.compare_texts(
			"<<test>>Hello, World!<</test>>How are you?<<test>>I am fine. Thank you. And you?<</test>>",
			"--Hello, World!--How are you?--I am fine. Thank you. And you?--" 
		)		
	
	def test__expand_content__tag_with_newline__changed(self):
		self.compare_texts(
			"<<test>>\nHello, World!\n<</test>>",
			"--\nHello, World!\n--" 
		)

	def test__expand_content__tags_with_newline__all_changed(self):
		self.compare_texts(
			"<<test>>\nHello, World!\n<</test>>\n\nHow are you?<<test>>I am fine. \nThank you. And you?<</test>>",
			"--\nHello, World!\n--\n\nHow are you?--I am fine. \nThank you. And you?--" 
		)

	# test 3. tests with multiple registered tags		

	def setUp_foo_bar_custom_tag(self):
		def foo(content):
			content = '**' + content + '**'
			return content
		
		def bar(content):
			content = '__' + content + '__'
			return content	
		
		add_custom_tag("foo", foo)
		add_custom_tag("bar", bar)
	
	def compare_texts2(self, input, result):
		self.setUp_test_custom_tag()
		self.setUp_foo_bar_custom_tag()
		self.assertEqual(expand_content(input), result)
	
	def test__expand_content__different_tags__all_changed(self):
		self.compare_texts2(
			"<<foo>>Hi<</foo>>More text here<<bar>>Good Bye!<</bar>>",
			"**Hi**More text here__Good Bye!__"
		)
	
	def test__expand_content__different_tags_and_one_non_exist__one_changed_and_other_not(self):
		self.compare_texts2(
			"<<foo>>Hi<</foo>>More text here<<no_name>>Good Bye!<</no_name>>",
			"**Hi**More text here<<no_name>>Good Bye!<</no_name>>"
		)
	
