from urllib.parse import quote, unquote

def normalize_slug(slug):
	if "%" not in slug:
		slug = quote(slug)
	
	return slug