from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import *

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
    return render(request, 'blog/single_post.html', {})

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
    else:
        post = Post()
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
    post.save()
    
    return redirect('blog:edit-post', slug=post.slug)