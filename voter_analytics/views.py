from typing import Any
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import datetime
import pandas as pd
import plotly.express as px
from django.utils.safestring import mark_safe

# Create your views here.
class VoterListView(ListView):
    '''View to display marathon results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 # show 50 results per page

    def get_queryset(self):
        '''Limit the voters to a small number of records'''
        queryset = Voter.objects.all()
        # Add filter logic based on query parameters (e.g., party, birth date, voter score, etc.)
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # If min_dob is provided, convert it to January 1 of that year
        if min_dob:
            min_dob_date = datetime.strptime(min_dob, "%Y").replace(month=1, day=1)
            queryset = queryset.filter(date_of_birth__gte=min_dob_date)

        # If max_dob is provided, convert it to December 31 of that year
        if max_dob:
            max_dob_date = datetime.strptime(max_dob, "%Y").replace(month=12, day=31)
            queryset = queryset.filter(date_of_birth__lte=max_dob_date)

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adding years from 1900 to 2023 to context
        context['years'] = list(range(1900, 2024))

        # voter scores
        context['voter_scores'] = [0, 1, 2, 3, 4, 5]
        
        # Adding the elections list to context
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        
        return context
    
# Create a DetailView to show a page for a single Voter record.
class VoterDetailView(DetailView):
    '''Display a single Voter on its own page'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

# Create a View to display graphs of voter data
class VoterGraphsView(ListView):
    '''View to display graphs of voter data'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filter Voters based on form inputs
        voters = self.get_queryset()  # Adjust if you need specific filtering logic
        
        # Create DataFrames for Plotly
        df = pd.DataFrame.from_records(voters.values('date_of_birth', 'party_affiliation', 'v20state', 'v21town', 'v21primary', 'v22general', 'v23town'))
        
        # Histogram by Year of Birth
        df['year_of_birth'] = pd.to_datetime(df['date_of_birth']).dt.year
        birth_histogram = px.histogram(df, x='year_of_birth', title='Voter Birth Year Distribution', nbins=200)
        birth_histogram.update_xaxes(title_text="Birth Year")
        birth_histogram.update_yaxes(title_text="Number of Voters")
        context['birth_histogram'] = mark_safe(birth_histogram.to_html(full_html=False))
        
        # Pie chart by Party Affiliation
        party_pie_chart = px.pie(df, names='party_affiliation', title='Voter distribution by Party Affiliation')
        context['party_pie_chart'] = mark_safe(party_pie_chart.to_html(full_html=False))
        
        # Histogram by Election Participation
        election_columns = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = df[election_columns].sum().reset_index()
        election_counts.columns = ['Election', 'Count']
        election_histogram = px.bar(election_counts, x='Election', y='Count', title='Vote Count by Election')
        context['election_histogram'] = mark_safe(election_histogram.to_html(full_html=False))

        return context
    
    def get_queryset(self):
        '''Limit the voters to a small number of records'''
        queryset = Voter.objects.all()
        # Add filter logic based on query parameters (e.g., party, birth date, voter score, etc.)
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # If min_dob is provided, convert it to January 1 of that year
        if min_dob:
            min_dob_date = datetime.strptime(min_dob, "%Y").replace(month=1, day=1)
            queryset = queryset.filter(date_of_birth__gte=min_dob_date)

        # If max_dob is provided, convert it to December 31 of that year
        if max_dob:
            max_dob_date = datetime.strptime(max_dob, "%Y").replace(month=12, day=31)
            queryset = queryset.filter(date_of_birth__lte=max_dob_date)

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)
        
        return queryset



