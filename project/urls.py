## project/urls.py
## description: URL patterns for the project app

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

# define a list of valid URL patterns
urlpatterns = [
    # home path
    path(r'', views.MainBakeryView.as_view(), name='main_bakery'),
    # path to show all recipes
    path(r'recipes/', views.ShowAllRecipesView.as_view(), name='show_all_recipes'),
    # path to show one recipe
    path(r'recipe/<int:pk>', views.ShowRecipePageView.as_view(), name='show_recipe'),
    # path to show blog
    path(r'blog/', views.ShowBlogView.as_view(), name='show_blog'),
    # path to show all bakery goods
    path(r'bakery_goods/', views.ShowAllBakeryGoodsView.as_view(), name='show_all_bakery_goods'),
    # path to show all orders
    path(r'orders/', views.ShowAllOrdersView.as_view(), name='show_all_orders'),
    # path to show all profiles
    path(r'users/', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    # path to one profile
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    # register path
    path(r'register/', views.RegisterProfileView.as_view(), name='register'),
    # path to update a profile
    path(r'profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    # Create a new URL pattern: 'profile/add_friend/<int:other_pk>'. 
    path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    # Create a new URL pattern: 'profile/friend_suggestions' and associate it with the ShowFriendSuggestionsView.
    path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    # login and logout path
    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logout.html', next_page='show_all_profiles'), name="logout"),
    # path to create an order
    path(r'create_order/', views.CreateOrderView.as_view(), name='create_order'),
    # path to add an item to an order
    path(r'add_to_order/', views.AddToOrderView.as_view(), name='add_to_order'),
    # path to show all user orders
    path(r'show_all_user_orders/', views.ShowAllUserOrdersView.as_view(), name='show_all_user_orders'),
    # Mark an order as pending
    path('mark_order_pending/<int:order_id>/', views.MarkOrderPendingView.as_view(), name='mark_order_pending'),
    # Create a URL mapping to route requests from the URL pattern 'profile/review/create_review', associate it with the CreateReviewView, and name this URL create_review.
    path(r'profile/review/create_review', views.CreateReviewView.as_view(), name='create_review'),
    # Create a URL mapping to route requests from the URL pattern 'profile/<int:pk>/delete_review/', associate it with the DeleteReviewView, and name this URL delete_review.
    path(r'profile/review/<int:pk>/delete', views.DeleteReviewView.as_view(), name='delete_review'),
    # Create a URL mapping to route requests from the URL patterns 'profile/<int:pk>/update_review/', associate it with the UpdateReviewView, and name this URL update_review.
    path(r'profile/review/<int:pk>/update', views.UpdateReviewView.as_view(), name='update_review'),
    # Create a URL mapping to route requests from the URL pattern 'profile/<int:pk>/create_blog_post/', associate it with the CreateBlogPostView, and name this URL create_blog_post.
    path(r'profile/create_blog_post', views.CreateBlogPostView.as_view(), name='create_blog_post'),
    # Create a URL mapping to route requests from the URL pattern 'recipe/statistics/', associate it with the RecipeStatisticsView, and name this URL recipe_statistics.
    path('recipes/statistics/', views.RecipeStatisticsView.as_view(), name='recipe_statistics'),
]
