# mini_fb/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
# import generic views
from django.views.generic import ListView, DetailView
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

class ShowProfilePageView(DetailView):
    '''
    Use this view to obtain data for one Profile record, 
    and to delegate work to a template called show_profile_page.html to display that Profile.
    '''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'