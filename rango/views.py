from django.http import HttpResponse
from django.shortcuts import render

# Import forms and models
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page

def index(request):
    # Order all categories by likes in descending order and retrieve top 5
    category_list = Category.objects.order_by('-likes')[:5]

    # Order all pages by views in descending order and retrieve top 5
    page_list = Page.objects.order_by('-views')[:5]

    # Construct dictionary to pass to template engine as its context
    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    # Return rendered response to client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            # Save new category to database
            form.save(commit=True)
            # Redirect to index
            return index(request)
        else:
            # Print form errors
            print(form.errors)

    # Render form, including error messages
    context_dict = {
        'form': form,
    }
    return render(request, 'rango/add_category.html', context_dict)

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                # Save page to database
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # Redirect to category
                return show_category(request, category_name_slug)
        else:
            # Print form errors
            print(form.errors)

    # Render form, including error messages
    context_dict = {
        'form': form,
        'category': category,
    }
    return render(request, 'rango/add_page.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Find category with given slug
        # get() method returns model instance or raises DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve list of pages associated with category
        pages = Page.objects.filter(category=category)

        # Add results to context dictionary under relevent keys
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)
