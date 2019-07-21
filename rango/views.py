from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Import forms and models
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page

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
    context_dict['visits'] = request.session['visits']

    # Return rendered response to client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Test cookie set in index() view
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    context_dict = {}
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

    return render(request, 'rango/category.html', context_dict)

def user_login(request):
    context_dict = {}

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
            context_dict['error'] = 'Username or password is incorrect.'
            context_dict['username'] = username
    
    # Render form, including error messages
    return render(request, 'rango/login.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
