## mini_fb/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    
]