// This draws the US map, with both state and county boundaries

var data; // loaded asynchronously
var counties;
var tooltip
var centered;
 // width: 960px;
 //height: 500px;



function drawMap() {
	var path = d3.geo.path();

	var svg = d3.select("#choroplethGraph")
		.append("svg")
		.attr("id", "chosvg")
		.attr("height", 400)
		//.attr("height", 500)
		.attr("viewBox", "0 0 870 530")
    .attr("width", 640)
		//.attr("width", 900)
    .attr("preserveAspectRatio", "true")
		//added for click
		
		.on("click", clicked);
		//end added for click

	counties = svg.append("g")
		.attr("id", "counties")
		.attr("class", "Blues")
		//added for click
		.on("click", clicked);
		//end added for click
	var states = svg.append("g")
		.attr("id", "states")
		//added for click
		.on("click", clicked);
		//end added for click

	tooltip = d3.select("body")
		.append("div")
		.attr("id","tooltip");

	d3.json("data/JSON/us-counties.json", function(json) {
		counties.selectAll("path")
			.data(json.features)
			.enter().append("path")
			.attr("class", data ? quantize : null)
			.attr("d", path)
			//added for click
			.on("click", clicked)
			//end added for click
			.on("mouseover", function(d){
	    	val = data[currentCPC][currentYear][d.id]['normalized'];
					tooltip.text(d.properties.name + " County: " + val + " Permits");
					d3.select(this).style('stroke-width','4px');
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

	d3.json("data/JSON/us-states.json", function(json) {
		states.selectAll("path")
			.data(json.features)
			.enter().append("path")
			.attr("d", path);
	});
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
  	x = width / 2;
		y = height / 2;
  	k = 1;
  	centered = null;
	}

	counties.transition()
	      	.duration(750)
	      	.attr("transform", "translate(" + xWidth / 2 + "," + xHeight / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
	      	.style("stroke-width", 1.5 / k + "px");

  g.selectAll("path")
    .classed("active", centered && function(d) { return d === centered; });

  g.transition()
    .duration(750)
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
    .style("stroke-width", 1.5 / k + "px");
}
//end click function




function getCountyNorm1(county){
	try{
		return data[currentCPC][currentYear][county]['sum'];
	}
	catch(e){
		return 0;
	}
}
