## hw/urls.py
## description: URL patterns for the hw app

from django.urls import path
    # library of functions for url management
        # path associated url with code
from django.conf import settings
    # import settings so the file knows about the project settings
from . import views
    # from the current directory, use code in views.py

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.home, name='home'),
            # name of function, name of url
    path(r'about', views.about, name='about'),
]