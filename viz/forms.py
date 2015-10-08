from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect


class BarForm(forms.Form):
    DBColumns = (
        # Hotel Characteristics
        ('prop_starrating', 'Hotel Star Rating'),
        ('prop_review_score', 'Hotel Review Score'), ('prop_brand_bool', 'Branded Hotels'),
        ('prop_location_score1', 'Hotel Location Popularity 1'),
        ('prop_location_score2', 'Hotel Location Popularity 2'),
        ('prop_log_historical_price', 'Hotel Historical Price in US Dollars'),
        ('price_usd', 'Hotel Price For A particular Search'),
        ('promotion_flag', 'Hotels That Were on Promotion'),
        # Visitor Information
        ('visitor_hist_starrating', 'Visitors Historical Star Rating'),
        ('visitor_hist_adr_usd', 'Visitors Historical Spending in US Dollars'), ('site_id', 'Website Searched From'),
        ('orig_destination_distance', 'The distance between the Visitors location to the Hotel location'),
        # Search Characteristics
        ('srch_id', 'Search Number'),
        ('srch_length_of_stay', 'Length of Stay Searched For'),
        ('srch_booking_window', 'The Amount of Time between when the Search was done to the Date of Stay'),
        ('srch_adults_count', 'Number of Adults Searched For'),
        ('srch_children_count', 'Number of Children Searched for'), ('srch_room_count', 'Number of Rooms Searched for'),
        ('srch_saturday_night_bool', 'Searches that were less than four days and included weekends'),
        ('srch_query_affinity_score', 'The log of the probability that a Hotel will be clicked on Internet Searches'),
        ('position', 'Hotel Position on Search Result Page'),
        ('random_bool', 'Searches that were randomly sorted'),
        # Booking Characteristics
        ('click_bool', 'Hotels that were Clicked'),
        ('gross_bookings_usd', 'Cost of the Bookings in US Dollars'), ('booking_bool', 'Hotels that were Booked'))

    booleans = (
        ('prop_brand_bool', 'Filter by branded hotels?'),
        ('promotion_flag', 'Filter by hotels that were on promotion?'),
        ('srch_saturday_night_bool', 'Filter by searches that were less than four days and included saturdays?'),
        ('random_bool', 'Filter by searches that were random?'),
        ('click_bool', 'Filter by search results that were clicked?'),
        ('booking_bool', 'Filter by search results that were booked?'))

    competitor_ota = (
        ('comp1_rate', 'Search results where the First Competitors rate was lower, higher or the same as Expedias'),
        ('comp1_inv', 'Search results where the First Competitors did not have availability in a Hotel'),
        ('comp1_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Ones booking rate'),
        ('comp2_rate', 'Search results where the Second Competitors rate was lower, higher or the same as Expedias'),
        ('comp2_inv', 'Search results where the Second Competitors did not have availability in a Hotel'),
        ('comp2_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Twos booking rate'),
        ('comp3_rate', 'Search results where the Third Competitors rate was lower, higher or the same as Expedias'),
        ('comp3_inv', 'Search results where the Third Competitors did not have availability in a Hotel'),
        ('comp3_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Threes booking rate'),
        ('comp4_rate', 'Search results where the Fourth Competitors rate was lower, higher or the same as Expedias'),
        ('comp4_inv', 'Search results where the Fourth Competitors did not have availability in a Hotel'),
        ('comp4_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Fours booking rate'),
        ('comp5_rate', 'Search results where the Fifth Competitors rate was lower, higher or the same as Expedias'),
        ('comp5_inv', 'Search results where the Fifth Competitors did not have availability in a Hotel'),
        ('comp5_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Fives booking rate'),
        ('comp6_rate', 'Search results where the Sixth Competitors rate was lower, higher or the same as Expedias'),
        ('comp6_inv', 'Search results where the Sixth Competitors did not have availability in a Hotel'),
        ('comp6_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Sixes booking rate'),
        ('comp7_rate', 'Search results where the Seventh Competitors rate was lower, higher or the same as Expedias'),
        ('comp7_inv', 'Search results where the Seventh Competitors did not have availability in a Hotel'),
        ('comp7_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Sevens booking rate'),
        ('comp8_rate', 'Search results where the Eighth Competitors rate was lower, higher or the same as Expedias'),
        ('comp8_inv', 'Search results where the Eighth Competitors did not have availability in a Hotel'),
        ('comp8_rate_percent_diff',
         'The percentage difference between Expedias booking rate and Competitor Eights booking rate'),)

    fields = forms.MultipleChoiceField(choices=DBColumns, required=True, widget=CheckboxSelectMultiple)
    boolean_filters = forms.ChoiceField(choices=booleans, required=False, widget=RadioSelect)
    price_usd = forms.FloatField(label='Filter by hotel price', min_value=0, required=False)
    visitor_hist_starrating = forms.IntegerField(label='Filter by users average star rating awarded?', min_value=0,
                                                 max_value=5, required=False)
    prop_review_score = forms.IntegerField(label='Filter by hotel review score?', min_value=0, max_value=5,
                                           required=False)
    prop_starrating = forms.IntegerField(label='Filter by hotel star rating?', min_value=0, max_value=5, required=False)


class MotionForm(forms.Form):
    identifiers = (('srch_id', 'Search Number'), ('site_id', 'Website Searched From'), ('prop_id', 'Hotel Number'),
                   ('position', 'Hotel Position on Search Result Page'))

    numeric = (('visitor_hist_starrating', 'Visitors Historical Star Rating'),
               ('visitor_hist_adr_usd', 'Visitors Historical Spending in US Dollars'),
               ('prop_starrating', 'Hotel Star Rating'),
               ('prop_review_score', 'Hotel Review Score'),
               ('prop_location_score1', 'Hotel Location Popularity 1'),
               ('prop_location_score2', 'Hotel Location Popularity 2'),
               ('prop_log_historical_price', 'Hotel Historical Price in US Dollars'),
               ('price_usd', 'Hotel Price For A particular Search'),
               ('srch_length_of_stay', 'Length of Stay Searched For'),
               ('srch_booking_window', 'The Amount of Time between when the Search was done to the Date of Stay'),
               ('srch_adults_count', 'Number of Adults Searched For'),
               ('srch_room_count', 'Number of Rooms Searched for'),
               ('srch_query_affinity_score',
                'The log of the probability that a Hotel will be clicked on Internet Searches'),
               ('orig_destination_distance', 'The distance between the Visitors location to the Hotel location'),
               ('gross_bookings_usd', 'Cost of the Bookings in US Dollars'))

    booleans = (
        ('prop_brand_bool', 'Branded Hotels'),
        ('promotion_flag', 'Hotels That Were on Promotion'),
        ('srch_saturday_night_bool', 'Searches that were less than four days and included weekends'),
        ('random_bool', 'Searches that were randomly sorted'),
        ('click_bool', 'Hotels that were Clicked'),
        ('booking_bool', 'Hotels that were Booked'))

    num_bool = numeric + booleans
    name = forms.ChoiceField(choices=identifiers, required=True, label="Select the column you're interested in:")
    x = forms.ChoiceField(choices=num_bool, required=True, label="Select the data to be plotted on the x-axis:")
    y = forms.ChoiceField(choices=num_bool, required=True, label="Select the data to be plotted on the y-axis:")
    radius = forms.ChoiceField(choices=num_bool, required=True,
                               label="Select the data to be displayed by means of the size of the bubble:")
    circum_color = forms.ChoiceField(choices=numeric, required=True,
                                     label="Select the data to be displayed by means of the colour of the circumference of the bubble:")
