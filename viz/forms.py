from django import forms
from django.forms import CheckboxSelectMultiple


class SelectionForm(forms.Form):
    DBColumns = (
        ('srch_id', 'Search Number'), ('site_id', 'Website Searched From'),
        ('visitor_location_country_id', 'Visitors Country'),
        ('visitor_hist_starrating', 'Visitors Historical Star Rating'),
        ('visitor_hist_adr_usd', 'Visitors Historical Spending in US Dollars'),
        ('prop_country_id', 'Hotel Country'), ('prop_starrating', 'Hotel Star Rating'),
        ('prop_review_score', 'Hotel Review Score'), ('prop_brand_bool', 'Branded Hotels'),
        ('prop_location_score1', 'Hotel Location Popularity 1'),
        ('prop_location_score2', 'Hotel Location Popularity 2'),
        ('prop_log_historical_price', 'Hotel Historical Price in US Dollars'),
        ('position', 'Hotel Position on Search Result Page'),
        ('price_usd', 'Hotel Price For A particular Search'),
        ('promotion_flag', 'Hotels That Were on Promotion'),
        ('srch_length_of_stay', 'Length of Stay Searched For'),
        ('srch_booking_window', 'The Amount of Time between when the Search was done to the Date of Stay'),
        ('srch_adults_count', 'Number of Adults Searched For'),
        ('srch_children_count', 'Number of Children Searched for'), ('srch_room_count', 'Number of Rooms Searched for'),
        ('srch_saturday_night_bool', 'Searches that were less than four days and included weekends'),
        ('srch_query_affinity_score', 'The log of the probability that a Hotel will be clicked on Internet Searches'),
        ('orig_destination_distance', 'The distance between the Visitors location to the Hotel location'),
        ('random_bool', 'Searches that were randomly sorted'),
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
         'The percentage difference between Expedias booking rate and Competitor Eights booking rate'),
        ('click_bool', 'Hotels that were Clicked'),
        ('gross_bookings_usd', 'Cost of the Bookings in US Dollars'), ('booking_bool', 'Hotels that were Booked'))
    fields = forms.MultipleChoiceField(choices=DBColumns, required=True, widget=CheckboxSelectMultiple)
