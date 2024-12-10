# project/forms.py
# define the forms for the project app

from django import forms
from .models import UserProfile, Review, BlogPost

# Create a class CreateProfileForm which inherits from forms.ModelForm.
class CreateProfileForm(forms.ModelForm):
    '''
    A form to add a Profile to the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the Profile model.
    class Meta:
        model = UserProfile
        # specify the list of fields that this form should set (i.e., all of the data attributes of the Profile class).
        fields = ['first_name', 'last_name', 'address', 'email'] 

# Create a class CreateReviewForm which inherits from forms.ModelForm.
class CreateReviewForm(forms.ModelForm):
    '''
    A form to add a StatusMessage to the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the Review model.
    class Meta:
        model = Review
        # specify the list of fields that this form should set (i.e., all of the data attributes of the StatusMessage class).
        fields = ['message']

# Create a new form class UpdateProfileForm which inherits from forms.ModelForm. 
class UpdateProfileForm(forms.ModelForm):
    '''
    A form to update a Profile in the database
    '''
    # Be sure to specify the inner-class Meta, which relates this form to the Profile model.
    class Meta:
        model = UserProfile
        # specify the list of fields that this form should set 
        # NOT the user’s first name or last name, which should not be changeable
        fields = ['address', 'email']

# Create a new form class for creating a blog post
class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'recipe', 'image']
        widgets = {
            'recipe': forms.TextInput(attrs={'placeholder': 'Describe the recipe you tried'}),
        }