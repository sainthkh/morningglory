from django.core.urlresolvers import reverse

def get_post_url_by_slug(slug):
	return reverse('blog:distribute-post', kwargs={"slug" : slug})