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


class ExploreView(generic.TemplateView):
    template_name = "viz/explore.html"


class SetView(generic.TemplateView):
    template_name = "viz/set.html"


def selection(request, country):
    return render_to_response('viz/selection.html', {"country": country})


# view that allows user to select fields that should be plotted for a graph
def field(request, country):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BarForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
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
        form = BarForm()

    return render(request, 'viz/filter_bar.html',
                  {'form': form, 'hotel_characteristics_loop': range(1, 9),
                   'visitor_information_loop': range(9, 13), 'srch_characteristics_loop': range(13, 23),
                   'booking_characteristics_loop': range(23, 26)})


def motion(request, country):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MotionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data['name'] in identifiers:
                name = form.cleaned_data['name']
            else:
                raise Http404("Name is of the incorrect type")
            if form.cleaned_data['circum_color'] in numeric:
                circum_color = form.cleaned_data['circum_color']
            else:
                raise Http404("Circumference color is of the incorrect type")

            radius_val = form.cleaned_data['radius']
            y = form.cleaned_data['y']
            x = form.cleaned_data['x']

            # Find country
            country = country.replace('_', ' ')
            country_object = Countries.objects.get(a_name=country)
            country_id = country_object.name

            query = create_query_motion(name, circum_color, radius_val, y, x, country_id)
            collect_from_db_and_write_to_file(query)

            y_type = ""
            x_type = ""
            rad_type = ""
            # [{"xaxis":"Review Score", "yaxis":"User Rating", "xmax":"5","ymax":"20000", "ytype":"bool", "xtype":"num", "radType":"num"}]
            if y in numeric:
                y_type = "num"
            elif y in booleans:
                y_type = "bool"
            if x in numeric:
                x_type = "num"
            elif x in booleans:
                x_type = "bool"
            if radius_val in numeric:
                rad_type = "num"
            elif radius_val in booleans:
                rad_type = "bool"

            ymax = find_max_big_table(y, country_id)
            xmax = find_max_big_table(x, country_id)

            config = {"xaxis": x, "yaxis": y, "xmax": xmax, "ymax": ymax, "ytype": y_type, "xtype": x_type,
                      "radtype": rad_type}
            write_config(config)

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
        graph_type = "numnum"
        x = columns[0]
        y = columns[1]
    elif columns[0] in numeric and columns[1] in identifiers:
        graph_type = "numnum"
        x = columns[1]
        y = columns[0]
    elif columns[0] in identifiers and columns[1] in numeric:
        graph_type = "numnum"
        x = columns[0]
        y = columns[1]
    elif columns[0] and columns[1] in identifiers:
        graph_type = "numnum"
        x = columns[0]
        y = columns[1]
    elif columns[0] in booleans and columns[1] in numeric:
        graph_type = "numbool"
        x = columns[1]
        y = columns[0]
    elif columns[0] in numeric and columns[1] in booleans:
        graph_type = "numbool"
        x = columns[0]
        y = columns[1]
    elif columns[0] in booleans and columns[1] in identifiers:
        graph_type = "numbool"
        x = columns[1]
        y = columns[0]
    elif columns[0] in identifiers and columns[1] in booleans:
        graph_type = "numbool"
        x = columns[0]
        y = columns[1]
    else:
        raise Http404("Could not determine graph type")

    query = create_query_bar(x, y, graph_type, country, filter_string, filter_type, filter_name)
    collect_from_db_and_write_to_file(query)

    config = {"xaxis": x, "yaxis": y, "type": graph_type}
    write_config(config)


def collect_from_db_and_write_to_file(query):
    cur = connection.cursor()
    cur.execute(query)
    db_columns = cur.fetchone()[0]

    if db_columns is None:
        raise Http404("There are no results matching the given parameters")

    with open("viz/static/viz/js/result.json", "w") as fp:
        json.dump(db_columns, fp)

    cur.close()
    connection.close()


def write_config(config):
    with open("viz/static/viz/js/config.json", "w") as fp:
        json.dump(config, fp)


def find_max_big_table(column, country):
    query = "SELECT MAX(" + column + ") FROM (SELECT " + column + " FROM viz_bigtable WHERE prop_country_id = " + country + ") t"

    cur = connection.cursor()
    cur.execute(query)
    maximum = cur.fetchone()[0]

    if maximum is None:
        raise Http404("Could not determine the max value for the column")
    else:
        return maximum


def create_query_motion(name, circum_color, radius_val, y, x, country):
    query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT " + name + " as name, " + circum_color + \
            " as circumColor, " + radius_val + " as radiusVal, " + "date_time at time zone 'UTC' as date, " + y + \
            " AS ycord, " + x + " AS xcord FROM viz_bigtable WHERE " + name + " IS NOT NULL AND " + circum_color + \
            " IS NOT NULL AND "

    if radius_val in numeric:
        append = radius_val + " IS NOT NULL AND "
        query += append
    elif radius_val in booleans:
        append = radius_val + " = TRUE AND "
        query += append
    else:
        raise Http404("Radius Value is of the incorrect type")
    if y in numeric:
        append = y + " IS NOT NULL AND "
        query += append
    elif y in booleans:
        append = y + " = TRUE AND "
        query += append
    else:
        raise Http404("Y Value is of the incorrect type")
    if x in numeric:
        append = x + " IS NOT NULL AND "
        query += append
    elif x in booleans:
        append = x + " = TRUE AND "
        query += append
    else:
        raise Http404("X Value is of the incorrect type")

    append = "prop_country_id = " + str(country) + " ) t;"
    query += append

    return query


def create_query_bar(x, y, graph_type, country, filter_string, filter_type, filter_name):
    query = "SELECT array_to_json(array_agg(row_to_json(t))) AS id FROM (SELECT date_time at time zone 'UTC'," + x + \
            " AS xCord," + y + " AS yCord FROM viz_bigtable WHERE "

    if graph_type == "numnum":
        append = x + " IS NOT NULL AND " + y + " IS NOT NULL AND "
        query += append
    elif graph_type == "numbool":
        append = y + "= TRUE AND " + x + " IS NOT NULL AND "
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
