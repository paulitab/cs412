# restaurant/views.py
# Define the views for the restaurant app

from django.shortcuts import render, redirect
import random
import time
from datetime import timedelta, datetime 

# Create your views here.

def main(request):
    '''
    Display the main page with basic information about the restaurant. 
    This view simply directs the application to display the main.html template.
    '''

    template_name = "restaurant/main.html"

    return render(request, template_name)


def order(request):
    '''
    the view for the ordering page. 
    This view will need to create a “daily special” item (choose randomly from a list), and add it to the context dictionary for the page.
    Finally, delegate presentation to the order.html HTML template for display.
    '''
    template_name = "restaurant/order.html"

    # list of specials 
    specials = [
        'Spaghetti and Meatballs','Napolitan Pizza','Chicken Alfredo','Chicken Parmesan','Lasagna','Fettuccine Alfredo','Ravioli','Penne alla Vodka','Shrimp Scampi','Eggplant Parmesan','Chicken Marsala','Chicken Piccata','Chicken Francese','Chicken Cacciatore','Chicken Saltimbocca','Chicken Rollatini','Chicken Sorrentino','Chicken Scarpariello','Chicken Milanese','Chicken Florentine','Chicken Caprese','Chicken Bruschetta','Chicken Pizzaiola','Chicken Puttanesca','Chicken Tetrazzini','Chicken Saltimbocca'
    ]

        # list of specials 
    menu_prices = {
        'Spaghetti and Meatballs': 12.99,
        'Napolitan Pizza': 14.99,
        'Chicken Alfredo': 15.99,
        'Chicken Parmesan': 16.99,
        'Lasagna': 13.99,
        'Fettuccine Alfredo': 14.99,
        'Ravioli': 13.99,
        'Penne alla Vodka': 14.99,
        'Shrimp Scampi': 16.99,
        'Eggplant Parmesan': 13.99,
        'Chicken Marsala': 15.99,
        'Chicken Piccata': 15.99,
        'Chicken Francese': 15.99,
        'Chicken Cacciatore': 15.99,
        'Chicken Saltimbocca': 15.99,
        'Chicken Rollatini': 15.99,
        'Chicken Sorrentino': 15.99,
        'Chicken Scarpariello': 15.99,
        'Chicken Milanese': 15.99,
        'Chicken Florentine': 15.99,
        'Chicken Caprese': 15.99,
        'Chicken Bruschetta': 15.99,
        'Chicken Pizzaiola': 15.99,
        'Chicken Puttanesca': 15.99,
        'Chicken Tetrazzini': 15.99,
        'Chicken Saltimbocca': 15.99,
    }

    daily_special = specials[random.randint(0, len(specials)-1)]
    daily_special_price = menu_prices[daily_special]

    context = {
        'daily_special': daily_special,
        'daily_special_price': daily_special_price
    }

    return render(request, template_name, context)

def confirmation(request):
    '''
    The view to process the submission of an order, and display a confirmation page.
    We will implement this view as a custom view function 
    This view must check the form data to determine which items have been ordered, 
    and add these back to the context for the confirmation page. 
    In addition, the view must calculate the total price for the order – keep it simple, 
    but nonetheless add the items up; include this total in the order confirmation.
    Finally, delegate presentation to the confirmation.html HTML template for display.
    '''

    template_name = 'restaurant/confirmation.html'

    # menu prices
    menu_prices = {
        'Spaghetti and Meatballs': 12.99,
        'Napolitan Pizza': 14.99,
        'Chicken Alfredo': 15.99,
        'Chicken Parmesan': 16.99,
        'Lasagna': 13.99,
        'Fettuccine Alfredo': 14.99,
        'Ravioli': 13.99,
        'Penne alla Vodka': 14.99,
        'Shrimp Scampi': 16.99,
        'Eggplant Parmesan': 13.99,
        'Chicken Marsala': 15.99,
        'Chicken Piccata': 15.99,
        'Chicken Francese': 15.99,
        'Chicken Cacciatore': 15.99,
        'Chicken Saltimbocca': 15.99,
        'Chicken Rollatini': 15.99,
        'Chicken Sorrentino': 15.99,
        'Chicken Scarpariello': 15.99,
        'Chicken Milanese': 15.99,
        'Chicken Florentine': 15.99,
        'Chicken Caprese': 15.99,
        'Chicken Bruschetta': 15.99,
        'Chicken Pizzaiola': 15.99,
        'Chicken Puttanesca': 15.99,
        'Chicken Tetrazzini': 15.99,
        'Chicken Saltimbocca': 15.99,
    }
    
    # print(request)

    # check that we have a POST request
    if request.POST:

        # print(request.POST)

        # read the form data into python variables
        name = request.POST['name']
        # get the list of items ordered
        ordered_items = request.POST.getlist('items')
        total_price = 0

        # calculate the total price based on the selected items
        for item in ordered_items:
            if item in menu_prices:
                total_price += menu_prices[item]

        # calculate the time the order will be ready
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        
        # package the form data up as context variables for the template
        context = {
            'name' : name,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%I:%M %p'),
        }

        return render(request, template_name, context)
    
    ## handle GET request on this URL
    # redirect to the correct URL:
    return redirect('order')


