//
// This draws the US map, with both state and cbsa boundaries

var data; // loaded asynchronously
var cbsa;
var tooltip;
var width =900;
var height = 600;

var centered;

var path = d3.geo.path();

function drawMap() {
	
	var projection = d3.geo.albersUsa()
		//.scale( 1300 )
		//.translate( [width/2,height/2] );
	
	var path = d3.geo.path().projection(projection);
	
	tooltip = d3.select("body")
		.append("div")
		.attr("id","tooltip")
		.text("test")
		.style("visibility", "visible");

	var svg = d3.select("body")
		.append("svg")
		.attr("id", "chosvg")
		.attr("height", height)      
		//.attr("viewBox", "0 0 2000 2000")
	    .attr("width", width)
	    .style("preserveAspectRatio", "true");

//	counties = svg.append("g")
//			.attr("id", "counties")
//			.attr("class", "Blues");
	
	//zoom box
	svg.append("rect")
		.attr("class", "background")
		.attr("width", width)
		.attr("height", height)
		.on("click", clicked);
	
	var states = svg.append("g");
	d3.json("data/us-states.json", function(json) {
		states.append("g")
			.attr("id", "states")
			.selectAll("path")
			.data(json.features)
			.enter().append("path")
			.attr("d", path)
			.attr("stroke-width", "1px")
			.attr("stroke", "black")
			.on("click", clicked)
		    .on("mouseenter", function(d){

		    	d3.select(this).attr("fill", "red")
		    	tooltip.text(d.properties.name)
		    		.style("visibility", "visible")
			  		.style("top", (event.pageY)+"px")
			  		.style("left", (event.pageX)+"px");
		      }).on("mouseleave", function(d){
		    	  d3.select(this).attr("fill", "gray");
		      });
	});
	
	
	
	cbsa = svg.append("g");
	d3.json("data/us-cbsa.json", function(json) {
		cbsa.append("g")
			.selectAll("path")
			.attr("id", "cbsa")	
			.data(json.features)
			.enter()
			.append("path")
			.attr("fill", "none")
			.attr("class", data ? quantize : null)
			.attr("d", path)
			.on("click", clicked);
	});


function clicked(d) {
	var x, y, k;
	
	if (d && centered !== d) {
		var centroid = path.centroid(d);
	    x = centroid[0];
	    y = centroid[1];
	    k = 4;
	    centered = d;
	} else {
	    x = width / 2;
	    y = height / 2;
	    k = 1;
	    centered = null;
	}

//		  states.selectAll("path")
//		      .classed("active", centered && function(d) { return d === centered; });

	cbsa.selectAll("path")
	  	.classed("active", centered && function(d) {
	  	d3.select(this).attr("fill", "blue")
	  	.attr("stroke", "black")
	  	.on("mouseenter", function(d){
	  		console.log("testing data");
	  		console.log(data[currentCPC][currentYear][d.properties.GEOID]["cbsaNormalized"]);
	    	val = data[currentCPC][currentYear][d.properties.GEOID]["cbsaNormalized"];
	  		d3.select(this)
  		  		.attr("stroke", "yellow")
  		  		.attr("stroke-width", "2px")
  		  		.attr("fill", "orange");
	  		tooltip.text(d.properties.NAME + " : " + val + " patents");
	  		tooltip.style("visibility", "visible")
	  		.style("top", (event.pageY)+"px")
	  		.style("left", (event.pageX)+"px");
	  	})
	  	.on("mouseleave", function(d){
	  		d3.select(this)
  		  	.attr("stroke", "black")
  		  	.attr("stroke-width", ".5px")
  		  	.attr("fill", "blue");
	  		tooltip.style("visibility", "hidden");
	  	})	
	  	return d === centered; 
	  	});
	  
	  	cbsa.transition()
	      	.duration(750)
	      	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
	      	.style("stroke-width", 1.5 / k + "px");
	  
	  	states.transition()
	      	.duration(750)
	      	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
	      	.style("stroke-width", 1.5 / k + "px");
		}
}	


function quantize(d) {
	return "q" + Math.floor(getCBSANorm1(d.cbsaID)) + "-9";
}

function getCBSANorm1(cbsa){
	try{
//		return data[county]['normalized'];
//		console.log("county data "+data['A'][county]['sum']);
		//console.log(data[currentCPC][currentYear])
//		return data[currentCPC][currentYear][cbsa]['cbsaSum'];
	}
	catch(e){
		return 0;
	}
}
