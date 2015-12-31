from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'blog/index.html', {})
   
def list_post(request):
    pass
   
def list_post_paged(request):
    pass

def single_post(request):
    pass

def category(request):
    pass

def category_paged(request):
    pass

