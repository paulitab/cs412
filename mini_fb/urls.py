## mini_fb/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# define a list of valid URL patterns
urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path(r'create_profile', views.CreateProfileView.as_view(), name='create_profile'), # Create a URL mapping to route requests from the URL pattern 'create_profile' to the CreateProfileView view.
    # Create a URL mapping to route requests from the URL pattern 'profile/<int:pk>/create_status', associate it with the CreateStatusMessageView, and name this URL create_status.
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    # Create a URL mapping to route requests from the URL pattern 'profile/<int:pk>/update_profile', associate it with the UpdateProfileView, and name this URL update_profile.
    path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
]