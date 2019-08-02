from django.urls import path

from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('goto/', views.track_url, name='goto'),
    path('profile/<username>', views.profile, name='profile'),
    path('profiles/', views.list_profiles, name='list_profiles'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('restricted/', views.restricted, name='restricted'),
]
