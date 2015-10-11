__author__ = 'User'


import psycopg2

try:
    conn = psycopg2.connect("dbname='hotelViz' user='jedi' host='localhost' password='trance'")
except:
    print ("I am unable to connect to the database")

doc = {}
positionsdoc = {}
totaldoc = {}
departmentdoc = {}
data = []

cur = conn.cursor()
#cur.execute("SELECT * from continentdata")
#continentlist = ["Africa", "Asia","Antarctica", "Europe","Oceania","South America","North America"]
continentlist = ["Antarctica","Oceania"]

for continent in continentlist:
    #cur.execute("SELECT * from continentdata WHERE continent = 'Oceania'")
    cur.execute("SELECT * from continentdata WHERE continent = (%s)", (continent,))
    rows = cur.fetchall()

    # this function assumes that it only retrieves data fro a particular continent
    for countrydata in rows:
        doc = {}
        doc["id"] = countrydata[0] #id of the country in the database
        doc["department"] = countrydata[1] #the continent the country belongs to
        doc["name"] = countrydata[2] # the name of the particular country
        doc["discretion"] = "discretionary"

        country = countrydata[0]

        cur.execute("SELECT booking_bool, gross_bookings_usd,date_time at time zone 'UTC' FROM viz_bigtable WHERE prop_country_id = (%s) AND booking_bool = TRUE AND date_time between to_date('2012-1-1','yyyy-mm-dd') and to_date('2012-12-31','yyyy-mm-dd')", (country,))
        row2012 = cur.fetchall()
        cur.execute("SELECT booking_bool, gross_bookings_usd,date_time at time zone 'UTC' FROM viz_bigtable WHERE prop_country_id = (%s) AND booking_bool = TRUE AND date_time between to_date('2013-1-1','yyyy-mm-dd') and to_date('2013-12-31','yyyy-mm-dd')",(country,))
        row2013 = cur.fetchall()

        bookings = sum([pair[0] for pair in row2012 ]) + sum([pair[0] for pair in row2013 ])
        budget2012 = sum([pair[1] for pair in row2012 ])
        budget2013 = sum([pair[1] for pair in row2013 ])

        doc["bookings"] = bookings
        doc["budget_2013"] = budget2013
        doc["change"] = (budget2012-budget2013)/budget2012
        doc["budget_2012"] = budget2012
        data.append(doc)

print(data)
print(len(data))

