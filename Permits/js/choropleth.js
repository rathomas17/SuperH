// This draws the US map, with both state and county boundaries

//var data; // loaded asynchronously
var counties;
var tooltip;
//xWwidth =900;
//xHeight = 600;
var compareJSON;

var centered;
var alreadyMade = false;
var path = d3.geo.path();
var data;
var states;


function drawMap() {

	console.log("here, data is: ");
	console.log(data["ALL"]["2015"]["22079"]);


	var projection = d3.geo.albersUsa()
	.scale(850)
	.translate([450,250]);

	var path = d3.geo.path().projection(projection);

	tooltip = d3.select("body")
	.append("div")
	.attr("id","tooltip");

	var svg = d3.select("#choroplethGraph")
		.append("svg")
		.attr("id", "chosvg")
		.attr("height", 500)
		//.attr("height", 500)
		//.attr("viewBox", "0 0 870 530")
		.attr("width", 900)
		//.attr("width", 900)
    	//.attr("preserveAspectRatio", "true")
		//added for click
		//.on("click", clicked);
		//end added for click


	//zoom box
	svg.append("rect")
		.attr("class", "background")
		.attr("fill", "none")
		.attr("width", xWidth)
		.attr("height", xHeight)
		.on("click", clicked);

	states = svg.append("g");
	d3.json("data/JSON/us-states.json", function(json) {
		states.append("g")
			.attr("id", "states")
			.selectAll("path")
			.data(json.features)
			.enter().append("path")
			.attr("d", path)
			.on("click", clicked);
	});

	counties = svg.append("g");
	d3.json("data/JSON/us-counties.json", function(json) {
		console.log("data is: ");
  		var x = data["ALL"][2015][22079];
  		console.log("x is: ")
  		console.log(x);
		counties
			.attr("class", "Blues")
			.selectAll("path")
			.attr("id", "county")
			//.attr("class", "Blues")
			.data(json.features)
			.enter().append("path")
			.attr("class", data ? quantize : null)
			.attr("d", path)
			//added for click
			.on("click", clicked)
			//end added for click
			.on("mouseover", function(d){
				if(data[currentState][currentYear][d.id]!=null){
					val = data[currentState][currentYear][d.id]['normalized'];
					tooltip.text(d.properties.name + " County: " + val + " Permits");
				} else {
					tooltip.text(d.properties.name + "County : NO DATA");
				}
				d3.select(this).style('stroke-width','1px');
				d3.select(this).style('stroke','red');
				tooltip.style("visibility", "visible");
			})
			.on("mousemove", function(){
				tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})



			.on("mouseout", function(){
				d3.select(this).style('stroke-width','.25px');
				d3.select(this).style('stroke','grey');
				tooltip.style("visibility", "hidden");});
	});


}



/**** Helper functions to highlight and select data **************/
function highlight(row, on_off) {
	if(typeof on_off === 'undefined'){
		// if on_off is not provided, just toggle class.
		on_off = !d3.select(row).classed('highlight');
	}
	// Set the row's class as highlighted if on==true,
	// Otherwise remove the 'highlighted' class attribute.
	// In DataTables, this is handled automatically for us.
	d3.select(row).classed('highlight', on_off);

	// Fire a highlight event, with the data and highlight status.
	dispatcher.highlight(table.rows(row).data()[0], on_off);
}
function select(row, on_off) {
	// Similar to highlight function.
	if(typeof on_off === 'undefined'){
		on_off = !d3.select(row).classed('selected');
	}

	d3.select(row).classed('selected', on_off);

	// Fire a select event, with the data and selected status.
	dispatcher.select(table.rows(row).data()[0], on_off);
}








function quantize(d) {
	return "q" + Math.floor(getCountyNorm1(d.id)) + "-9";
}

//click function
function clicked(d) {
  var x, y, k;

  if (d && centered !== d) {
    var centroid = path.centroid(d);
    x = centroid[0];
    y = centroid[1];
    k = 4;
    centered = d;
  }
	else {
  	x = 900 / 2;
		y = 450 / 2;
  	k = 1;
  	centered = null;
	}

  counties.selectAll("path")
    .classed("active", centered && function(d) {
    	d3.select(this)
    		.attr("stroke","black")
    		.on("mouseenter", function(d){

    		})


    	return d === centered;
    	});

  counties.transition()
    .duration(750)
    .attr("transform", "translate(" + 900 / 2 + "," + 500 / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
    .style("stroke-width", 0.2 / k + "px");

  states.transition()
  	.duration(750)
  	.attr("transform", "translate(" + 900 / 2 + "," + 500/ 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
  	.style("stroke-width", 0.2 / k + "px");
}

//end click function




function getCountyNorm1(county){
	try{
		return data[currentState][currentYear][county]['sum'];
	}
	catch(e){
		return 0;
	}
}
