from django.http import HttpResponse
from django.shortcuts import render

# Import Category model
from rango.models import Category

def index(request):
    # Order all currently stored categories by likes in descending order and retrieve top 5
    category_list = Category.objects.order_by('-likes')[:5]

    # Construct dictionary to pass to template engine as its context
    context_dict = {
        'categories': category_list,
    }

    # Return rendered response to send to client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')
