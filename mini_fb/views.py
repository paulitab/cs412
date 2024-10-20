# mini_fb/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
# import generic views
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from .models import *
from .forms import *

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

    # Implement the get_context_data method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the profile based on the primary key in the URL
        profile = self.get_object()
        
        # Add the profile's status messages to the context
        context['status_messages'] = StatusMessage.objects.filter(profile=profile)
        
        # Optionally, also pass images for each status message
        # This assumes you have a get_images method on StatusMessage
        for status in context['status_messages']:
            status.images = status.get_images()

        return context

# Create a class-based view called CreateProfileView, which inherits from the generic CreateView class.
# Be sure to specify the form this create view should use, i.e., the CreateProfileForm. 
# Also, specify the name of the template to use to render this form, which must be called mini_fb/create_profile_form.html.
class CreateProfileView(CreateView):
    '''
    A view to create a Profile
    '''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        return reverse('show_all_profiles') # lookup the URL called 'show_all_profiles' after the form has been succesful
    
class CreateStatusMessageView(CreateView):
    '''
    A view to create a StatusMessage
    '''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # first complication: Implementing get_context_data method
    def get_context_data(self, **kwargs):
            # The attribute self.kwargs is a dictionary of any URL parameters, and the value self.kwargs['pk'] is the primary key of the Profile corresponding to the URL pattern.
        '''
        Add the Profile to the context data so that the template can use it to display the Profile's name.
        '''
        # Within get_context_data method, create a context dictionary, add the Profile object (call the context variabale profile, for consistency with how things worked on other pages).
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    # Second complication: Implementing the form_valid method
    # To solve this problem, you will need to implement the special method form_valid on the CreateStatusMessageView class.
    def form_valid(self, form):
        '''
        This method is called after the form is validated but before saving the data to the database.
        '''
        # look up the Profile object by its pk. You can find this pk in self.kwargs['pk'].
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # attach this object to the profile attribute of the status message.
        form.instance.profile = profile

        # assignment 7 task 2:
        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # For each file, you will need to create an Image object; set the file into the Image‘s ImageField attribute, set the foreign key (the status message), and then call Image.save() to save the Image object to the database.
        for f in files:
            image = Image(image=f, status_message=sm)
            image.save()
        print(files)
        print(image.image.url)

        # delegate work to the superclass version of this method.
        return super().form_valid(form)

    # Third complication: Implementing the get_success_url method
    # To solve this problem, you will need to implement the special method get_success_url on the CreateStatusMessageView class.
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return the URL corresponding to the profile page for whom the StatusMessage was added.
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
