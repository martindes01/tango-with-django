from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, UserProfile

from datetime import datetime


# Helper functions

def get_category_list(max_results=0, starts_with=''):
    cat_list = []

    # Retrieve all categories beginning with starts_with if supplied
    if starts_with:
        # istartwith filter ignores case
        # startwith filter recognises case
        cat_list = Category.objects.filter(name__istartswith=starts_with).order_by('-likes')

    # Limit categories to max_results if supplied
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    # Return category list
    return cat_list

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
                    # Find page with given ID
                    # get() method returns model instance or raises DoesNotExist exception
                    page = Page.objects.get(id=page_id)

                    # Set last_visit to now
                    page.last_visit = datetime.now()

                    # Increment page views
                    page.views = page.views + 1

                    # Update page
                    page.save()

                    print("First visit {0}".format(str(page.first_visit)))
                    print("Last visit {0}".format(str(page.last_visit)))

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
def like_category(request):
    cat_id = None
    likes = 0

    if request.method == 'GET':
        # Retrieve category ID
        cat_id = request.GET['category_id']

        if cat_id:
            try:
                # Find category with given ID
                # get() method returns model instance or raises DoesNotExist exception
                cat = Category.objects.get(id=int(cat_id))

                # Increment and save category likes and update local likes variable
                likes = cat.likes + 1
                cat.likes = likes
                cat.save()
            except Category.DoesNotExist:
                pass

    # Return repsonse to client
    return HttpResponse(likes)

@login_required
def list_profiles(request):
    # Retrieve all user profiles
    userprofile_list = UserProfile.objects.all()

    # Return rendered response to client
    context_dict = {
        'userprofile_list': userprofile_list,
    }
    return render(request, 'rango/list_profiles.html', context_dict)

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
        
        # Retrieve ordered list of pages associated with category
        pages = Page.objects.filter(category=category).order_by('-views')

        # Add results to context dictionary under relevent keys
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    # Return rendered response to client
    return render(request, 'rango/category.html', context_dict)

def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        # Retrieve query and remove trailing and leading characters
        starts_with = request.GET['suggestion'].strip()

        # Get list of suggested categories
        cat_list = get_category_list(8, starts_with)

    # Return rendered response to client
    context_dict = {
        'cats': cat_list,
        'query': starts_with,
    }
    return render(request, 'rango/cats.html', context_dict)
