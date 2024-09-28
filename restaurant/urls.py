# restaurant/urls.py
# define the URL patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
# /main : the page with basic information about the restaurant. 
#       the main page should include the name, location, hours of operation (displayed as a list or table), 
#       and one or more photos appropriate to such a page.
# /order : display an online order form (details below under HTML templates).
# /confirmation : a confirmation page to display after the order is placed. 
#       The confirmation page will display which items were ordered, the customer information, 
#       and the expected time at which the order will be ready (a time to be determined randomly, 
#       but within 30-60 minutes of the current date/time).
urlpatterns = [
    path('', views.main, name='main'), 
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]