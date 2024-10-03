# mini_fb/models.py
#Define the data objeects for our application
from django.db import models

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