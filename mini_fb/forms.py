# mini_fb/forms.py
# define the forms for the mini_fb app
# task 3

from django import forms
from .models import Profile, StatusMessage

# Create a class CreateProfileForm which inherits from forms.ModelForm.
class CreateProfileForm(forms.ModelForm):
    '''
    A form to add a Profile to the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the Profile model.
    class Meta:
        model = Profile
        # specify the list of fields that this form should set (i.e., all of the data attributes of the Profile class).
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url'] 

# task 4
# Create a class CreateStatusMessageForm which inherits from forms.ModelForm.
class CreateStatusMessageForm(forms.ModelForm):
    '''
    A form to add a StatusMessage to the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the StatusMessage model.
    class Meta:
        model = StatusMessage
        # specify the list of fields that this form should set (i.e., all of the data attributes of the StatusMessage class).
        fields = ['message']


# assignment 5 task 3
# Create a new form class UpdateProfileForm which inherits from forms.ModelForm. 
class UpdateProfileForm(forms.ModelForm):
    '''
    A form to update a Profile in the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the Profile model.
    class Meta:
        model = Profile
        # specify the list of fields that this form should set 
        # NOT the user’s first name or last name, which should not be changeable
        fields = ['city', 'email', 'image_url']