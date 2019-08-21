import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango-with-django.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    # Create lists of page dictionaries for each category

    python_pages = [
        {
            'title': 'Official Python Tutorial',
            'url': 'http://docs.python.org/2/tutorial/',
            'views': 128,
        },
        {
            'title': 'How to Think like a Computer Scientist',
            'url': 'http://www.greenteapress.com/thinkpython/',
            'views': 64,
        },
        {
            'title': 'Learn Python in 10 Minutes',
            'url': 'http://www.korokithakis.net/tutorials/python/',
            'views': 32,
        },
    ]

    django_pages = [
        {
            'title': 'Official Django Tutorial',
            'url': 'https://docs.djangoproject.com/en/1.9/intro/tutorial01/',
            'views': 16,
        },
        {
            'title': 'Django Rocks',
            'url': 'http://www.djangorocks.com/',
            'views': 8,
        },
        {
            'title': 'How to Tango with Django',
            'url': 'http://www.tangowithdjango.com/',
            'views': 4,
        },
    ]

    other_pages = [
        {
            'title': 'Bottle',
            'url': 'http://bottlepy.org/docs/dev/',
            'views': 2,
        },
        {
            'title': 'Flask',
            'url': 'http://flask.pocoo.org',
            'views': 1,
        },
    ]

    # Create dictionary of categories, including page dictionary lists
    cats = {
        'Python': {
            'pages': python_pages,
            'views': 128,
            'likes': 64,
        },
        'Django': {
            'pages': django_pages,
            'views': 64,
            'likes': 32,
        },
        'Other Frameworks': {
            'pages': other_pages,
            'views': 32,
            'likes': 16,
        },
        'Pascal': {
            'pages': [],
            'views': 16,
            'likes': 8,
        },
        'Perl': {
            'pages': [],
            'views': 8,
            'likes': 4,
        },
        'PHP': {
            'pages': [],
            'views': 4,
            'likes': 2,
        },
        'Prolog': {
            'pages': [],
            'views': 2,
            'likes': 1,
        },
        'PostScript': {
            'pages': [],
            'views': 1,
            'likes': 0,
        },
        'Programming': {
            'pages': [],
            'views': 0,
            'likes': 0,
        },
    }

    # Add each category in category dictionary
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        # Add pages associated to category
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # Print categories added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
