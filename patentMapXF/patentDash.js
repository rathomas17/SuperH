var xWidth;
var wHeight;
var scale;
var xHeight;
var minYear = 2005;
var maxYear = 2016;
var currentCPC = 'A';
var currentYear = 2015;
var patentSummeries
//var data=new Array(new Array());
//var data=[];
var data = new Array();
data['A'] = new Array();
data['B'] = new Array();
data['C'] = new Array();
data['D'] = new Array();
data['E'] = new Array();
data['F'] = new Array();
data['G'] = new Array();
data['H'] = new Array();
data['Y'] = new Array();
for (year=minYear; year<maxYear; year++){
	console.log('making array '+year);
	data['A'][year] = new Array();
	data['B'][year] = new Array();
	data['C'][year] = new Array();
	data['D'][year] = new Array();
	data['E'][year] = new Array();
	data['F'][year] = new Array();
	data['G'][year] = new Array();
	data['H'][year] = new Array();
	data['Y'][year] = new Array();
}
//data['A'] = new Array();
//data['B'] = new Array();
//data['C'] = new Array();
//data['D'] = new Array();
//data['E'] = new Array();
//data['F'] = new Array();
//data['G'] = new Array();
//data['H'] = new Array();
//data['Y'] = new Array();
var maxCounty = 0.0;
function resize(){
	xWidthLineGraph = document.getElementById("lineColumn").offsetWidth;
	scale = xWidthLineGraph/960;
	xHeightLineGraph = 500*scale;
	console.log("resize xWidthLineGraph "+xWidthLineGraph+"; wHeight "+xHeightLineGraph);


	xWidth = document.getElementById("graphs").offsetWidth;
	wHeight = $(window).height();
	console.log("window width " + xWidth);
	console.log("resize xwdith "+xWidth+"; wHeight "+wHeight);

	if (xWidth < wHeight){
		console.log("wide window");
		xWidth = Math.max((xWidth - 50)/2 - 20, 400);
	}
	else {
		xWidth = xWidth - 60;
		xWidth = Math.max(xWidth, 400);
	}
	scale = xWidth/960;
	xHeight = 500*scale;
	patentSummeries;

	d3.select("#chosvg").remove();
	drawMap();
	console.log("new window width " + xWidth);
	$("#lineContainer").width(xWidth);
	$("#graphContainer").width(xWidth);
}
//resize();

function setup() {
	resize();

	d3.json("data/cpc_summary.json", function(json, error) {
		patentSummeries = json;
	    console.log("patentSummeries in wrapper ");
	    console.log(patentSummeries);
		setUpTable(patentSummeries);

		var urlpatent = window.location.search.replace('?','').replace('/','').replace(/%20/g, ' ');
		console.log(urlpatent);
		if (patentSummeries[urlpatent]){
			drawPatent(urlpatent);
		}
		else {
			drawPatent('cpc_A');
		}

		//extend both divs to the bottom of the page
		pageHeight = Math.max($('#right').height(), $('#left').height());
		$('#right').height(pageHeight);
		$('#left').height($('#right').height());
	});

    d3.json("data/cpc_xf.json", function(json,error) {
//	data = json;
        cpcData = json.cpcData;
        cpcData.forEach(function(p){
//           console.log("p.cpc "+p.cpc+"; p.fips "+p.fips);
//	       data[p.cpc] = p;
              p.sum = +p.sum
              p.normalized = +p.normalized
              year = +p.year;
	       data[p.cpc][year][p.fips] = p;
//             console.log(p);
           }
        );

	//for (var key in data){
	//    if (data.hasOwnProperty(key)) {
		//console.log("key " + key + " data[key] " + data[key]);
	//    }
	//}
//	    console.log(json);
		counties.selectAll("path")
				.attr("class", quantize);
	});
	d3.selectAll('.currentYear').text(currentYear);
	d3.selectAll('.currentCPC').text(currentCPC);


}

function drawPatent(patent){
	console.log("patent " + patent);
	currentCPC = patent;
	currentCPC = currentCPC.replace("cpc_","");
	console.log('currentCPC '+currentCPC);

//	d3.json("data/"+patent+"_countyDisplay.json", function(json) {
//	    data = json;
//	    console.log(data);
//		counties.selectAll("path")
//				.attr("class", quantize);
//	});
//	d3.json("data/cpc_C_year_fips.json", function(json) {
//    d3.json("data/"+patent+"_year_fips.csv", function(json,error) {

	//for (var key in data){
	//    if (data.hasOwnProperty(key)) {
		//console.log("key " + key + " data[key] " + data[key]);
	//    }
	//}
//	    console.log(json);
		counties.selectAll("path")
				.attr("class", quantize);
//	});

	d3.select("#currentLineGraph").remove();
	drawLine(patent);

//	history.replaceState(null, null, window.location.pathname + "?" + patent +'/');
	highlightRow(patent);

	d3.selectAll('.currentYear').text(currentYear);
	d3.selectAll('.currentCPC').text(currentCPC);

}

function showfaq(){
	$(function() {
        $( "#faq" ).dialog(
        	{title: "FAQ",
        	minWidth:600,
        	position: [390,80]}
        );
    });
}

window.onload = setup;
//window.onresize = setup;
