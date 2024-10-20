# blog/models.py
# tell the admin we want to administer these models
from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)