# mini_fb/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
# import generic views
from django.views.generic import ListView
from .models import *

# class-based view
class ShowAllProfilesView(ListView):
    '''
    the view to show all Profiles
    Use this view to obtain data for all Profile records, 
    and to deleguate work to a template called show_all_profiles.html to display all Profiles.
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # the variable name for the list of objects