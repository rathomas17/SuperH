function drawLine(patent){
    console.log("patent: "+patent);
	var margin = {top: 20, right: 30, bottom: 30, left: 70},
		width = xWidthLineGraph - margin.left - margin.right,
		height = xHeightLineGraph - margin.top - margin.bottom;
		console.log("linegraph: w "+width+"; h "+height);

	var x = d3.scale.linear()
		.range([0, width]);

	var y = d3.scale.linear()
		.range([height, 0]);

	var xAxis = d3.svg.axis()
    .ticks(5)
    .scale(x)
    .orient("bottom");
    //.tickFormat(d3.time.format("%b %e"))
    //.ticks(7);

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	var area = d3.svg.area()
		.x(function(d) { return x(d.x); })
		.y0(height)
		.y1(function(d) { return y(d.y); });

	var lsvg = d3.select("#lineGraph")
		.append("svg")
		.attr("id", "currentLineGraph")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var data = [];
    console.log("patent "+patent);
    console.log("dateSums "+patentSummeries[patent]);
  var dateSums = patentSummeries[patent]['sumDates'];
	var i = 0;
  for(date in dateSums){
		data[i] = {};
		data[i]['x'] = +date;
		data[i]['y'] = parseFloat(dateSums[date]);
		data[i]['delta'] = patentSummeries[patent]['sumDates'][date];
		i = i + 1;
	}
	data.sort(function(a,b){
		return (a.x < b.x) ? 1 : -1;
	});

	x.domain(d3.extent(data, function(d) { return d.x; }));
	y.domain([0, Math.max(d3.max(data, function(d) { return d.y; }), 26000)]);

	lsvg.append("path")
		.datum(data)
		.attr("class", "area")
		.attr("d", area);

	lsvg.append("lsvg:line")
		.attr("x1", x(data[0].x))
		.attr("y1", y(25000))
		.attr("x2", x(data[data.length-1].x))
		.attr("y2", y(25000))
		.style("stroke", "grey");

	lsvg.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	lsvg.append("g")
		.attr("class", "y axis")
		.call(yAxis)
		.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 6)
		.attr("dy", ".71em")
		.style("text-anchor", "end");

	lsvg.selectAll(".dot")
		.data(data.filter(function(d) { return d.y; }))
	  .enter().append("circle")
		.attr("class", "dot")
		.attr("cx", area.x())
		.attr("cy", area.y())
		.attr("r", 3.5)
		.on("mouseover", function(d){
			var month_names_short = ['pan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      	tooltip.text(d.delta + " patentSs " +  d.x);
      	d3.select(this).attr('r',6);
      	tooltip.style("visibility", "visible");
  	})
		.on("click", function(d){
			console.log("clicked!" + d.x);
			currentYear = d.x;
      d3.selectAll('.currentYear').text(currentYear);
			counties.selectAll("path")
      .attr("class", quantize);
		})
		.on("mousemove", function(){
			tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
		.on("mouseout", function(){
			d3.select(this).attr('r',3.5);
			tooltip.style("visibility", "hidden");});
}
