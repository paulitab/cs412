# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
# import generic views
from django.views.generic import ListView
from .models import *

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # the variable name for the list of objects