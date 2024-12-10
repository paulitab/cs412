# project/views.py
# define the views for the mini_fb app
from typing import Any
from django.shortcuts import redirect, render

# Create your views here.
# import generic views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.db.models import Avg, Max, Min, Count

# import models
from .models import *
from .forms import *

# graphing imports
import pandas as pd
import plotly.express as px
from django.utils.safestring import mark_safe

# main bakery view
class MainBakeryView(ListView):
    '''
    MainBakeryView will display all of the bakery goods and link to the blog and recipes
    Delegate the work to the template main_bakery.html to display
    '''
    model = BakeryGood # the model to display
    template_name = 'project/main_bakery.html'
    context_object_name = 'bakery_goods' # the name of the list of objects for the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_recipes'] = Recipe.objects.order_by('-difficulty_level')[:5]
        context['top_items'] = BakeryGood.objects.order_by('-price')[:5]
        context['top_reviews'] = Review.objects.order_by('-timestamp')[:5]
        return context

# show all recipes view
class ShowAllRecipesView(LoginRequiredMixin, ListView):
    '''
    ShowAllRecipesView will display all of the recipes
    Delegate the work to the template show_all_recipes.html to display
    '''
    model = Recipe # the model to display
    template_name = 'project/show_all_recipes.html'
    context_object_name = 'recipes' # the name of the list of objects for the template
    paginate_by = 2 # show 2 recipes per page

    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_queryset(self):
        '''Allow filtering recipes based on search parameters'''

        queryset = Recipe.objects.all()

        # Add filter logic based on query parameters (difficulty, name and ingredients)
        difficulty = self.request.GET.get('difficulty')
        name = self.request.GET.get('name')
        ingredients = self.request.GET.get('ingredients')

        if difficulty and difficulty != '':
            print(f"Filtering by difficulty: {difficulty}")
            queryset = queryset.filter(difficulty_level=difficulty)
            print(f"Filtered queryset: {queryset}")
        if name and name.lower != 'none':
            queryset = queryset.filter(name__icontains=name)
        if ingredients and ingredients.lower != 'none':
            queryset = queryset.filter(recipeingredient__ingredient__name__icontains=ingredients)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name')
        context['ingredients'] = self.request.GET.get('ingredients')
        context['difficulty'] = self.request.GET.get('difficulty')
        return context 

# show one recipe view
class ShowRecipePageView(LoginRequiredMixin, DetailView):
    '''
    Use this view to obtain data for one Recipe record, 
    and to delegate work to a template called show_recipe.html to display that Recipe.
    '''
    model = Recipe # the model to display
    template_name = 'project/show_recipe.html'
    context_object_name = 'recipe'

    def get_object(self):
        '''Locate and return the Recipe associated with this User'''
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

# show blog view
class ShowBlogView(ListView):
    '''
    ShowBlogView will display the blog
    Delegate the work to the template show_blog.html to display
    '''
    model = BlogPost # the model to display
    template_name = 'project/blog.html'
    context_object_name = 'posts' # the name of the list of objects for the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateBlogPostForm()  # Form to create a new blog post
        return context

    def get_login_url(self):
        return reverse('login')
    
# create blog post view
class CreateBlogPostView(LoginRequiredMixin, CreateView):
    '''
    A view to create a new blog post.
    '''
    model = BlogPost
    form_class = CreateBlogPostForm
    template_name = 'project/create_blog_post.html'

    def form_valid(self, form):
        '''
        Automatically set the author of the blog post to the logged-in user.
        '''
        # Attach the logged-in user as the author
        form.instance.author = self.request.user.userprofile  # Assuming UserProfile is linked to User
        return super().form_valid(form)

    def get_success_url(self):
        '''
        Redirect to the blog page after successfully creating a post.
        '''
        return reverse('show_blog')
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

# show all bakery goods view
class ShowAllBakeryGoodsView(ListView):
    '''
    ShowAllBakeryGoodsView will display all of the bakery goods
    Delegate the work to the template show_all_bakery_goods.html to display
    '''
    model = BakeryGood # the model to display
    template_name = 'project/show_all_bakery_goods.html'
    context_object_name = 'bakery_goods' # the name of the list of objects for the template

# show all orders view
class ShowAllOrdersView(LoginRequiredMixin, ListView):
    '''
    ShowAllOrdersView will display all of the orders
    Delegate the work to the template show_all_orders.html to display
    '''
    model = Order # the model to display
    template_name = 'project/show_all_orders.html'
    context_object_name = 'orders' # the name of the list of objects for the template

    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

# show all users view
class ShowAllProfilesView(LoginRequiredMixin, ListView):
    '''
    ShowAllUsersView will display all of the users
    Delegate the work to the template show_all_profiles.html to display
    '''
    model = UserProfile # the model to display
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles' # the name of the list of objects for the template

    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

# show one profile
class ShowProfilePageView(LoginRequiredMixin, DetailView):
    '''
    Use this view to obtain data for one Profile record, 
    and to delegate work to a template called show_profile_page.html to display that Profile.
    '''
    model = UserProfile # the model to display
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(UserProfile, pk=self.kwargs['pk'])
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    # Implement the get_context_data method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the profile based on the primary key in the URL
        profile = self.get_object()
        
        # Add the profile's review messages to the context
        context['review_messages'] = Review.objects.filter(profile=profile)
        return context

# register profile view
class RegisterProfileView(CreateView):
    '''
    RegisterProfileView will display a form to register a new user
    Delegate the work to the template register_profile.html to display
    '''
    # model = UserProfile # the model to display
    # template_name = 'project/register_profile.html'
    # fields = ['first_name', 'last_name', 'address', 'email'] # the fields to display in the form
    # success_url = '/' # the URL to redirect to after a successful form submission
    
    form_class = CreateProfileForm
    template_name = 'project/register_profile.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.object.pk}) 
    
    # create an instance of the UserCreationForm and store this instance in the context data. 
    def get_context_data(self, **kwargs: Any) -> Any:
        '''Add the UserCreationForm to the context data to pass it to the template'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
     
    def form_valid(self, form):
        '''This method is called after the form is validated but before saving the data to the database.'''
        # Reconstruct the UserCreationForm instance from the self.request.POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            # Attach the User to the Profile
            form.instance.user = user
            # Save the Profile and delegate to the superclass
            return super().form_valid(form)
        else:
            # If the user form is not valid, re-render the form with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

# update profile view
# Create a class-based view called UpdateProfileView, which inherits from the generic UpdateView class. 
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''
    A view to update a Profile but not the first name or last name
    '''
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return the URL corresponding to the profile page for whom the Profile was updated.
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()  # Add the profile to the context
        return context
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(UserProfile, user=self.request.user)

# Create an order view
class CreateOrderView(LoginRequiredMixin, CreateView):
    '''
    CreateOrderView will allow a logged-in user to create a new order.
    '''
    model = Order
    template_name = 'project/create_order.html'
    fields = ['status']

    def form_valid(self, form):
        # Attach the logged-in user's profile to the order
        form.instance.userProfile = get_object_or_404(UserProfile, email=self.request.user.email)
        form.instance.status = 'cart'  # Default to "cart" status
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the page where the user can add items to the order
        return reverse('add_to_order', kwargs={'order_id': self.object.id})

class AddToOrderView(LoginRequiredMixin, CreateView):
    '''
    Add items to the order
    If no order "in cart" status exists, create a new one, otherwise add the item to the existing order.
    '''
    model = OrderItem
    template_name = 'project/add_to_order.html'
    fields = ['bakery_good', 'quantity']
    login_url = '/login/'

    def form_valid(self, form):
        # Get the user profile
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            # Handle the case where the user does not have a profile
            raise Exception("UserProfile not found for the logged-in user.")

        # Check if there is an existing order with status 'in cart'
        order = Order.objects.filter(userProfile=user_profile, status='in cart').first()

        if not order:
            # No "in cart" order exists, create a new one
            order = Order.objects.create(
                userProfile=user_profile,
                status='in cart',
                order_date=now(),
            )

        # Assign this order to the item being created
        form.instance.order = order

        # Save the OrderItem instance
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the user profile
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            user_profile = None
        # Get the current 'in cart' order for this user
        order = Order.objects.filter(userProfile=user_profile, status='in cart').first()
        context['current_order'] = order  # Pass the order to the template
        context['order_items'] = order.orderitem_set.all() if order else None  # Pass order items
        return context

    def get_success_url(self):
        # Redirect back to showing all this users orders
        return reverse('show_all_user_orders')
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
                           
# view to display all orders for a user
class ShowAllUserOrdersView(LoginRequiredMixin, ListView):
    '''
    UserOrdersView will display all orders for the logged-in user.
    '''
    model = Order
    template_name = 'project/show_all_user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Filter orders by the logged-in user's profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return Order.objects.filter(userProfile=user_profile)
    
# View to mark an order as "pending"
class MarkOrderPendingView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        # Fetch the order
        order = get_object_or_404(Order, id=order_id, userProfile__user=request.user)

        # Change status to "pending" if it's in cart
        if order.status == "in cart":
            order.status = "pending"
            order.save()

        # Redirect back to the "Your Orders" page
        return HttpResponseRedirect(reverse('show_all_user_orders'))
    
# Create a class CreateFriendView, which inherits from the generic superclass django.views.generic.View. 
class CreateFriendView(LoginRequiredMixin, CreateView):
    '''
    A view to create a Friend relationship
    '''
    # form_class = CreateFriendForm
    # template_name = 'project/add_friend_form.html'
    
    # Implement/override the dispatch method, in which we can read the URL parameters (from self.kwargs), use the object manager to find the requisite Profile objects, and then call the Profile‘s add_friend method (from step 2, above). Finally, we can redirect the user back to the profile page.
    def dispatch(self, request, *args, **kwargs):
        '''
        Dispatch the request to the appropriate method based on the request method.
        '''
        # get the Profile objects
        # profile1 = Profile.objects.get(pk=self.kwargs['pk'])
        # profile2 = Profile.objects.get(pk=self.kwargs['other_pk'])
        # Get the Profile of the logged-in user
        profile1 = get_object_or_404(UserProfile, user=request.user)
        # Get the Profile of the other user using the 'other_pk' from the URL
        profile2 = get_object_or_404(UserProfile, pk=self.kwargs['other_pk'])
        # call the add_friend method
        profile1.add_friend(profile2)
        # redirect the user back to the profile page
        return redirect('show_profile', pk=profile1.pk)
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# Create a class-based view called ShowFriendSuggestionsView, which inherits from the generic DetailView class.
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''
    A view to show friend suggestions
    '''
    model = UserProfile
    template_name = 'project/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        '''Locate and return the Profile associated with this User'''
        return get_object_or_404(UserProfile, user=self.request.user)


# views for the review comments

class CreateReviewView(LoginRequiredMixin, CreateView):
    '''
    A view to create a Review comment
    '''
    form_class = CreateReviewForm
    template_name = 'project/create_review_form.html'

    # first complication: Implementing get_context_data method
    def get_context_data(self, **kwargs):
        # The attribute self.kwargs is a dictionary of any URL parameters, and the value self.kwargs['pk'] is the primary key of the UserProfile corresponding to the URL pattern.
        '''
        Add the Profile to the context data so that the template can use it to display the Profile's name.
        '''
        # Within get_context_data method, create a context dictionary, add the Profile object (call the context variabale profile, for consistency with how things worked on other pages).
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    # Second complication: Implementing the form_valid method
    # To solve this problem, we will need to implement the special method form_valid on the CreateReviewView class.
    def form_valid(self, form):
        '''
        This method is called after the form is validated but before saving the data to the database.
        '''
        # look up the Profile object by its pk. You can find this pk in self.kwargs['pk'].
        profile = UserProfile.objects.get(user=self.request.user)
        # attach this object to the profile attribute of the review.
        form.instance.profile = profile

        # save the review to database
        review = form.save()

        # Print a message to confirm the review has been saved
        print(f"Review saved: {review.message}")

        # delegate work to the superclass version of this method.
        return super().form_valid(form)

    # Third complication: Implementing the get_success_url method
    # To solve this problem, we will need to implement the special method get_success_url on the CreateReviewView class.
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return the URL corresponding to the profile page for whom the Review was added.
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# Create a class DeleteStatusMessageView, which inherits from the generic DeleteView class. 
# Set the model, template_name and context_object_name attributes as you have done in the past when using other generic views.
class DeleteReviewView(LoginRequiredMixin, DeleteView):
    '''
    A view to delete a Review, overriding some of the default behavior of the generic DeleteView.
    '''
    model = Review
    template_name = 'project/delete_review_form.html'
    context_object_name = 'review'

    # Implement the get_success_url method
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # Override the get_success_url(self) method, so that when a StatusMessage is deleted, the user is redirected to the profile page for whom the status message was deleted.
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # assignment 9: review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# create a new class UpdateReviewView, which inherits from the generic UpdateView class.
# Set the model, form_class, and template_name attributes as you have done in the past when using other generic views.
class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'project/update_review_form.html'

    def get_success_url(self):
        '''
        After updating, redirect to the profile page of the user who created the review.
        '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    # review the create update delete so only logged in users can do them
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
# statistics for the bakery abpout recipes and ingredients models
class RecipeStatisticsView(LoginRequiredMixin, TemplateView):
    """
    A view to display aggregate statistics about recipes and ingredients.
    With a focus on difficulty levels and ingredient usage.
    Graphs are generated using Plotly and displayed in the template.
    """
    model = Recipe
    template_name = 'project/recipe_statistics.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recipe statistics
        total_recipes = Recipe.objects.count()
        average_difficulty = Recipe.objects.aggregate(Avg('difficulty_level'))['difficulty_level__avg']
        max_difficulty = Recipe.objects.aggregate(Max('difficulty_level'))['difficulty_level__max']
        min_difficulty = Recipe.objects.aggregate(Min('difficulty_level'))['difficulty_level__min']
        difficulty_counts = Recipe.objects.values('difficulty_level').annotate(count=Count('id'))

        # Ingredient statistics
        total_ingredients = RecipeIngredient.objects.count()
        ingredient_counts = RecipeIngredient.objects.values('ingredient__name').annotate(count=Count('id'))

        context['total_ingredients'] = Ingredient.objects.count()
        context['most_common_ingredients'] = (
            RecipeIngredient.objects.values('ingredient__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        context['ingredient_usage'] = (
            RecipeIngredient.objects.values('ingredient__name')
            .annotate(total_used=Count('id'))
            .order_by('-total_used')
        )

        # Create Two DataFrames for Plotly
        recipe_df = pd.DataFrame.from_records(difficulty_counts)
        ingredient_df = pd.DataFrame.from_records(ingredient_counts)

        # Generate graphs
        # Recipes by Difficulty Level
        difficulty_bar_chart = px.bar(
            recipe_df,
            x='difficulty_level',
            y='count',
            title='Recipes by Difficulty Level',
            labels={'difficulty_level': 'Difficulty Level', 'count': 'Number of Recipes'},
        )
        context['difficulty_graph'] = mark_safe(difficulty_bar_chart.to_html(full_html=False))

        # Ingredient Usage
        if not ingredient_df.empty:
            ingredient_pie_chart = px.pie(
                ingredient_df,
                names='ingredient__name',
                values='count',
                title='Ingredient Usage Distribution',
            )
            context['ingredient_graph'] = mark_safe(ingredient_pie_chart.to_html(full_html=False))
        else:
            context['ingredient_graph'] = None

        # Add summary statistics to context
        context.update({
            'total_recipes': total_recipes,
            'average_difficulty': round(average_difficulty, 2) if average_difficulty else None,
            'max_difficulty': max_difficulty,
            'min_difficulty': min_difficulty,
            'total_ingredients': total_ingredients,
        })

        context['recipes_per_level'] = Recipe.objects.values('difficulty_level').annotate(count=Count('id')).order_by('difficulty_level')

        return context