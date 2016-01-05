from django.shortcuts import render, redirect
#from django.utils.text import slugify
from .models import *
from datetime import datetime
from urllib.parse import quote, unquote
import re

# Create your views here.

def index(request):
    dummy = {
        "category" : [
            {"link" : '/', "name" : 'RM Words' }
        ],
        "link" : '/',
        "title" : '5 Words in RM 3000',
    }
    return render(request, 'blog/index.html', {
        "post" : dummy,
    })
   
def list_post(request):
    pass
   
def list_post_paged(request):
    pass

def single_post(request, year, month, date, slug):
    post_slug = slug
    post = Post.objects(slug=post_slug)
    return __view_single(request, post)

def category(request):
    pass

def category_paged(request):
    pass

def write_new_post(request):
    empty = {
        "slug": "",
        "title": "",
        "content": "",
    }
    return render(request, 'blog-admin/write.html', {
        "post" : empty,
    })

def edit_post(request, slug):
    post_slug = slug
    posts = Post.objects(slug=post_slug)
    post = posts[0]
    print('slug' + str(post.slug))
    return render(request, 'blog-admin/write.html', {
        "post": post
    })

def save_post(request):
    if (request.POST['slug'] != ""):
        post = Post.objects(slug=request.POST['slug'])[0] 
        post.last_modified_date = datetime.now()
    else:
        post = Post()
        post.published_date = datetime.now()
        post.last_modified_date = post.published_date
        slug_base = slugify(request.POST['title'])
        print(Post.objects(slug=slug_base).count())
        exist = Post.objects(slug=slug_base).count() != 0
        if exist:
            num = 1
            while True:
                final_slug = slug_base + '-' + str(num)
                exist = Post.objects(slug=final_slug).count() != 0
                if not exist:
                    break
            post.slug = final_slug
        else:
            post.slug = slug_base        
              
    
    post.title = request.POST['title']
    post.content = request.POST['content']
    post.post_type = 'post'
    post.save()
    
    return redirect('blog:edit-post', slug=post.slug)
    
def distribute_post(request, slug):
    print(slug)
    if "%" not in slug:
        slug = quote(slug)
    print(slug) 
    post_slug = slug
    post = Post.objects.get(slug=post_slug)
    
    if(post.post_type == "link"):
        return redirect(post.redirect_link)
    return __view_single(request, post)
    
def __view_single(request, post):
    return render(request, 'blog/single_post.html', {'post': post })

def slugify(text):
    text = re.sub("\s+", '-', text.lower()) # space to -
    text = quote(text) # escape text
    text = re.sub("\-\-+", '-', text) # multiple '-' with single '-'
    text = re.sub("^-+", '', text) # Trim - in the front
    text = re.sub("-+$", '', text) # Trim - in the back
    return text