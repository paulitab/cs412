# project/models.py
# Define the data objeects for our application
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# from the proposal we have the following models:
# UserProfile, Recipe, Ingredient, RecipeIngredient, BakeryGood, Order, OrderItem

# UserProfile
#       Last name (text)
#       First name (text)
#       Address (text)
#       Email (text)

# Recipe
#       Name (text)
#       Instructions (text)
#       Difficulty level (number)
#       Image (image file)

# Ingredient
#       Name (text)

# RecipeIngredient
#       Recipe (Foreign Key to Recipe)
#       Ingredient (Foreign Key to Ingredient)
#       Quantity (number)
#       Unit (text)
# this model was not in the proposal but was created in order to get rid of the many-to-many relationship 
# between Recipe and Ingredient since the professor said it was best not to use many-to-many relationships

# BakeryGood
#       Name (text)
#       Description (text)
#       Price (number)
#       Image (image file)

# Order
#       Order date (date)
#       UserProfile (Foreign Key to UserProfile)
#       Total price (number calculated based on OrderItems)
#       Status (choice of: “cart”, “processing” or “complete”)

# OrderItem
#       Order (Foreign Key to Order)
#       BakeryGood (Foreign Key to BakeryGood)
#       Quantity (number)
#       Price (number)


# Create your models here.
class UserProfile(models.Model):
    '''
    UserProfile will model the data attributes of individual users.
    It need to include the following data attributes: 
    last name, first name, address, and email.
    '''
    # data attributes for this model:
    last_name = models.TextField(blank=False)
    first_name = models.TextField(blank=False)
    address = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.first_name} {self.last_name} from {self.address}'
    
    # create an accessor method get_review to obtain all review for this Profile.
    def get_review(self):
        '''
        Return a QuerySet of all Reviews objects for this Profile.
        '''
        # use the ORM to retrieve reviews objects for which the FK (foreign key) is this Profile
        review = Review.objects.filter(profile=self)
        return review

    # After storing this new record, the generic CreateView will attempt to display it by using the Profile model’s get_absolute_url method – which you must implement.
    # The get_absolute_url method must return a URL to show this one profile, i.e., the URL pattern will be similar to: 'http://127.0.0.1:8000/mini_fb/profile/1.
    # Use the reverse function (from (django.urls) and the named URL pattern to obtain a valid URL to show this profile.
    def get_absolute_url(self): 
        '''Return a URL to display this profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    # assignment 8
    # Write a get_friends accessor method on the Profile class, which will return a list of friend’s profiles.
    def get_friends(self):
        '''
        Return a list of Profile objects that are friends with this Profile.
        '''
        # This method will need to use the Django ORM (i.e., Friend.objects) and its methods to filter/retrieve matching Friend records.
        # This method must return a list of the friends’ Profiles (not a QuerySet or list of Friends). Pay attention to the data types.

        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        # Collect all friend Profiles
        friends = [f.profile2 for f in friends_as_profile1] + [f.profile1 for f in friends_as_profile2]
        
        return friends

    # Create a method on the Profile class called add_friend(self, other). 
    # This method takes a parameter other, which refers to another Profile instance, and the effect of the method should be add a Friend relation for the two Profiles: self and other.
    def add_friend(self, other):
        '''
        Add a Friend relation for both this Profile and other Profile.
        '''
        # It is important to not add extra/duplicate Friends
        # Additionally, we do not want to allow “self-friending”
        # If no existing Friend relationship exists, create a new Friend instance and save it to the database.
        if self != other:
            if not Friend.objects.filter(profile1=self, profile2=other).exists() and not Friend.objects.filter(profile1=other, profile2=self).exists():
                friend = Friend(profile1=self, profile2=other)
                friend.save()
        return None
    
    # Write a method get_friend_suggestions(self) which will return a list (or QuerySet) of possible friends for a Profile. 
    def get_friend_suggestions(self):
        '''
        Return a list of Profile objects that are not already friends with this Profile.
        '''
        # Get all profiles that are already friends
        friend_profiles = set(self.get_friends())
        # Add self to the excluded profiles
        excluded_profiles = friend_profiles.union({self})
        # Get profiles that are not already friends or the profile itself
        suggestions = UserProfile.objects.exclude(id__in=[p.id for p in excluded_profiles])
        
        return suggestions
    
class Recipe(models.Model):
    '''
    Recipe will model the data attributes of a recipe.
    It need to include the following data attributes:
    name, instructions, difficulty level, and image.
    '''

    # data attributes for this model:
    name = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    difficulty_level = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.name} with difficulty level {self.difficulty_level}'
    
class Ingredient(models.Model):
    '''
    Ingredient will model the data attributes of an ingredient.
    It need to include the following data attributes:
    name.
    '''

    # data attributes for this model:
    name = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.name}'
    
class RecipeIngredient(models.Model):
    '''
    RecipeIngredient will model the data attributes of a recipe ingredient.
    It need to include the following data attributes:
    recipe, ingredient, quantity, and unit.
    '''

    # data attributes for this model:
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    unit = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.quantity} {self.unit} of {self.ingredient} in {self.recipe}'
    
class BakeryGood(models.Model):
    '''
    BakeryGood will model the data attributes of a bakery good.
    It need to include the following data attributes:
    name, description, price, and image.
    '''

    # data attributes for this model:
    name = models.TextField(blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.name} for ${self.price}'
    
class Order(models.Model):
    '''
    Order will model the data attributes of an order.
    It need to include the following data attributes:
    order_date, user, total_price, and status.
    '''

    # data attributes for this model:
    order_date = models.DateField(auto_now=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # total_price = models.DecimalField(max_digits=6, decimal_places=2)
            # not sure if this is needed since it can be calculated based on OrderItem
    status = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'Order by {self.userProfile} on {self.order_date} with status {self.status}'
    
    # @property
    def total_price(self):
        '''Calculate the total price of the order.'''
        return sum(item.bakery_good.price * item.quantity for item in self.orderitem_set.all())
    
class OrderItem(models.Model):
    '''
    OrderItem will model the data attributes of an order item.
    It need to include the following data attributes:
    order, bakery_good, quantity, and price.
    '''

    # data attributes for this model:
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bakery_good = models.ForeignKey(BakeryGood, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    # price = models.DecimalField(max_digits=6, decimal_places=2)
            # not sure if this is needed since it can be calculated based on BakeryGood

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.quantity} {self.bakery_good} in {self.order}'

class Review(models.Model):
    '''
    Review will model the data attributes of a review in the blog.
    It need to include the following data attributes:
    message, profile, and timestamp.
    '''

    # data attributes for this model:
    message = models.TextField(blank=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.message} by {self.profile.first_name} {self.profile.last_name} at {self.timestamp}'

# Create a new data model called Friend, which encapsulates the idea of an edge connecting two nodes within the social network
class Friend(models.Model):
    '''
    Model for encapsulating the idea of an edge connecting two nodes within the social network.
    A Friend relation will associate 2 Profiles, and also store a timestamp of the friendship creation (i.e., “anniversary”) date. Use the attribute names profile1, profile2, and timestamp.
    '''
    profile1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    # write a __str__ method so that you can view this relationship as a string representation
    def __str__(self):
        '''Return a string representation of this friendship object.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} and {self.profile2.first_name} {self.profile2.last_name} became friends on {self.timestamp}'

# Model for a blog post  
class BlogPost(models.Model):
    '''Model for a blog post in the blog''' 
    '''contains the following data attributes: title, content, recipe, author, image, and timestamp'''
    title = models.CharField(max_length=100)
    content = models.TextField()
    recipe = models.TextField(blank=True, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Optional image
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this object.'''
        return self.title