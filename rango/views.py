from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Import forms and models
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # Set registration success false initially
    registered = False

    if request.method == 'POST':
        # Retrieve raw form data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user form data to database
            user = user_form.save()

            # Hash password with set_password() method
            user.set_password(user.password)
            user.save()

            # Set commit=False since user attribute must set separately
            profile = profile_form.save(commit=False)
            profile.user = user

            # Retrieve profile picture from form and add to user profile
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save user profile model instance
            profile.save()

            # Set registration success true
            registered = True
        else:
            # Print form errors
            print(user_form.errors, profile_form.errors)
    else:
        # Not HTTP POST
        # Initialise blank forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render form, including error messages
    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }
    return render(request, 'rango/register.html', context_dict)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

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

def user_login(request):
    if request.method == 'POST':
        # request.POST.get() returns None if value does not exist
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check validity and return user object
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Account valid and active
                # Log in and return to index
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # Inactive account
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Invalid login
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        # Render form
        context_dict = {}
        return render(request, 'rango/login.html', context_dict)
