function reDomain(maxValue) {
    var dy = Math.pow(10, Math.round(Math.log(maxValue) / Math.log(10)) - 1);
    return Math.ceil(maxValue / dy) * dy;
	}
// Various accessors that specify the four dimensions of data to visualize.
function typeCheck(d){
	ycord: d3.mean(v, function(d) { return d.ycord; });
}
function x(d) { return d.values.xcord; }
function y(d) { return d.values.ycord; }
function radius(d) { return ((d.values.radiusval + 1) * 50000000); }
function color(d) { return d.key; }
function key(d) { return d.key; }
function independant(d) {
	
	if (d.values.circumcolor == 1)
		{return "blue";}
	else if (d.values.circumcolor == 0)
		{return "black";}
}
//function key(d) { return d.name; }
var config = [{"xaxis":"Review Score", "yaxis":"User Rating", "xmax":"5","ymax":"2000", "ytype":"bool", "xtype":"num", "radType":"num"}];
var yaxisName = config[0].yaxis;
var xaxisName = config[0].xaxis;
var xmax = config[0].xmax;
var ymax = config[0].ymax;
var ytype = config[0].ytype;
var xtype = config[0].xtype;
var radType = config[0].radType;

var domain0 = [new Date(2012, 0, 1), new Date(2013, 11, 31)];
    //domain1 = [new Date(2000, 1, 1), new Date(2000, 1, 2)];
// Chart dimensions.
var margin = {top: 100, right: 300, bottom: 150, left: 100},
    width = window.innerWidth - margin.right,
    height = window.innerHeight - margin.top - margin.bottom;

// Various scales. These domains make assumptions of data, naturally.
var xScale = d3.scale.linear().domain([0, xmax]).range([0, width]),
    yScale = d3.scale.linear().domain([0, ymax]).range([height, 0]),
    radiusScale = d3.scale.sqrt().domain([0, 5e8]).range([0, 40]),
    colorScale = d3.scale.category10();

// The x & y axes.
var xcord = d3.svg.axis().orient("bottom").scale(xScale).ticks(12, d3.format(",d")),
    ycord = d3.svg.axis().scale(yScale).orient("left");

// Create the SVG container and set the origin.
var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add the x-axis.
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xcord);

// Add the y-axis.
svg.append("g")
    .attr("class", "y axis")
    .call(ycord);

// Add an x-axis label.
svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width)
    .attr("y", height - 6)
    .text(xaxisName);

// Add a y-axis label.
svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", 6)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .text(yaxisName);

// Add the year label; the value is set on transition.
var label = svg.append("text")
    .attr("class", "year label")
    .attr("text-anchor", "end")
    .attr("y", height - 24)
    .attr("x", width)
    .text('Jan-2012');

//this one filters the time in question of the data in question
		function filter_year(filter) {
			var f = eval(filter);
			var object;
			if ( typeof (f.length) != "undefined") {
			} else {
			}
			if ( typeof (f.top) != "undefined") {
				f = f.top(Infinity);
			} else {
			}
			if ( typeof (f.dimension) != "undefined") {
				f = f.dimension(function(d) {
					return "";
				}).top(Infinity);
			} else {
			}
			yearPoints = [];
			for (var i = 0; i < f.length; i++) {
				object = f[i];
				yearPoints.push(object);
			}
			return yearPoints;
		}

d3.json("result.json", function(data) {
//function plotGraph(data){
	console.log(data);
	//var dateFormat = d3.time.format('%m-%d-%Y %H:%M:%S');
	var dateFormat = d3.time.format.utc("%Y-%m-%d %H:%M:%S");
	 data.forEach(function(d) {
        d.ycord = +d.ycord;
        d.xcord = +d.xcord;
        d.dd = dateFormat.parse(d.date);
        d.month = d3.time.month(d.dd); // pre-calculate month for better performance
    });
    console.log(data);
    var xmax = d3.max(data, function(d) { return d.xcord; });
	var xmin = d3.min(data, function(d) { return d.xcord; });
   	xmaxRound = reDomain(xmax);
   	xminRound = reDomain(xmin);
   	
   	var ymax = d3.max(data, function(d) { return d.ycord; });
	var ymin = d3.min(data, function(d) { return d.ycord; });
   	ymaxRound = reDomain(ymax);
   	yminRound = reDomain(ymin);
   	
   	
    
  var initDate = new Date(2012, 3, 5);
  var formatDate = d3.time.format("%b-%Y");
 
  // Add a dot per nation. Initialize the data at 1800, and set the colors.
  var dot = svg.append("g")
      .attr("class", "dots")
      .selectAll(".dot")
      .data(initializeData(initDate))
      .enter().append("circle")
      .attr("class", "dot")
      .style("fill", function(d) { return colorScale(color(d)); })
      .style("opacity", 0.5)
      .style("stroke", function(d){return independant(d);})
      .call(position)
      .sort(order);

  // Add a title.
  dot.append("title")
      .text(function(d) { return d.key; });

  // Add an overlay for the year label.
  var box = label.node().getBBox();

  var overlay = svg.append("rect")
        .attr("class", "overlay")
        .attr("x", box.x)
        .attr("y", box.y)
        .attr("width", box.width)
        .attr("height", box.height)
        .on("mouseover", enableInteraction);
        
    svg.transition()
      .duration(10000)
      .ease("linear")
      .tween("year", tweenYear)
      .each("end", enableInteraction);

  // Positions the dots based on data.
  function position(dot) {
    dot .attr("cx", function(d) { return xScale(x(d)); })
        .attr("cy", function(d) { return yScale(y(d)); })
        .attr("r", function(d) { return radiusScale(radius(d)); })
        ;
  }

  // Defines a sort order so that the smallest dots are drawn on top.
  function order(a, b) {
    return radius(b) - radius(a);
  }

  // After the transition finishes, you can mouseover to change the year.
  function enableInteraction() {
        var yearScale = d3.time.scale()
    		.domain(domain0)
    		.range([box.x + 10, box.x + box.width - 10])
    		.clamp(true);
    		//.range([0, width]);

    // Cancel the current transition, if any.
    svg.transition().duration(0);

    overlay
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("mousemove", mousemove)
        .on("touchmove", mousemove);

    function mouseover() {
      label.classed("active", true);
    }

    function mouseout() {
      label.classed("active", false);
    }

    function mousemove() {
      displayYear(yearScale.invert(d3.mouse(this)[0]));
    }
  }
  
 

  // Tweens the entire chart by first tweening the year, and then the data.
  // For the interpolated data, the dots and label are redrawn.
 
   function tweenYear() {
    var year = d3.interpolate(new Date(2012, 1, 1), new Date(2013, 11, 31));   		
    return function(t) { displayYear(year(t)); };
  }


  // Updates the display to show the specified year.
  function displayYear(date) {
  	if (typeof(date) == "number"){
  		dot.data(interpolateData(new Date(date)), key).call(position);
  		label.text(formatDate(new Date(date)));
  	}
  	else{
  		dot.data(interpolateData(date), key).call(position);	
  		label.text(formatDate(date));
  	};  
  }

  // Interpolates the dataset for the given (fractional) year.
  function interpolateData(date) {
  	console.log(date);
  	var formatDate = d3.time.format("%b-%Y");
  		newdate = formatDate(date);
  		
		var crossData = crossfilter(data);
		var dataDim = crossData.dimension(function(d) {
		
		var dateData = formatDate(d.dd);
			return dateData;});
		var filterData = dataDim.filter(newdate);
		var yearData = filter_year(filterData);
		var ycordVal;
		var xcordVal;
		var radiusNewVal;

		var finalArray = d3.nest()
		  .key(function(d) { return d.name; }) //grouped according to name
		  .rollup(function(v) { 
		  	if (ytype == "num"){
		  		ycordVal  = d3.mean(v, function(d) { return d.ycord; });
		  	}
		  	else ycordVal = d3.sum(v,function(d){return d.ycord;});
		  	
		  	if (xtype == "num"){
		  		xcordVal = d3.mean(v, function(d) { return d.xcord; });
		  	}
		  	else xcordVal = d3.sum(v,function(d){return d.xcord;});
		  	if (radType == "num"){
		  		radiusNewVal = d3.mean(v, function(d) { return d.radiusval; });
		  	}
		  	else radiusNewVal = d3.sum(v,function(d){return d.radiusval;});
		  	return {
		    //ycord: d3.mean(v, function(d) { return d.ycord; }),
		    ycord: ycordVal,
		    xcord: xcordVal,
		    radiusval: radiusNewVal,
		    circumcolor: d3.mean(v,function(d){return d.circumcolor;})}; })
		  .entries(yearData);
		console.log(finalArray);
		return finalArray;
  }
  
  function initializeData(date) {
  	
  	var formatDate = d3.time.format("%Y");
  		newdate = formatDate(date);
		var crossData = crossfilter(data);
		var dataDim = crossData.dimension(function(d) {
		
		var dateData = formatDate(d.dd);
			return dateData;});
		var filterData = dataDim.filter(newdate);
		var yearData = filter_year(filterData);
		var ycordVal;
		var xcordVal;
		var radiusNewVal;

		var finalArray = d3.nest()
		  .key(function(d) { return d.name; }) //grouped according to name
		  .rollup(function(v) { 
		  	return {
		    ycord: 0,
		    xcord: 0,
		    radiusval: 1,
		   	name: "name",
		    circumcolor: "circumcolor"}; })
		  .entries(yearData);
		  console.log(finalArray)
		return finalArray;
  }
});


