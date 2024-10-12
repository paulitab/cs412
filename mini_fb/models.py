# mini_fb/models.py
#Define the data objeects for our application
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''
    Profile will model the data attributes of individual Facebook users.
    It need to include the following data attributes: 
    first name, last name, city, email address, and a profile image url.
    '''

    # data attributes for this model:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.first_name} {self.last_name} from {self.city}'
    
    # create an accessor method get_status_messages to obtain all status messages for this Profile.
    def get_status_messages(self):
        '''
        Return a QuerySet of all StatusMessage objects for this Profile.
        '''
        # use the ORM to retrieve StatusMessage objects for which the FK (foreign key) is this Profile
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages

# After storing this new record, the generic CreateView will attempt to display it by using the Profile model’s get_absolute_url method – which you must implement.
# The get_absolute_url method must return a URL to show this one profile, i.e., the URL pattern will be similar to: 'http://127.0.0.1:8000/mini_fb/profile/1.
# Use the reverse function (from (django.urls) and the named URL pattern to obtain a valid URL to show this profile.
    def get_absolute_url(self): 
        '''Return a URL to display this profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    '''
    Class will model the data attributes of Facebook status message.
    It need to include the following data attributes:
        timestamp (the time at which this status message was created/saved)
        message (the text of the status message)
        profile (the foreign key to indicate the relationship to the Profile of the creator of this message)
    '''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # be sure to include the __str__ method on this class to return a string representation of this object.
    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.message} by {self.profile.first_name} {self.profile.last_name} at {self.timestamp}'