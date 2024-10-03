# mini_fb/models.py
#Define the data objeects for our application
from django.db import models

# Create your models here.

class Procfile(models.Model):
    '''
    Procfile will model the data attributes of individual Facebook users.
    It need to include the following data attributes: 
    first name, last name, city, email address, and a procfile image url.
    '''

    # data attributes for this model:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_url = models.URLField(blank=True)