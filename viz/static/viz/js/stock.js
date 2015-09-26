
var chart = dc.barChart("#test");
var volumeChart = dc.barChart('#monthly-volume-chart');
var fluctuationChart = dc.barChart('#fluctuation-chart');


var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Frequency:</strong> <span style='color:red'>" + tip + "</span>";
  });

//chart.call(tip);


//function plotgraph(data){
d3.json("/static/viz/js/ndx.json", function (data) {
	//console.log(data);
    var dateFormat = d3.time.format('%m/%d/%Y');
    var numberFormat = d3.format('.2f');

    data.forEach(function (d) {
        d.dd = dateFormat.parse(d.date);
        d.month = d3.time.month(d.dd); // pre-calculate month for better performance
        d.close = +d.close; // coerce to number
        d.open = +d.open;
    });
    
    //console.log(data);

    var ndx = crossfilter(data);
    var all = ndx.groupAll();

    var moveMonths = ndx.dimension(function (d) {
        return d.month;
    });

    var volumeByMonthGroup = moveMonths.group().reduceSum(function (d) {
        return d.volume / 500000;
    });
    
    var fluctuation = ndx.dimension(function (d) {
     	data = Math.round((d.close - d.open) / d.open * 100);
        return Math.round((d.close - d.open) / d.open * 100);

    });
    var fluctuationGroup = fluctuation.group();

    var barg = ndx.dimension(function (d) {
        return Math.round((d.close - d.open) / d.open * 100);
        //return Math.round(d.open);
    });
    var bargGroup = barg.group();
    
  

  chart
    .width(768)
    .height(200)
    //.x(d3.scale.ordinal())
    //.xUnits(dc.units.ordinal)
    .x(d3.scale.linear().domain([-25, 25]))

    .elasticY(true)
    .elasticX(true)
    //.yAxisLabel("This is the Y Axis!")
    .dimension(barg)
    .group(bargGroup)
    .on('pretransition', function(chart) {
        chart.selectAll("rect.bar").on("click", function (d) {
            console.log('click');
            chart.filter(null)
                .filter(d.data.key)
                .redrawGroup();
        });
    });
   
        
   fluctuationChart /* dc.barChart('#volume-month-chart', 'chartGroup') */
        .width(768)
        .height(200)
        .margins({top: 10, right: 50, bottom: 30, left: 40})
        .dimension(fluctuation)
        .group(fluctuationGroup)
        .elasticY(true)
      
        // (_optional_) whether bar should be center to its x value. Not needed for ordinal chart, `default=false`
        .centerBar(true)
        // (_optional_) set gap between bars manually in px, `default=2`
        .gap(1)
        // (_optional_) set filter brush rounding
        .round(dc.round.floor)
        .alwaysUseRounding(true)
        .x(d3.scale.linear().domain([-25, 25]))
        .renderHorizontalGridLines(true)
        // Customize the filter displayed in the control span
        .filterPrinter(function (filters) {
            var filter = filters[0], s = '';
            s += numberFormat(filter[0]) + '% -> ' + numberFormat(filter[1]) + '%';
            return s;
        });
    
    
   volumeChart.width(990) /* dc.barChart('#monthly-volume-chart', 'chartGroup'); */
        .height(40)
        .margins({top: 0, right: 50, bottom: 20, left: 40})
        .dimension(moveMonths)
        .group(volumeByMonthGroup)
        .centerBar(true)
        .gap(1)
        .x(d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
        .round(d3.time.month.round)
        .alwaysUseRounding(true)
        .xUnits(d3.time.months);   
        
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
    };
        
        
    fluctuationChart.focusChart = function (c) {
     if (!arguments.length) {
     	console.log('returned focus chart');
         return _focusChart;
     }
     _focusChart = c;
     fluctuationChart.on('filtered', function (inchart) {
         if (!inchart.filter()) {
             dc.events.trigger(function () {
             	console.log('ranges are equal');
                 _focusChart.x().domain(_focusChart.xOriginalDomain());
             });
         } else if (!rangesEqual(chart.filter(), _focusChart.filter())) {
             dc.events.trigger(function () {
             	console.log('ranges not equal');
                 _focusChart.focus(inchart.filter());
             });
         }
     });
     return fluctuationChart;
 }; 
 	dc.renderAll();   
    fluctuationChart.focusChart(chart);
    

});
//};
d3.selectAll('#version').text(dc.version);
d3.json('https://api.github.com/repos/dc-js/dc.js/releases/latest', function (error, latestRelease) {
	d3.selectAll('#latest').text(latestRelease.tag_name); /* jscs:disable */

});
