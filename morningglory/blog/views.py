from django.shortcuts import render, redirect

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
    return render(request, 'blog-admin/write.html', {})

def edit_post(request, post_id):
    return render(request, 'blog-admin/write.html', {})

def save_post(request):
    return redirect('blog:edit_post', args=(1))