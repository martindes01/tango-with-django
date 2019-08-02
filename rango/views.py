from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, UserProfile

from datetime import datetime


# Cookie helper functions

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Cast value of visits cookie to int, default 1
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Cast value of last_visit cookie to datetime, default now
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # Test whether at least 1 day has passed since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        # Update last visit_cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set last visit_cookie
        request.session['last_visit'] = last_visit_cookie

    # Set or update visits cookie
    request.session['visits'] = visits


# View functions

def track_url(request):
    # Initially assume page_id not provided
    page_id = None

    if request.method == 'GET':
        if 'page_id' in request.GET:
            try:
                # GET[] method returns int given as base 10 literal or raises ValueError exception
                page_id = request.GET['page_id']

                try:
                    # Find page with given id
                    # get() method returns model instance or raises DoesNotExist exception
                    page = Page.objects.get(id=page_id)

                    # Increment page views and save
                    page.views = page.views + 1
                    page.save()

                    # Redirect to page
                    return redirect(page.url)
                except Page.DoesNotExist:
                    pass
            except ValueError:
                pass
        
        # Redirect to index if page_id parameter not provided or does not return model instance
        return redirect('index')

def index(request):
    # Set cookie to test in about() view
    request.session.set_test_cookie()

    # Order all categories by likes in descending order and retrieve top 5
    category_list = Category.objects.order_by('-likes')[:5]

    # Order all pages by views in descending order and retrieve top 5
    page_list = Page.objects.order_by('-views')[:5]

    # Construct dictionary to pass to template engine as its context
    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    # Call helper function to handle cookies
    visitor_cookie_handler(request)

    # Return rendered response to client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Test cookie set in index() view
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # Call helper function to handle cookies
    visitor_cookie_handler(request)

    # Return rendered response to client
    context_dict = {
        'visits': request.session['visits']
    }
    return render(request, 'rango/about.html', context_dict)

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        # Find category with given slug
        # get() method returns model instance or raises DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                # Set commit=False since some attributes must be set separately
                page = form.save(commit=False)
                
                # Set attributes and save page to database
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
def profile(request, username):
    try:
        # Find user with given username
        # get() method returns model instance or raises DoesNotExist exception
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Redirect to index
        return redirect('index')

    # get_or_create() method returns (object, created) tuple
    # object is model instance and created is boolean
    # A database entry is created if none is found
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    
    # Populate form with user profile data
    form = UserProfileForm({
        'website': userprofile.website,
        'picture': userprofile.picture,
    })

    if request.method == 'POST':
        # Retrieve form data
        # UserProfileForm model instance references UserProfile model instance being updated
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            # Save updated user profile to database
            form.save(commit=True)

            # Redirect to updated profile
            #return redirect('profile', user.username)
        else:
            # Print form errors
            print(form.errors)

    # Render form, including error messages
    context_dict = {
        'userprofile': userprofile,
        'selecteduser': user,
        'form': form,
    }
    return render(request, 'rango/profile.html', context_dict)

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        # Retrieve form data
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # Set commit=False since user attribute must be set separately
            user_profile = form.save(commit=False)

            # Set user attribute and save user profile model instance
            user_profile.user = request.user
            user_profile.save()

            # Redirect to index
            return redirect('index')
        else:
            # Print form errors
            print(form.errors)

    # Render form, including error messages
    context_dict = {
        'form': form,
    }
    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def restricted(request):
    # Return rendered response to client
    context_dict = {}
    return render(request, 'rango/restricted.html', context_dict)

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

    # Return rendered response to client
    return render(request, 'rango/category.html', context_dict)
