from django.shortcuts import reverse
from django.test import TestCase

from rango.models import Category, Page

from datetime import datetime


# Helper functions

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(category, title):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.save()
    return p


# Test function classes

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive returns True for categories with non-negative views
        """

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks appropriate slug created when category added
        """

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

class PageMethodTests(TestCase):
    def test_ensure_visits_not_in_future(self):
        """
        ensure_visits_not_in_future checks first visit and last visit not in future
        """
        
        # Create category and add page
        c = add_cat('test', 1, 1)
        p = add_page(c, 'test')

        # Test visits not in future
        self.assertEqual(p.first_visit < datetime.now(), True)
        self.assertEqual(p.last_visit < datetime.now(), True)

    def test_ensure_last_visit_not_before_first(self):
        """
        ensure_last_visit_not_before_first checks last visit not before first
        """

        # Create category and add page
        c = add_cat('test', 1, 1)
        p = add_page(c, 'test')

        # Test last visit not before first
        self.assertEqual(p.last_visit < p.first_visit, False)

class IndexViewTests(TestCase):
    def test_index_view_with_categories(self):
        """
        index_view_with_categories checks categories displayed on index
        """

        # Create 4 categories
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))

        # Test page load OK
        self.assertEqual(response.status_code, 200)

        # Test response HTML contains category name
        self.assertContains(response, "tmp test temp")
        
        # Test context dictionary contains 4 categories
        self.assertEqual(len(response.context['categories']), 4)

    def test_index_view_with_no_categories(self):
        """
        index_view_with_no_categories checks appropriate message displayed if no categories exist
        """

        response = self.client.get(reverse('index'))

        # Test page load OK
        self.assertEqual(response.status_code, 200)

        # Test context dictionary contains empty category list
        self.assertQuerysetEqual(response.context['categories'], [])

        # Test response HTML contains message
        self.assertContains(response, "There are currently no categories.")
