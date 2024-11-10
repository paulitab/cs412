from typing import Any
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

import plotly
import plotly.graph_objects as go

# Create your views here.
class VoterListView(ListView):
    '''View to display marathon results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 50 # show 50 results per page


    def get_queryset(self):
        '''Milit the results to a small number of records'''
        
        # default query set is all of the records
        qs = super().get_queryset()
        # return qs[:25] # limit to 25 records

        # handle search form/URL parameters:
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            # filter the Results by this parameter
            qs = Voter.objects.filter(city__icontains=city) #case insensitive

        return qs


