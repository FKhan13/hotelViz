import re
import json

from django.shortcuts import render, render_to_response
from django.views import generic
from django.db import connection

from django.http import Http404

from .forms import BarForm, MotionForm
from viz.models import Countries


# Data Types
numeric = ['visitor_hist_starrating', 'visitor_hist_adr_usd', 'prop_starrating',
           'prop_review_score',
           'prop_location_score1', 'prop_location_score2', 'prop_log_historical_price', 'price_usd',
           'srch_length_of_stay',
           'srch_booking_window', 'srch_adults_count', 'srch_children_count', 'srch_room_count',
           'srch_query_affinity_score',
           'orig_destination_distance', 'gross_bookings_usd']
identifiers = ['srch_id', 'site_id', 'visitor_location_country_id', 'prop_country_id', 'prop_id', 'position',
               'srch_destination_id']
booleans = ['prop_brand_bool', 'promotion_flag', 'srch_saturday_night_bool', 'random_bool', 'click_bool',
            'booking_bool']
filters = ['price_usd', 'visitor_hist_starrating', 'prop_starrating', 'prop_review_score']
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

    if chart_type == "bar":
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = BarForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # redirect to a new URL:
                # Will have to incorporate logic for deciding if graph that is selected is applicable to be drawn and will sort through form data
                chart = form.cleaned_data['type']

                if chart == 'bar':
                    # Determine what type of filter has been selected and its name
                    filter_string = ""
                    filter_type = ""
                    filter_name = ""  # Only used if the filter is a numerical integer
                    # Handle the case where the filter is a boolean type
                    if form.cleaned_data['boolean_filters'] != '':
                        filter_string = form.cleaned_data['boolean_filters']
                        filter_type = "bool"
                    # handle the case when the filter is either an integer or a float
                    else:
                        for f in filters:
                            if form.cleaned_data[f] is not None:
                                filter_string = form.cleaned_data[f]
                                if isinstance(filter_string, int):
                                    filter_type = "int"
                                    filter_name = f
                                    break
                                else:
                                    filter_type = "float"
                                    break

                    # Find country
                    country = country.replace('_', ' ')
                    country_object = Countries.objects.get(a_name=country)
                    country_id = country_object.name

                    # create query and render the graph
                    columns = form.cleaned_data['fields']
                    bar(columns, country_id, filter_string, filter_type, filter_name)
                    return render_to_response('viz/bar.html')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = BarForm(initial={'type': chart_type})

        return render(request, 'viz/filter_bar.html',
                      {'form': form, 'chart_type': chart_type, 'hotel_characteristics_loop': range(1, 10),
                       'visitor_information_loop': range(10, 15), 'srch_characteristics_loop': range(15, 25),
                       'booking_characteristics_loop': range(25, 28)})

    else:
        raise Http404("Could not determine chart type")


def motion(request, country):
    chart_type = request.GET.get('chartType')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MotionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render_to_response('viz/motion.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MotionForm()

    return render(request, 'viz/filter_motion.html', {'form': form})


def bar(fields, country, filter_string, filter_type, filter_name):
    if isinstance(fields, str):
        print(fields)
    field_string = re.sub("[\[\]\']", '', str(fields))
    columns = field_string.split(", ")

    # Bar charts should only be created for 1 column vs another
    if columns.__len__() != 2:
        raise Http404("There are more than two columns selected - A bar chart is not applicable to be created")

    graph_type = ""
    x = None
    y = None

    if columns[0] and columns[1] in numeric:
        graph_type = "NumNum"
        x = columns[0]
        y = columns[1]
    elif columns[0] in numeric and columns[1] in identifiers:
        graph_type = "NumNum"
        x = columns[1]
        y = columns[0]
    elif columns[0] in identifiers and columns[1] in numeric:
        graph_type = "NumNum"
        x = columns[0]
        y = columns[1]
    elif columns[0] in booleans and columns[1] in numeric:
        graph_type = "NumBool"
        x = columns[0]
        y = columns[1]
    elif columns[0] in numeric and columns[1] in booleans:
        graph_type = "NumBool"
        x = columns[1]
        y = columns[0]
    elif columns[0] in booleans and columns[1] in identifiers:
        graph_type = "BoolIdent"
        x = columns[0]
        y = columns[1]
    elif columns[0] in identifiers and columns[1] in booleans:
        graph_type = "BoolIdent"
        x = columns[1]
        y = columns[0]
    elif columns[0] and columns[1] in booleans:
        graph_type = "BoolBool"
        x = columns[0]
        y = columns[1]
    else:
        raise Http404("Could not determine graph type")

    query = create_query(x, y, graph_type, country, filter_string, filter_type, filter_name)
    collect_from_db_and_write_to_file_bar(query)

    # , {'config': config_list})


def collect_from_db_and_write_to_file_bar(query):
    cur = connection.cursor()
    cur.execute(query)
    db_columns = cur.fetchone()[0]

    if db_columns is None:
        raise Http404("There are no results matching the given parameters")

    with open("viz/static/viz/js/result.json", "w") as fp:
        json.dump(db_columns, fp)

    cur.close()
    connection.close()


def create_query(x, y, graph_type, country, filter_string, filter_type, filter_name):
    query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + x + " AS xCord," + y + " AS yCord FROM viz_bigtable WHERE "

    if graph_type == "NumNum":
        append = x + " IS NOT NULL AND " + y + " IS NOT NULL AND "
        query += append
    elif graph_type == "NumBool":
        append = x + "= TRUE AND " + y + " IS NOT NULL AND "
        query += append
    elif graph_type == "BoolIdent":
        append = x + " IS NOT NULL AND " + y + "= TRUE AND "
        query += append
    elif graph_type == "BoolBool":
        append = x + "= TRUE AND " + y + "= TRUE AND "
        query += append
    else:
        raise Http404("Graph type is incorrect")

    if filter_type == "bool":
        append = filter_string + "= TRUE AND "
        query += append
    elif filter_type == "int":
        if filter_name == "":
            raise Http404("Could not determine filter name")
        filter_upper = filter_string + 0.5
        filter_lower = filter_string - 0.5
        append = filter_name + " >= " + str(filter_lower) + " AND " + filter_name + " <= " + str(
            filter_upper) + " AND "
        query += append
    elif filter_type == "float":
        filter_upper = filter_string + 100
        filter_lower = filter_string - 100
        append = "price_usd >= " + str(filter_lower) + " AND " + "price_usd <= " + str(filter_upper) + " AND "
        query += append
    else:
        raise Http404("Could not determine filter type")

    append = "prop_country_id = " + str(country) + ") t"
    query += append

    return query
