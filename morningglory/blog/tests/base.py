from django.test import TestCase

class MorningGloryTestCase(TestCase):
	def run_tests(self, test_set, f):
		for t in test_set:
			with self.subTest(input=t[0]):
				result = f(t[0])
				self.assertEqual(result, t[1])