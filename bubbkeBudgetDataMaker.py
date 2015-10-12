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
discretionaryTotal = 0
discretionaryBookings = 0
discretionary2012 = 0
discretionary2013 = 0

mandatoryTotal = 0
mandatoryBookings = 0
mandatory2012 = 0
mandatory2013 = 0

cur = conn.cursor()
#continentlist = ["Africa", "Asia","Antarctica", "Europe","Oceania","South America","North America"]
continentlist = ["Oceania"]

for continent in continentlist:
    fivestar = 0
    fourstar = 0
    threestar = 0
    belowtwostar = 0
    cur.execute("SELECT * from continentdata WHERE continent = (%s)", (continent,))
    rows = cur.fetchall()

    # this function assumes that it only retrieves data fro a particular continent
    for countrydata in rows:
        countryfivestar = 0
        countryfourstar = 0
        countrythreestar = 0
        countrybelowtwostar = 0

        doc = {}
        doc["id"] = countrydata[0] #id of the country in the database
        doc["department"] = countrydata[1] #the continent the country belongs to
        doc["name"] = countrydata[2] # the name of the particular country
        # a place is discretionary if it is mostly independant and
        print(countrydata[1])
        country = countrydata[0]

        cur.execute("SELECT booking_bool, gross_bookings_usd,date_time at time zone 'UTC', prop_brand_bool,prop_starrating  FROM viz_bigtable WHERE prop_country_id = (%s) AND booking_bool = TRUE AND gross_bookings_usd IS NOT NULL AND date_time between to_date('2012-1-1','yyyy-mm-dd') and to_date('2012-12-31','yyyy-mm-dd')", (country,))
        row2012 = cur.fetchall()
        cur.execute("SELECT booking_bool, gross_bookings_usd,date_time at time zone 'UTC', prop_brand_bool, prop_starrating  FROM viz_bigtable WHERE prop_country_id = (%s) AND booking_bool = TRUE AND gross_bookings_usd IS NOT NULL AND date_time between to_date('2013-1-1','yyyy-mm-dd') and to_date('2013-12-31','yyyy-mm-dd')",(country,))
        row2013 = cur.fetchall()
        if (row2012 or row2013):
            bookings = sum([pair[0] for pair in row2012 ]) + sum([pair[0] for pair in row2013 ])
            budget2012 = sum([pair[1] for pair in row2012 ])
            budget2013 = sum([pair[1] for pair in row2013 ])
            brandType =  (sum([pair[3] for pair in row2012 ]) + sum([pair[3] for pair in row2013 ]))/(len(row2012) + (len(row2013)))
            if brandType < 0.5:
                doc["discretion"] = "Discretionary" # brand type is  mostly 0, therefore mostly independant
                discretionaryBookings = discretionaryBookings + bookings
                discretionaryTotal = discretionaryTotal + budget2012 + budget2013
                discretionary2012 = discretionary2012 + budget2012
                discretionary2013 = discretionary2013 + budget2013
            elif brandType >= 0.5:
                doc["discretion"] = "Mandatory" # mostly chain
                mandatoryBookings = mandatoryBookings + bookings
                mandatoryTotal = mandatoryTotal + budget2012 + budget2013
                mandatory2012 = mandatory2012 + budget2012
                mandatory2013 = mandatory2013 + budget2013

        # get how many bookings per hotel star rating
            totalRow = row2012 + row2013

            for item in totalRow:
                if item[4] == 5:
                    countryfivestar +=1
                elif item[4] == 4:
                    countryfourstar +=1
                elif item[4] == 3:
                    countrythreestar +=1
                elif item[4] <= 2:
                    countrybelowtwostar +=1

        elif (row2012 and row2013 is None):
            bookings = sum([pair[0] for pair in row2012 ]) + sum([pair[0] for pair in row2013 ])
            budget2012 = sum([pair[1] for pair in row2012 ])
            budget2013 = 0
            brandType =  (sum([pair[3] for pair in row2012 ]))/(len(row2012))
            if brandType < 0.5:
                doc["discretion"] = "Discretionary" # brand type is  mostly 0, therefore mostly independant
                discretionaryBookings = discretionaryBookings + bookings
                discretionaryTotal = discretionaryTotal + budget2012 + budget2013
                discretionary2012 = discretionary2012 + budget2012
                discretionary2013 = discretionary2013 + budget2013
            elif brandType >= 0.5:
                doc["discretion"] = "Mandatory" # mostly chain
                mandatoryBookings = mandatoryBookings + bookings
                mandatoryTotal = mandatoryTotal + budget2012 + budget2013
                mandatory2012 = mandatory2012 + budget2012
                mandatory2013 = mandatory2013 + budget2013

        # get how many bookings per hotel star rating
            totalRow = row2012

            for item in totalRow:
                if item[4] == 5:
                    countryfivestar +=1
                elif item[4] == 4:
                    countryfourstar +=1
                elif item[4] == 3:
                    countrythreestar +=1
                elif item[4] <= 2:
                    countrybelowtwostar +=1
        elif (row2013 and row2012 is None):
            bookings = sum([pair[0] for pair in row2013 ]) + sum([pair[0] for pair in row2013 ])
            budget2013 = sum([pair[1] for pair in row2013 ])
            budget2012 = 0
            brandType =  (sum([pair[3] for pair in row2013 ]))/(len(row2013))
            if brandType < 0.5:
                doc["discretion"] = "Discretionary" # brand type is  mostly 0, therefore mostly independant
                discretionaryBookings = discretionaryBookings + bookings
                discretionaryTotal = discretionaryTotal + budget2012 + budget2013
                discretionary2012 = discretionary2012 + budget2012
                discretionary2013 = discretionary2013 + budget2013
            elif brandType >= 0.5:
                doc["discretion"] = "Mandatory" # mostly chain
                mandatoryBookings = mandatoryBookings + bookings
                mandatoryTotal = mandatoryTotal + budget2012 + budget2013
                mandatory2012 = mandatory2012 + budget2012
                mandatory2013 = mandatory2013 + budget2013

        # get how many bookings per hotel star rating
            totalRow = row2013

            for item in totalRow:
                if item[4] == 5:
                    countryfivestar +=1
                elif item[4] == 4:
                    countryfourstar +=1
                elif item[4] == 3:
                    countrythreestar +=1
                elif item[4] <= 2:
                    countrybelowtwostar +=1

        else:
            bookings = 0
            budget2012 = 0
            budget2013 = 0
            countryfivestar = 0
            countryfourstar = 0
            countrythreestar = 0
            countrybelowtwostar = 0

        doc["bookings"] = bookings
        doc["budget_2013"] = budget2013
        if (budget2012!= 0):
            doc["change"] = (budget2013 - budget2012)/budget2012
        else:
             doc["change"] = 0

        doc["budget_2012"] = budget2012
        doc["fivestar"] = countryfivestar
        doc["fourstar"] = countryfourstar
        doc["threestar"] = countrythreestar
        doc["belowtwostar"] = countrybelowtwostar

        fivestar = fivestar + countryfivestar
        fourstar = fourstar + countryfourstar
        threestar = threestar + countrythreestar
        belowtwostar = belowtwostar + countrybelowtwostar

        data.append(doc)


print("No of countries",len(data))

import json

extraData = {}
extraData["discretionary bookings"] = discretionaryBookings
extraData["discretionary total"] = discretionaryTotal
extraData["discretionary2012"] = discretionary2012
extraData["discretionary2013"] = discretionary2013
if (discretionary2012!= 0):
    extraData["discretionary spending difference"] = ((discretionary2012-discretionary2013)/discretionary2012)*100
else:
    extraData["discretionary spending difference"] = "no data"

extraData["mandatory bookings"] = mandatoryBookings
extraData["mandatory total"] = mandatoryTotal
extraData["mandatory2012"] = mandatory2012
extraData["mandatory2013"] = mandatory2013
if (mandatory2012 != 0):
    extraData["mandatory spending difference"] = ((mandatory2012-mandatory2013)/mandatory2012)*100
else:
    extraData["mandatory spending difference"] = "no data"

import json
with open('budgetData.txt', 'w') as outfile:
    json.dump(data, outfile)
#print("data", data)
with open('extraData.txt', 'w') as outfile:
    json.dump(extraData, outfile)


