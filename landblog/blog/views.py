from django.shortcuts import render

from blog.models import Article


# Create your views here.
def index(request):
    post_list = Article.objects.all().order_by('-created_at')

    context = {
        'post_list': post_list,
    }

    return render(request, 'index.html', context=context)