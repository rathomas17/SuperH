//
// This draws the US map, with both state and county boundaries

var data; // loaded asynchronously
var counties;
var tooltip;
 //width: 960px;
 //height: 500px;

function drawMap() {
	var path = d3.geo.path();

	var svg = d3.select("#choroplethGraph")
		.append("svg")
		.attr("id", "chosvg")
		.attr("height", xHeight)
//		.attr("height", 500)
		.attr("viewBox", "0 0 960 500")
	    .attr("width", xWidth)
//	    .attr("width", 900)
	    .attr("preserveAspectRatio", "true");

	counties = svg.append("g")
			.attr("id", "counties")
			.attr("class", "Blues");

	var states = svg.append("g")
			.attr("id", "states");

	tooltip = d3.select("body")
		.append("div")
		.attr("id","tooltip")

	d3.json("data/us-counties.json", function(json) {
		counties.selectAll("path")
				.data(json.features)
			.enter().append("path")
				.attr("class", data ? quantize : null)
				.attr("d", path)
			 	.on("mouseover", function(d){
				    //			 		tooltip.text(d.properties.name + " County: " + data[d.id]['sum'] + " Signers");
				    //console.log(" Countyxxx: " + data[currentCPC][d.id]['normalized'] + " Patents");
				    //val = 0;
				    // vvfif (d.id in data[currentCPC])
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
	;
	});

	d3.json("data/us-states.json", function(json) {
		states.selectAll("path")
				.data(json.features)
			.enter().append("path")
				.attr("d", path);
	});
}


function quantize(d) {
	return "q" + Math.floor(getCountyNorm1(d.id)) + "-9";
}

function getCountyNorm1(county){
	try{
//		return data[county]['normalized'];
//		console.log("county data "+data['A'][county]['sum']);
		return data[currentCPC][currentYear][county]['sum'];
	}
	catch(e){
		return 0;
	}
}
