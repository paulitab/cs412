## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views    ## NEW
from .views import * # our view class definition

# define a list of valid URL patterns
urlpatterns = [
    path(r'', views.RandomArticleView.as_view(), name='random'), # NEW
    path(r'show_all', views.ShowAllView.as_view(), name='show_all'), # re-factor
    path(r'article/<int:pk>', views.ArticleView.as_view(), name='article'), # re-factor
    # path(r'create_comment', views.CreateCommentView.as_view(), name='create_comment'), # class 10/10
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'), # re-factoring the URL, changing how the URLs work
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    path('register/', views.RegistrationView.as_view(), name='register'), ## NEW
]