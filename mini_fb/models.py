# mini_fb/models.py
#Define the data objeects for our application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    # assignment 9 
    # add a ForeignKey to the standard Django User model that will associate each Profile with an User for authentication and identification purposes.
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW

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
    
    # assignment 8
    # Write a get_friends accessor method on the Profile class, which will return a list of friend’s profiles.
    def get_friends(self):
        '''
        Return a list of Profile objects that are friends with this Profile.
        '''
        # This method will need to use the Django ORM (i.e., Friend.objects) and its methods to filter/retrieve matching Friend records.
        # This method must return a list of the friends’ Profiles (not a QuerySet or list of Friends). Pay attention to the data types.
        
        # friends = []
        # friend_relations = Friend.objects.filter(profile1=self)
        # for friend_relation in friend_relations:
        #     friends.append(friend_relation.profile2)
        # return friends

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
        suggestions = Profile.objects.exclude(id__in=[p.id for p in excluded_profiles])
        
        return suggestions
    
    # Write a method get_news_feed(self) on the Profile object, which will return a list (or QuerySet) of all StatusMessages for the profile on which the method was called, as well as all of the friends of that profile.
    def get_news_feed(self):
        '''
        Return a list of StatusMessage objects for this Profile and its friends.
        '''
        # Get all status messages for this Profile
        news_feed = list(self.get_status_messages())
        # Get all status messages for friends
        for friend in self.get_friends():
            news_feed.extend(list(friend.get_status_messages()))
        # Sort the list of status messages by timestamp
        news_feed.sort(key=lambda x: x.timestamp, reverse=True)
        
        return news_feed

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
    
    # access the Images associated with a StatusMessage by adding an accessor method (get_images) to the StatusMessage model.
    # This get_images method should use the ORM to find all Images with the foreign key of this StatusMessage, 
    # and then return the QuerySetof those Image(s). 
    # The QuerySet could be empty if there are no Images for this StatusMessage.
    def get_images(self):
        '''
        Return a QuerySet of all Image objects for this StatusMessage.
        '''
        # use the ORM to retrieve Image objects for which the FK (foreign key) is this StatusMessage
        images = Image.objects.filter(status_message=self)
        return images
    
# Assignment 7
# Create a new data model called Image, which encapsulates the idea of an image file (not a URL) that is stored in the Django media directory.
class Image(models.Model):
    '''
    We want to enable one StatusMessage to have zero to many Images, and thus the Image model will have a foreign key to the StatusMessage model.
    In addition to the models.ImageField and models.ForeignKey, the Image must also include a timestamp of when it was uploaded.
    '''
    image = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    # be sure to include the __str__ method on this class to return a string representation of this object.
    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.image} uploaded at {self.timestamp}'

# Assignment 8
# Create a new data model called Friend, which encapsulates the idea of an edge connecting two nodes within the social network
class Friend(models.Model):
    '''
    Model for encapsulating the idea of an edge connecting two nodes within the social network.
    A Friend relation will associate 2 Profiles, and also store a timestamp of the friendship creation (i.e., “anniversary”) date. Use the attribute names profile1, profile2, and timestamp.
    '''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    # write a __str__ method so that you can view this relationship as a string representation
    def __str__(self):
        '''Return a string representation of this friendship object.'''

        return f'{self.profile1.first_name} {self.profile1.last_name} and {self.profile2.first_name} {self.profile2.last_name} became friends on {self.timestamp}'