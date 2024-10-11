## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
urlpatterns = [
    path(r'', views.RandomArticleView.as_view(), name='random'), # NEW
    path(r'show_all', views.ShowAllView.as_view(), name='show_all'), # re-factor
    path(r'article/<int:pk>', views.ArticleView.as_view(), name='article'), # re-factor
    # path(r'create_comment', views.CreateCommentView.as_view(), name='create_comment'), # class 10/10
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'), # re-factoring the URL, changing how the URLs work
]