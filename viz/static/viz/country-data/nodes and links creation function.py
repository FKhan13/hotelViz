def play(request):
    logging.basicConfig(filename='viz/static/viz/country-data/log.txt', level=logging.INFO)
    first_date = datetime.date(2012, 10, 31)
    end_date = datetime.date(2013, 7, 1)
    delta = datetime.timedelta(weeks=1)
    file_no = 1

    while first_date < end_date:
        logging.info("Started with File: " + str(file_no))
        second_date = first_date + delta

        date_range = (first_date, second_date)
        cur = connection.cursor()

        query = "SELECT DISTINCT ON (visitor_location_country_id) visitor_location_country_id FROM viz_bigtable WHERE date_time BETWEEN %s AND %s"

        cur.execute(query, date_range)

        countries = []
        for row in cur:
            countries.append(row[0])

        if countries is None:
            raise Http404("Could not find visitor countries ")

        logging.info("Visitor Countries: " + str(countries.__len__()))

        query = "SELECT DISTINCT ON (prop_country_id) prop_country_id FROM viz_bigtable WHERE date_time BETWEEN %s AND %s"

        cur.execute(query, date_range)

        for row in cur:
            if row[0] not in countries:
                countries.append(row[0])

        logging.info("Total Countries: " + str(countries.__len__()))

        countries.sort()

        nodes = []

        for country in countries:
            nodes.append({"name": str(country), "group": random.randint(1, 7)})

        logging.info("Created Nodes dictionary")

        query = "SELECT DISTINCT ON (visitor_location_country_id,prop_country_id) visitor_location_country_id,prop_country_id FROM viz_bigtable WHERE date_time BETWEEN %s AND %s"

        cur.execute(query, date_range)

        cur1 = connection.cursor()
        links = []
        for row in cur:
            query = "SELECT COUNT(visitor_location_country_id) FROM viz_bigtable WHERE date_time BETWEEN %s AND %s AND visitor_location_country_id=%s AND prop_country_id=%s;"
            data = date_range + row
            cur1.execute(query, data)

            value = cur1.fetchone()[0]

            source = countries.index(row[0])
            target = countries.index(row[1])

            links.append({"source": source, "target": target, "value": value})

        logging.info("Done With Links - About to write Json file")

        file_path = "viz/static/viz/country-data/" + str(file_no) + ".json"

        with open(file_path, "w") as fp:
            json.dump({"nodes": nodes, "links": links}, fp)

        logging.info("Done With File Number: " + str(file_no))
        first_date = second_date
        file_no += 1

    cur.close()
    connection.close()

    return render(request, 'viz/play.html')