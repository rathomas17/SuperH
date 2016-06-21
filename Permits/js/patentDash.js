var xWidth;
var wHeight;
var scale;
var xHeight;
var minYear = 2005;
var maxYear = 2016;
var currentState = 'ALL';
var currentYear = 2015;
var patentSummeries;
//var data=new Array(new Array());
//var data=[];
var data = new Array();
data['ALL'] = new Array();
data['AK'] = new Array();
data['AR'] = new Array();
data['AS'] = new Array();
data['AZ'] = new Array();
data['CA'] = new Array();
data['CO'] = new Array();
data['CT'] = new Array();
data['DC'] = new Array();
data['DE'] = new Array();
data['FL'] = new Array();
data['GA'] = new Array();
data['GU'] = new Array();
data['HI'] = new Array();
data['IA'] = new Array();
data['ID'] = new Array();
data['IL'] = new Array();
data['IN'] = new Array();
data['KS'] = new Array();
data['KY'] = new Array();
data['LA'] = new Array();
data['MA'] = new Array();
data['MD'] = new Array();
data['ME'] = new Array();
data['MI'] = new Array();
data['MN'] = new Array();
data['MO'] = new Array();
data['MS'] = new Array();
data['MT'] = new Array();
data['NC'] = new Array();
data['ND'] = new Array();
data['NE'] = new Array();
data['NH'] = new Array();
data['NJ'] = new Array();
data['NM'] = new Array();
data['NV'] = new Array();
data['NY'] = new Array();
data['OH'] = new Array();
data['OK'] = new Array();
data['OR'] = new Array();
data['PA'] = new Array();
data['PR'] = new Array();
data['RI'] = new Array();
data['SC'] = new Array();
data['SD'] = new Array();
data['TX'] = new Array();
data['UT'] = new Array();
data['VA'] = new Array();
data['VI'] = new Array();
data['WA'] = new Array();
data['WI'] = new Array();
data['WV'] = new Array();
data['WY'] = new Array();
for (year=minYear; year<maxYear; year++){
	console.log('making array '+year);
	data['ALL'][year] = new Array();
	data['AK'][year] = new Array();
	data['AR'][year] = new Array();
	data['AS'][year] = new Array();
	data['AZ'][year] = new Array();
	data['CA'][year] = new Array();
	data['CO'][year] = new Array();
	data['CT'][year] = new Array();
	data['DC'][year] = new Array();
	data['DE'][year] = new Array();
	data['FL'][year] = new Array();
	data['GA'][year] = new Array();
	data['GU'][year] = new Array();
	data['HI'][year] = new Array();
	data['IA'][year] = new Array();
	data['ID'][year] = new Array();
	data['IL'][year] = new Array();
	data['IN'][year] = new Array();
	data['KS'][year] = new Array();
	data['KY'][year] = new Array();
	data['LA'][year] = new Array();
	data['MA'][year] = new Array();
	data['MD'][year] = new Array();
	data['ME'][year] = new Array();
	data['MI'][year] = new Array();
	data['MN'][year] = new Array();
	data['MO'][year] = new Array();
	data['MS'][year] = new Array();
	data['MT'][year] = new Array();
	data['NC'][year] = new Array();
	data['ND'][year] = new Array();
	data['NE'][year] = new Array();
	data['NH'][year] = new Array();
	data['NJ'][year] = new Array();
	data['NM'][year] = new Array();
	data['NV'][year] = new Array();
	data['NY'][year] = new Array();
	data['OH'][year] = new Array();
	data['OK'][year] = new Array();
	data['OR'][year] = new Array();
	data['PA'][year] = new Array();
	data['PR'][year] = new Array();
	data['RI'][year] = new Array();
	data['SC'][year] = new Array();
	data['SD'][year] = new Array();
	data['TX'][year] = new Array();
	data['UT'][year] = new Array();
	data['VA'][year] = new Array();
	data['VI'][year] = new Array();
	data['WA'][year] = new Array();
	data['WI'][year] = new Array();
	data['WV'][year] = new Array();
	data['WY'][year] = new Array();
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
	//patentSummeries;

	d3.select("#chosvg").remove();
	drawMap();
	console.log("new window width " + xWidth);
	$("#lineContainer").width(xWidth);
	$("#graphContainer").width(xWidth);
}
//resize();

function setup() {
	resize();

	d3.json("data/JSON/State_summary.json", function(json, error) {
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
			drawPatent('State_A');
		}

		//extend both divs to the bottom of the page
		pageHeight = Math.max($('#right').height(), $('#left').height());
		$('#right').height(pageHeight);
		$('#left').height($('#right').height());
	});

    d3.json("data/JSON/all_states.json", function(json,error) {
        StateData = json.StateData;
        StateData.forEach(function(p){
          p.sum = +(p.sum/100);
          p.normalized = +p.normalized;
          year = +p.year;
      		data[p.State][year][p.fips] = p;
        });
		counties.selectAll("path")
			.attr("class", quantize);
		});
		d3.selectAll('.currentYear').text(currentYear);
		d3.selectAll('.currentState').text(currentState);

		console.log("in setup");
		console.log(data["ALL"]["2015"]["22079"]);

}

function drawPatent(patent){
	console.log("patent " + patent);
	currentState = patent;
	currentState = currentState.replace("State_","");
	console.log('currentState '+currentState);

	counties.selectAll("path")
	.attr("class", quantize);

	d3.select("#currentLineGraph").remove();
	drawLine(patent);

	highlightRow(patent);

	d3.selectAll('.currentYear').text(currentYear);
	d3.selectAll('.currentState').text(currentState);

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
