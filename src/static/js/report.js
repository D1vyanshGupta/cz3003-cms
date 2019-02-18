var datetime = document.getElementById('time');
var endDateTime = Date.now();
var startDateTime = endDateTime - 30*60*1000;
endDateTime = new Date(endDateTime);
startDateTime = new Date(startDateTime);
datetime.innerHTML = "<b>Time period:</b> " + startDateTime.toLocaleString() + " - " + endDateTime.toLocaleString();

function displayTraffic(data){
	var accidents = document.getElementById('accidents');
	var vehicles = document.getElementById('vehicles');
	var trafficCasualties = document.getElementById('traffic-casualties');
	var trafficInjuries = document.getElementById('traffic-injuries');
	var trafficLocations = document.getElementById('traffic-locations');

	accidents.innerHTML = "Number of accidents: " + data['numTraffics'];
	vehicles.innerHTML = "Number of vehicle involved: " + data['numVehicles'];
	trafficCasualties.innerHTML = "Number of casualties: " + data['numCasualties'];
	trafficInjuries.innerHTML = "Number of injuries: " + data['numInjuries'];
	locationString = "Locations of accidents: ";
	locations = data['locations'];
	for(var i = 0;i < locations.length; i++){
		locationString += locations[i];
		locationString += ", ";
	}
	trafficLocations.innerHTML = locationString;
}

function displayTerrorist(data){
	var attacks = document.getElementById('attacks');
	var hostiles = document.getElementById('hostiles');
	var terroristCasualties = document.getElementById('terrorist-casualties');
	var terroristInjuries = document.getElementById('terrorist-injuries');
	var terroristLocations = document.getElementById('terrorist-locations');
	var terroristTypes = document.getElementById('terrorist-types');

	attacks.innerHTML = "Number of attacks: " + data['numAttacks'];
	hostiles.innerHTML = "Number of hostiles: " + data['numHostiles'];
	terroristCasualties.innerHTML = "Number of casualties: " + data['numCasualties'];
	terroristInjuries.innerHTML = "Number of injuries: " + data['numInjuries'];

	locationString = "Locations of attacks: ";
	locations = data['locations'];
	for(var i = 0;i < locations.length; i++){
		locationString += locations[i];
		locationString += ", ";
	}
	terroristLocations.innerHTML = locationString;

	var typeString = "Types of attacks: ";
	var types = data['attackTypes'];
	for(var i = 0;i < types.length; i++){
		typeString += types[i];
		typeString += ", ";
	}
	terroristTypes.innerHTML = typeString;
}

function displayCrisis(data){
	$.each(data, function(key,value){
		$('#districts').append('<li>' + key +': ' + value+'</li>');
	});
}

$.ajax( {
	url: '/pmo_report/get_crisis_info',
	dataType: 'json'
}).done(function (data) {
	displayCrisis(data);
});

$.ajax({
	url: '/pmo_report/get_traffic_info',
	data: {},
	dataType: 'json'
}).done(function (data) {
	displayTraffic(data);
});

$.ajax({
	url: '/pmo_report/get_terrorist_info',
	data: {},
	dataType: 'json'
}).done(function (data) {
	displayTerrorist(data);
});
