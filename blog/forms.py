# blog/forms.py

from django import forms
from .models import Comment 

class CreateCommentForm(forms.ModelForm):
    '''
    A form to add a Comment on an Article to the database
    '''
    class Meta:
        model = Comment
        # fields = ['article', 'author', 'text'] # which field ton include in the form
        fields = ['author', 'text'] # which field ton include in the form