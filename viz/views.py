from django.shortcuts import render, render_to_response
from django.views import generic
from django.db import connection
from .forms import SelectionForm
from django.http import Http404
from viz.models import BigTable
import psycopg2
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import re, json

# Data Types
numeric = ['visitor_location_country_id', 'visitor_hist_starrating', 'visitor_hist_adr_usd', 'prop_starrating',
           'prop_review_score',
           'prop_location_score1', 'prop_location_score2', 'prop_log_historical_price', 'price_usd',
           'srch_length_of_stay', 'srch_length_of_stay',
           'srch_booking_window', 'srch_adults_count', 'srch_children_count', 'srch_room_count',
           'srch_query_affinity_score',
           'orig_destination_distance', 'gross_bookings_usd']
identifiers = ['srch_id', 'site_id', 'visitor_location_country_id', 'prop_country_id', 'prop_id', 'position',
               'srch_destination_id']
booleans = ['prop_brand_bool', 'promotion_flag', 'srch_saturday_night_bool', 'random_bool', 'click_bool',
            'booking_bool']
competitor_info = ['comp1_rate', 'comp1_inv', 'comp1_rate_percent_diff', 'comp2_rate', 'comp2_inv',
                   'comp2_rate_percent_diff',
                   'comp3_rate', 'comp3_inv', 'comp3_rate_percent_diff', 'comp4_rate', 'comp4_inv',
                   'comp4_rate_percent_diff',
                   'comp5_rate', 'comp5_inv', 'comp5_rate_percent_diff', 'comp6_rate', 'comp6_inv',
                   'comp6_rate_percent_diff',
                   'comp7_rate', 'comp7_inv', 'comp7_rate_percent_diff', 'comp8_rate', 'comp8_inv',
                   'comp8_rate_percent_diff', ]


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "viz/index.html"


def selection(request, country):
    return render_to_response('viz/selection.html', {"country": country})


# view that allows user to select fields that should be plotted for a graph
def field(request, country):
    chart_type = request.GET.get('chartType')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SelectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # redirect to a new URL:
            # Will have to incorporate logic for deciding if graph that is selected is applicable to be drawn and will sort through form data
            return render_to_response('viz/bar.html', {"fields": form.cleaned_data['fields']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SelectionForm()

    return render(request, 'viz/filter.html', {'form': form})


def bar(request, fields):
    field_string = re.sub('[\[\]\']', '', fields)
    columns = field_string.split(", ")

    # Bar charts should only be created for 1 column vs another
    if columns.__len__() is not 2:
        raise Http404("There are more than two columns selected - A bar chart is not applicable to be created")
    # clasiifier = []
    #
    # if columns[0] and columns[1] in numeric or columns[0] in numeric and columns[1] in identifiers:
    #     clasiifier.append("NumNum")
    #     query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + columns[0] + " AS xCord," + columns[1] + " AS yCord FROM viz_bigtable WHERE " + columns[0] + " IS NOT NULL AND " + columns[1] + " IS NOT NULL) t"
    #     collect_from_db_and_write_to_file_bar(query)
    #
    # elif columns[0] in numeric and columns[1] in booleans:
    #     clasiifier.append("NumBool")
    #     query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + columns[1] + " AS xCord," + columns[0] + " AS yCord FROM viz_bigtable WHERE " + columns[1] + " = TRUE AND " + columns[0] + " IS NOT NULL) t"
    #     collect_from_db_and_write_to_file_bar(query)
    #
    # elif columns[0] in booleans and columns[1] in identifiers:
    #     clasiifier.append("BoolID")
    #     query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + columns[1] + " AS xCord," + columns[0] + " AS yCord FROM viz_bigtable WHERE " + columns[0] + " = TRUE AND " + columns[1] + " IS NOT NULL) t"
    #     collect_from_db_and_write_to_file_bar(query)
    #
    # elif columns[0] and columns[1] in booleans:
    #     clasiifier.append("BoolBool")
    #     query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + columns[0] + " AS xCord," + columns[1] + " AS yCord FROM viz_bigtable WHERE " + columns[0] + " = TRUE AND " + columns[1] + " = TRUE) t"
    #     collect_from_db_and_write_to_file_bar(query)
    #
    # config_list = list({'type': clasiifier[0], 'xaxis': columns[0], 'yaxis': columns[1]})

    return render_to_response('viz/bar.html')  # , {'config': config_list})


def collect_from_db_and_write_to_file_bar(query):
    cur = connection.cursor()
    cur.execute(query)
    db_columns = cur.fetchone()[0]

    with open("viz/static/viz/js/result.json", "w") as fp:
        json.dump(db_columns, fp)

    cur.close()
    connection.close()
