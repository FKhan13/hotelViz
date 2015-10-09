d3.json("/static/viz/js/config.json", function (configData) {
    //var config = [{"xaxis": "Country ID", "yaxis": "Avg Bookings", "type": "numnum"}];
    var config = configData;
    var chart1 = dc.barChart("#test1");
var chart2 = dc.barChart("#test2");
var volumeChart = dc.barChart('#monthly-volume-chart');
var xAxisDimension;
var yAxisSumGroup;
var xmax;
var xmin;


var xaxisName = config[0].xaxis;
var yaxisName = config[0].yaxis;

//function drawGraph(error, experiments){
d3.json("/static/viz/js/result.json", function (error, experiments) {
    //numnum, numbool, boolident, identnum, boolbool
    //var dateFormat = d3.time.format('%m/%d/%Y');
    console.log(experiments);
    var dateFormat = d3.time.format.utc("%Y-%m-%d %H:%M:%S");
    //date = new Date(2013, 3, 4);
    //console.log(dateFormat(date));
    //date2 = "2013-03-04 12:21:18";
    //console.log(dateFormat.parse(date2));

    var numberFormat = d3.format('.2f');
    //console.log(experiments);
    experiments.forEach(function (d) {
        d.ycord = +d.ycord;
        d.xcord = +d.xcord;
        d.dd = dateFormat.parse(d.timezone);
        //formatDate = d3.time.format("%b-%Y")
        //console.log(d.dd);
        d.month = d3.time.month(d.dd); // pre-calculate month for better performance

    });
    console.log(experiments);
    //rounds limits to make sure limit is a whole/nice looking number
    function reDomain(maxValue) {
        var dy = Math.pow(10, Math.round(Math.log(maxValue) / Math.log(10)) - 1);
        return Math.ceil(maxValue / dy) * dy;
    }

    xmax = d3.max(experiments, function (d) {
        return d.xcord;
    });
    xmin = d3.min(experiments, function (d) {
        return d.xcord;
    });
    var xmaxRound = reDomain(xmax);
    var xminRound = reDomain(xmin);

    //console.log(xmax);
    var ndx = crossfilter(experiments);

    // These are the functions that determine how the data will be processed in order to be dsplayed appropriately
    if (config[0].type == "numnum") {
        xAxisDimension = ndx.dimension(function (d) {
            return d.xcord;
        });
        yAxisSumGroup = xAxisDimension.group().reduce(
            //add
            function (p, v) {
                p.count++;
                p.xcord = v.xcord;
                p.sum += v['ycord'];
                p.avg = d3.round((p.sum / p.count), 2);
                return p;
            },
            //remove
            function (p, v) {
                p.count--;
                p.xcord = v.xcord;
                p.sum -= v['ycord'];
                p.avg = d3.round((p.sum / p.count), 2);
                return p;
            },
            //init
            function (p, v) {
                return {
                    count: 0,
                    xcord: 0,
                    avg: 0,
                    sum: 0
                };
            });
        console.log(yAxisSumGroup.all());
    }
    else if (config[0].type == "numbool") {
        console.log("X dimension has a certain number of things");
        xAxisDimension = ndx.dimension(function (d) {
            return d.xcord;
        });
        yAxisSumGroup = xAxisDimension.group().reduceSum(function (d) {
            return d.ycord;
        });
        //console.log(yAxisSumGroup.all());
    }
    ;

    var moveMonths = ndx.dimension(function (d) {
        return d.month;
    });

    var volumeByMonthGroup = moveMonths.group().reduceSum(function (d) {
        return d.ycord;
    });

    chart2
        .width(768)
        .height(250)
        .margins({top: 10, right: 50, bottom: 40, left: 50})
        .brushOn(false)
        .x(d3.scale.linear().domain([xmin, xmax]))
        .yAxisLabel(yaxisName + " of Selection")
        .xAxisLabel(xaxisName)
        .dimension(xAxisDimension)
        .group(yAxisSumGroup)
        .valueAccessor(function (d) {
            if (config[0].type == "numnum")
                return d.value.avg;
            else
                return d.value;
        })
        .elasticY(true)
        .on('pretransition', function (chart) {
            chart.selectAll("rect.bar").on("click", function (d) {
                console.log('click');
                chart.filter(null)
                    .filter(d.data.key);
            });
        });
    chart2.render();
    //chart2.call(tip);

    chart1
        .width(768)
        .height(250)
        .margins({top: 10, right: 50, bottom: 40, left: 50})
        .dimension(xAxisDimension)
        .group(yAxisSumGroup)
        .elasticY(true)
        .round(dc.round.floor)
        .alwaysUseRounding(true)
        .valueAccessor(function (d) {
            if (config[0].type == "numnum")
                return d.value.avg;
            else
                return d.value;
        })
        .x(d3.scale.linear().domain([xmin, xmax]))

        .yAxisLabel(yaxisName)
        .xAxisLabel(xaxisName)
        .renderHorizontalGridLines(true)
        // Customize the filter displayed in the control span
        .filterPrinter(function (filters) {
            var filter = filters[0], s = '';
            s += numberFormat(filter[0]) + '% -> ' + numberFormat(filter[1]) + '%';
            return s;
        });

    chart1.render();


    // we need to this helper function out of coordinateGridMixin
    function rangesEqual(range1, range2) {
        if (!range1 && !range2) {
            return true;
        }
        else if (!range1 || !range2) {
            return false;
        }
        else if (range1.length === 0 && range2.length === 0) {
            return true;
        }
        else if (range1[0].valueOf() === range2[0].valueOf() &&
            range1[1].valueOf() === range2[1].valueOf()) {
            return true;
        }
        return false;
    }

    chart1.focusCharts = function (chartlist) {
        if (!arguments.length) {
            return this._focusCharts;
        }
        this._focusCharts = chartlist; // only needed to support the getter above
        this.on('filtered', function (range_chart) {
            if (!range_chart.filter()) {
                dc.events.trigger(function () {
                    chartlist.forEach(function (focus_chart) {
                        focus_chart.x().domain(focus_chart.xOriginalDomain());
                    });
                });
            } else chartlist.forEach(function (focus_chart) {
                if (!rangesEqual(range_chart.filter(), focus_chart.filter())) {
                    dc.events.trigger(function () {
                        focus_chart.focus(range_chart.filter());
                    });
                }
            });
        });
        return this;
    };


    volumeChart
        .width(768)/* dc.barChart('#monthly-volume-chart', 'chartGroup'); */
        .height(40)
        .margins({top: 0, right: 50, bottom: 20, left: 40})
        .dimension(moveMonths)
        .group(volumeByMonthGroup)
        .centerBar(true)
        .gap(1)

        .x(d3.time.scale().domain([new Date(2012, 1, 1), new Date(2013, 12, 31)]))
        .round(d3.time.month.round)
        .alwaysUseRounding(true)
        .xUnits(d3.time.months)
        .elasticY(true);
    volumeChart.yAxis().ticks(0);
    volumeChart.render();

    chart1.focusCharts([chart2]);


});
});

