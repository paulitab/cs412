## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
    # library of functions for url management
        # path associated url with code
from django.conf import settings
    # import settings so the file knows about the project settings
from . import views
    # from the current directory, use code in views.py

# all of the URLs that are part of this app

# The structure of this web application will involve the following URL patterns:
# / : the main page, which will display a picture of a famous or notable person of your choosing and a quote that this person said or wrote. The quote and image will be selected at random from a list of images/quote.
# /quote : the same as /, to generate one quote and one image at random.
# /show_all : an ancillary page which will show all quotes and images.
# /about : an about page with short biographical information about the person whose quotes you are displaying, as well as a note about the creator of this web application (you).
urlpatterns = [
    path(r'', views.quote, name='quote'),
    path(r'quote', views.quote, name='quote'),
    path(r'show_all', views.show_all, name='show_all'),
    path(r'about', views.about, name='about'),

]