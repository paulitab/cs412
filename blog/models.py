# blog/models.py
#Define the data objeects for our application
from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulate the idea of one Article by some author.'''

    # data attributes for an Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''Return a QuerySet of all COmments on this Article'''

        # use the ORM to retriebe Comments for which the FK (foregin key) is this Article
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment (models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # model the 1 to many relationship with Article (foreign key)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
        # cascade means if the article is delted, delete all comments
        # the other option is to protect or set null
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this comment.'''

        return f'{self.text}'