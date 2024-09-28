# formdata/urls.py
# define the URL patterns for the formdata app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
urlpatterns = [
    path('', views.show_form, name='show_form'), 
    path('submit/', views.submit, name='submit'),
]