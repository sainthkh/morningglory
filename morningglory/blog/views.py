from django.shortcuts import render

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

