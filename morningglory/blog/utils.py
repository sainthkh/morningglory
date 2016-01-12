import re
import unicodedata
from urllib.parse import quote, unquote
from django.utils.html import strip_tags

def slugify(text):
	text = remove_non_letters_and_normalize(text)
	text = sanitize_title_with_dashes(text)
	
	return text

def sanitize_title_with_dashes(title):
	title = title.lower()
	title = re.sub(r"\s+", '-', title)
	title = quote(title)
	title = re.sub(r"[^a-zA-z0-9\-%]+", '', title) #remove non-url characters
	title = re.sub(r"\-\-+", '-', title) # multiple '-' with single '-'
	title = re.sub(r"^-+", '', title) # Trim - in the front
	title = re.sub(r"-+$", '', title) # Trim - in the back

	return title;
	
def remove_non_letters_and_normalize(string):
	result_string = []
	
	for c in string:
		category = unicodedata.category(c)
		if c == '-' or c == ' ' or category[0] == 'L' or re.match('[0-9]', c) != None:
			if re.match('[가-힣]', c) == None: # Korean Hangeul should not be normalized
				c = unicodedata.normalize('NFD', c)
			result_string.append(c)
	
	return ''.join(result_string)