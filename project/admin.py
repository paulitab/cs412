# project/admin.py
# Paula Lopez Burgos, paulalb@bu.edu, 11/20/2024
# Description: This file registers the models in the admin site

from django.contrib import admin
from .models import *

# tell the admin we want to administer the following models
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(BakeryGood)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Friend)
admin.site.register(BlogPost)


