# mini_fb/views.py
# define the views for the mini_fb app
from typing import Any
from django.shortcuts import redirect, render

# Create your views here.
# import generic views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin # assignment 9
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm # assignment 9

from .models import *
from .forms import *

# class-based view
class ShowAllProfilesView(ListView):
    '''
    the view to show all Profiles
    Use this view to obtain data for all Profile records, 
    and to deleguate work to a template called show_all_profiles.html to display all Profiles.
    '''
    # def get_object(self):
    #     '''Locate and return the Profile associated with this User'''
    #     return get_object_or_404(Profile, user=self.request.user)
    
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # the variable name for the list of objects

    # def get_object(self):
    #     '''Locate and return the Profile associated with this User'''
    #     return get_object_or_404(Profile, user=self.request.user)

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
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

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
        return reverse('show_profile', kwargs={'pk': self.object.pk}) 
    
    # assignment 9
    # create an instance of the UserCreationForm and store this instance in the context data. 
    def get_context_data(self, **kwargs: Any) -> Any:
        '''Add the UserCreationForm to the context data to pass it to the template'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    
    # assignment 9 
    def form_valid(self, form):
        '''This method is called after the form is validated but before saving the data to the database.'''
        # Reconstruct the UserCreationForm instance from the self.request.POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            # Attach the User to the Profile
            form.instance.user = user
            # Save the Profile and delegate to the superclass
            return super().form_valid(form)
        else:
            # If the user form is not valid, re-render the form with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    # Second complication: Implementing the form_valid method
    # To solve this problem, you will need to implement the special method form_valid on the CreateStatusMessageView class.
    def form_valid(self, form):
        '''
        This method is called after the form is validated but before saving the data to the database.
        '''
        # look up the Profile object by its pk. You can find this pk in self.kwargs['pk'].
        profile = Profile.objects.get(user=self.request.user)
        # attach this object to the profile attribute of the status message.
        form.instance.profile = profile

        # assignment 7 task 2:
        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # For each file, you will need to create an Image object; set the file into the Image‘s ImageField attribute, set the foreign key (the status message), and then call Image.save() to save the Image object to the database.
        if files:
            for f in files:
                image = Image(image=f, status_message=sm)
                image.save()
            print(f"Image uploaded: {image.image.url}")
        else:
            print("No images uploaded")

        # delegate work to the superclass version of this method.
        return super().form_valid(form)

    # Third complication: Implementing the get_success_url method
    # To solve this problem, you will need to implement the special method get_success_url on the CreateStatusMessageView class.
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return the URL corresponding to the profile page for whom the StatusMessage was added.
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# assignment 7 task 3
# Create a class-based view called UpdateProfileView, which inherits from the generic UpdateView class. 
# Be sure to specify the form this create view should use, i.e., the UpdateProfileForm. 
# Also, specify the name of the template to use to render this form, which must be called mini_fb/update_profile_form.html.
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''
    A view to update a Profile but not the first name or last name
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return the URL corresponding to the profile page for whom the Profile was updated.
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(Profile, user=self.request.user)

# assignment 7 task 4
# Create a class DeleteStatusMessageView, which inherits from the generic DeleteView class. 
# Set the model, template_name and context_object_name attributes as you have done in the past when using other generic views.
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''
    A view to delete a StatusMessage, overriding some of the default behavior of the generic DeleteView.
    '''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    # Implement the get_success_url method
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # Override the get_success_url(self) method, so that when a StatusMessage is deleted, the user is redirected to the profile page for whom the status message was deleted.
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# assignment 7 task 4
# create a new class UpdateStatusMessageView, which inherits from the generic UpdateView class.
# Set the model, form_class, and template_name attributes as you have done in the past when using other generic views.
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        '''
        After updating, redirect to the profile page of the user who created the status message.
        '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

# Assignment 8
# Create a class CreateFriendView, which inherits from the generic superclass django.views.generic.View. 
class CreateFriendView(LoginRequiredMixin, CreateView):
    '''
    A view to create a Friend relationship
    '''
    # form_class = CreateFriendForm
    # template_name = 'mini_fb/add_friend_form.html'
    
    # Implement/override the dispatch method, in which we can read the URL parameters (from self.kwargs), use the object manager to find the requisite Profile objects, and then call the Profile‘s add_friend method (from step 2, above). Finally, we can redirect the user back to the profile page.
    def dispatch(self, request, *args, **kwargs):
        '''
        Dispatch the request to the appropriate method based on the request method.
        '''
        # get the Profile objects
        # profile1 = Profile.objects.get(pk=self.kwargs['pk'])
        # profile2 = Profile.objects.get(pk=self.kwargs['other_pk'])
        # Get the Profile of the logged-in user
        profile1 = get_object_or_404(Profile, user=request.user)
        # Get the Profile of the other user using the 'other_pk' from the URL
        profile2 = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        # call the add_friend method
        profile1.add_friend(profile2)
        # redirect the user back to the profile page
        return redirect('show_profile', pk=profile1.pk)
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# Create a class-based view called ShowFriendSuggestionsView, which inherits from the generic DetailView class.
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''
    A view to show friend suggestions
    '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(Profile, user=self.request.user)

# Create a new view class ShowNewsFeedView which inherits from DetailView, and associate it with the news_feed.html template.
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''
    A view to show a news feed
    '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(Profile, user=self.request.user)
