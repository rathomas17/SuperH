

var height = 1300;
var width = 1300;
var data; //loaded anynchronously
var tooltip;
var cbsa;

function drawCbsaMap(){

	//not sure why we need to create a path
	var path = d3.geo.path();
	
	//create svg box that will contain the map
	var svg = d3.select( "body" ) //select html element
	  	.append( "svg" ) //returns svg element
	  	.attr("viewBox", "0 0 950 1000")
	  	.attr( "width", width ) //also returns svg element
	  	//.attr("preserveAspectRatio", "true")
	  	.attr( "height", height );

	cbsa = svg.append( "g" )
		.attr("id", "CBSA")
		.attr("class", "Blues");

	var state = svg.append("g")
		.attr("id", "states");
	
	var projection = d3.geo.albers()
		.scale( 800 )
		.center( [-10, 35] )
		.translate( [width/2,height/2] );
	
	tooltip = d3.select("body")
		.append("div")
		.attr("id", "tooltip")
		.style("visibility", "invisible");
	
	/* 
	 * functionalities to add:
	 * 	1. double-click to zoom
	 *  2. mouse wheel to zoom
	 *  3. click to drag
	 *  4. +/- buttons to zoom
	 */
	
	
//	var zoom = d3.behavior.zoom()
//		.translate(projection.translate())
//		.scale(projection.scale())
//		.scaleExtent([height, 8*height])
//		.on("zoom", zoomed)
//		
//	var g = svg.append("g")
//		.call(zoom);
	
	
  	var geoPath = d3.geo.path()
  		.projection( projection );

  	//create tooltip for mouseover printing
  	var tooltip = d3.select("body")
  		.append("div")
  		.attr("id", "tooltip")
  		//.attr("class", "tooltip")
  		.style("position", "absolute");
  	
	d3.json("data/us-states.json", function(json){
		console.log(json);
		state.selectAll("path")
		.data( json.features )
		.enter()
		.append( "path" )
		.attr("fill", "none")
		.attr("stroke", "#ccc")
		.attr("d", geoPath )
		//change color of entire state (and cbsa's) when moused over
		.on("mouseover", function(d,i){
			//d3.select(this).style("fill", "red");
			//tooltip.text(d.properties.name);
		})
		.on("mousemove", function(d,i){
			//tooltip.style("top", (event.pageY-10)+"px")
			//.style("left", (event.pageX+10)+"px");
			//console.log(d.properties.name);
		})
		//return to default color when not moused over
		.on("mouseout", function(d,i){
			//d3.select(this).style("fill", "none");
		});
	});
	
	d3.json("data/us-cbsa.json", function(json){
		console.log(json);
		cbsa.selectAll( "path" ) //creates pointers to paths
		.data( json.features ) //binds data to not yet created paths
		.enter() //creates new paths for each data element
		.append( "path" )
		.attr("fill", "blue")
		.attr( "stroke", "#999" )
		.attr( "d", geoPath ) //the letter d refers to the path
		.on("mouseover", function(d,i){
			val = data[currentCPC][currentYear][d.id]['normalized']
			tooltip.text(d.properties.NAME)
				.style("visibility", "visible");
		})
		.on("mousemove",function(d,i){
			tooltip.style("top", (event.pageY)+"px")
				.style("left", (event.pageX)+"px");
		})
		.on("mouseout", function(d,i){
			tooltip.style("visibility", "hidden");
		})
	});
		

	
//	state.selectAll("path")
//		.data( state_json.features )
//		.enter()
//		.append( "path" )
//		.attr("fill", "none")
//		.attr("stroke", "#ccc")
//		.attr("d", geoPath );
//
//	cbsa.selectAll( "path" )
//		.data( cbsa_json.features )
//		.enter()
//		.append( "path" )
//		.attr("fill", "blue")
//		.attr( "stroke", "#999" )
//		.attr( "d", geoPath );
	
}

//function quantize(d) {
//	return "q" + Math.floor(getCountyNorm1(d.id)) + "-9";
//}
//
//function getCountyNorm1(county){
//	try{
////		return data[county]['normalized'];
////		console.log("county data "+data['A'][county]['sum']);
//		return data[currentCPC][currentYear][county]['sum'];
//	}
//	catch(e){
//		return 0;
//	}
//}


		
		
