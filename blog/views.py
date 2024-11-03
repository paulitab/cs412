# blog/views.py
# define the views for the blog app
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render

# Create your views here.
# import generic views
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm #31/10
from django.contrib.auth.models import User #31/10
from django.contrib.auth import login #31/10

from blog.forms import *
from .models import *

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # the variable name for the list of objects

    def dispatch(self, *args, **kwargs):
        '''implement this method to add some debug tracing'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        # let the sueprclass version of this method do its work:
        return super().dispatch(*args, **kwargs)

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article # the model to display
    template_name = 'blog/article.html'
    context_object_name = 'article'

    # AttributeError: Generic fetail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object methos
    def get_object(self):
        '''Return one Article chosen at random'''

        # explicitly add an error to generate a call stack trace:
        # y = 3 / 0

        # get all Article objects
        articles = Article.objects.all()
        # select one at random
        article = random.choice(articles)
        return article
    
class ArticleView(DetailView):
    '''Display one Article selecyed by PK'''
    model = Article # the model to display
    template_name = 'blog/article.html'
    context_object_name = 'article' # the variable name for the list of objects

class CreateCommentView(CreateView):
    '''
    A view to create a Comment on an Article
    '''
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return 'show_all' # a valid URL
        # return reverse('show_all') # lookup the URL called 'show_all'

        article = Article.objects.get(pk=self.kwargs['pk'])
        return reverse('article', kwargs={'pk': article.pk})
    
    def form_valid(self, form):
        '''This method is called after the form is validates before saving data to the database'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach this Article to the instance of the Comment to set its FK
        form.instance.article = article

        # delegate work to superclass version of this method
        return super().form_valid(form)
    
class RegistrationView(CreateView):
    '''
    A view to register a new user
    '''
    form_class = UserCreationForm
    template_name = 'blog/register.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return 'show_all' # a valid URL
        return reverse('show_all') # lookup the URL called 'show_all'

    def form_valid(self, form):
        '''This method is called after the form is validates before saving data to the database'''

        # delegate work to superclass version of this method
        response = super().form_valid(form)

        # log the user in
        login(self.request, self.object)

        # return the response
        return response