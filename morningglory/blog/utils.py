import re
import unicodedata
from urllib.parse import quote, unquote
from django.utils.html import strip_tags

def slugify(text):
	text = re.sub("\s+", '-', text.lower()) # space to -
	text = quote(text) # escape text
	text = re.sub("[^a-zA-z0-9\-%]+", '', text) #remove non-url characters
	text = re.sub("\-\-+", '-', text) # multiple '-' with single '-'
	text = re.sub("^-+", '', text) # Trim - in the front
	text = re.sub("-+$", '', text) # Trim - in the back
	return text
	
def sanitize_title(title):
	title = remove_accents(title);
	title = sanitize_title_with_dashes(title)
	
	return title;

def sanitize_title_with_dashes(title):
	title = strip_tags(title);
	# Preserve escaped octets.
	title = re.sub(r'%([a-fA-F0-9][a-fA-F0-9])', r'---\1---', title);
	# Remove percent signs that are not part of an octet.
	title = re.sub(r'%', r'', title)
	# Restore octets.
	title = re.sub(r'---([a-fA-F0-9][a-fA-F0-9])---', r'\1', title);

	title = title.lower()
	title = re.sub('&.+?;', '', title) # kill entities

	# Convert nbsp, ndash and mdash to hyphens
	title = re.sub('%c2%a0|%e2%80%93|%e2%80%94', '-', title );

	# Strip these characters entirely
	title = re.sub( r'%c2%a1|%c2%bf', '', title) # iexcl and iquest
	title = re.sub( r'%c2%ab|%c2%bb|%e2%80%b9|%e2%80%ba', '', title) # angle quotes
	title = re.sub( r'%e2%80%98|%e2%80%99|%e2%80%9c|%e2%80%9d|%e2%80%9a|%e2%80%9b|%e2%80%9e|%e2%80%9f', '', title) # curly quotes
	title = re.sub( r'%c2%a9|%c2%ae|%c2%b0|%e2%80%a6|%e2%84%a2', '', title) # copy, reg, deg, hellip and trade
	title = re.sub( r'%c2%b4|%cb%8a|%cc%81|%cd%81', '', title) #acute accents
	title = re.sub( r'%cc%80|%cc%84|%cc%8c', '', title) #grave accent, macron, caron

	# Convert times to x
	title = title.replace( '%c3%97', 'x');
	
	title = re.sub(r'[!@#$^&*()_\+<>{}\/.,]', '', title)
	title = re.sub("\s+", '-', title)
	title = quote(title)
	title = re.sub("[^a-zA-z0-9\-%]+", '', title) #remove non-url characters
	title = re.sub("\-\-+", '-', title) # multiple '-' with single '-'
	title = re.sub("^-+", '', title) # Trim - in the front
	title = re.sub("-+$", '', title) # Trim - in the back

	return title;

def remove_accents(string):
	a = []
	for c in string:
		if re.match('[가-힣]', c) == None:
			c = unicodedata.normalize('NFD', c)
		a.append(c)

	return ''.join(a)