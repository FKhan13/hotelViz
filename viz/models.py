from django.db import models


# Create your models here.

class BigTable(models.Model):
    srch_id = models.IntegerField(db_index=True)
    date_time = models.DateTimeField(db_index=True)
    site_id = models.IntegerField(db_index=True)
    visitor_location_country_id = models.IntegerField(blank=True, null=True, db_index=True)
    visitor_hist_starrating = models.FloatField(blank=True, null=True, db_index=True)
    visitor_hist_adr_usd = models.FloatField(blank=True, null=True, db_index=True)
    prop_country_id = models.IntegerField(db_index=True)
    prop_id = models.IntegerField(db_index=True)
    prop_starrating = models.IntegerField(db_index=True)
    prop_review_score = models.FloatField(blank=True, null=True, db_index=True)
    prop_brand_bool = models.BooleanField(db_index=True)
    prop_location_score1 = models.FloatField(blank=True, null=True, db_index=True)
    prop_location_score2 = models.FloatField(blank=True, null=True, db_index=True)
    prop_log_historical_price = models.FloatField(blank=True, null=True, db_index=True)
    position = models.IntegerField(db_index=True)
    price_usd = models.FloatField(blank=True, null=True, db_index=True)
    promotion_flag = models.BooleanField(db_index=True)
    srch_destination_id = models.IntegerField(db_index=True)
    srch_length_of_stay = models.IntegerField(db_index=True)
    srch_booking_window = models.IntegerField(db_index=True)
    srch_adults_count = models.IntegerField(db_index=True)
    srch_children_count = models.IntegerField(db_index=True)
    srch_room_count = models.IntegerField(db_index=True)
    srch_saturday_night_bool = models.BooleanField(db_index=True)
    srch_query_affinity_score = models.FloatField(blank=True, null=True, db_index=True)
    orig_destination_distance = models.FloatField(blank=True, null=True, db_index=True)
    random_bool = models.BooleanField(db_index=True)
    comp1_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp1_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp1_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp2_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp2_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp2_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp3_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp3_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp3_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp4_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp4_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp4_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp5_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp5_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp5_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp6_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp6_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp6_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp7_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp7_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp7_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    comp8_rate = models.IntegerField(blank=True, null=True, db_index=True)
    comp8_inv = models.IntegerField(blank=True, null=True, db_index=True)
    comp8_rate_percent_diff = models.FloatField(blank=True, null=True, db_index=True)
    click_bool = models.BooleanField(db_index=True)
    gross_bookings_usd = models.FloatField(blank=True, null=True, db_index=True)
    booking_bool = models.BooleanField(db_index=True)


class Countries(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    a_name = models.CharField(max_length=40, blank=True, null=True, db_index=True)


class Continents(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    continent = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    a_name = models.CharField(max_length=50, blank=True, null=True, db_index=True)
