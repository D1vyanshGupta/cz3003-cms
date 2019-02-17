var marker;

function generateInfoWindowHtml(event){
    var html = '<div class="marker-content"><p>' +
        '<strong> Reported by: </strong> ' + event['name'] + '<br/>' +
        '<strong> Description: </strong>' + event['description'] + '<br/>' +
        '<strong> Operator: </strong>' + event['operator'] + '<br/>' +
        '</p></div>';
    return html;
}

function initMap() {
    var mapDiv = document.getElementById('map');
    var infowindow =  new google.maps.InfoWindow();
    var weatherGeoJSON, eventsGeoJSON, dengueGeoJSON;

    var map = new google.maps.Map(mapDiv, {
      center: {lat: 1.364922150947930, lng: 103.80912780761719},
      zoom: 11
    });

    $.ajax({
    url: 'getEventsGeoJSON',
    data: {},
    dataType: 'json'
  }).done(function(data, textStatus, jqXHR) {
        eventsGeoJSON = data['geojson'];
    map.data.addGeoJson(data['geojson']);                
  }).fail(function(){
    console.log('failed'); // some proper failure message
  });
    
    $.ajax({
            url: '/getWeatherInfo',
            dataType: 'json'
        }).done(function (data) {
             weatherGeoJSON = data;
             map.data.addGeoJson(data);
        });

    $.ajax({
            url: '/getDengueInfo',
            dataType: 'json'
        }).done(function (data) {
            dengueGeoJSON = data;
            map.data.addGeoJson(data);
    })

    map.data.addListener('click', function(event) {
        var feature = event.feature
        var iconbase = '/static/img/';
        var type = feature.getProperty('type');
        if (type == 'weather') {
            infowindow.setContent("<div style='width:170px; text-align:center;'><b>"+feature.getProperty('name') + "</b><hr style='margin:3px;'/> <img src='" + iconbase+feature.getProperty('icon')+"' height= 30px width = 30px/>  "+ feature.getProperty('condition_long')+"</div>");
            infowindow.setPosition(feature.getGeometry().get());
            infowindow.setOptions({pixelOffset: new google.maps.Size(0,-30)});
            infowindow.open(map);
        }
        else if (type == 'dengue') {
            infowindow.setContent("<div style='width:170px; text-align:center;'><b>"+feature.getProperty('locality') + "</b><hr style='margin:3px;'/> <img src='" + iconbase+'dengue.png'+"' height= 30px width = 30px/>  Cases:"+ feature.getProperty('case_size')+"<br/><a target='__blank'   href='"+feature.getProperty('hyperlink')+ "'>More details<a/></div>");
            var bounds=new google.maps.LatLngBounds();
            feature.getGeometry().getArray().forEach(function(path){
                path.getArray().forEach(function(path2){
                    path2.getArray().forEach(function(latLng){
                        bounds.extend(latLng);
                        console.log(latLng)
                    });
                });
            });
            infowindow.setPosition(bounds.getCenter());
            infowindow.open(map);
        }
        else if (type == 'traffic' || type == 'terrorist'){
            var html = generateInfoWindowHtml(feature.getProperty('event'));
            infowindow.setContent(html);
            infowindow.setPosition(feature.getGeometry().get());
            infowindow.setOptions({pixelOffset: new google.maps.Size(0,-30)});
            infowindow.open(map);
        } 
    });  

    map.data.setStyle(function(feature) {
        var iconbase = '/static/img/';
        var type = feature.getProperty('type');
        if (type == 'weather') {
          return {
            icon: {
                url:iconbase + feature.getProperty('icon'),
                scaledSize: {
                    width: 30,
                    height:30
                }
            },
            title: feature.getProperty('name') + ":" + feature.getProperty('condition_long')
          };
        }
        if (type == 'dengue') {
            if (feature.getProperty('case_size') <10) {
                return {
                    fillColor: "rgb(241, 196, 15)",
                    strokeColor: "rgb(243, 156, 18)",
                    strokeWeight: 2
                }
            }
            if (feature.getProperty('case_size') < 20) {
                return {
                    fillColor: "rgb(230, 126, 34)",
                    strokeColor: "rgb(230, 126, 34)",
                    strokeWeight: 2
                }
            }
            else {
                return {
                    fillColor: "rgb(192, 57, 43)",
                    strokeColor: "rgb(192, 57, 43)",
                    strokeWeight: 2
                }
            }
        } 
        else if (type == 'traffic' || type == 'terrorist'){
            return {
                'icon': {
                    url: iconbase + feature.getProperty('icon'),
                    scaledSize: {
                        'width': 30,
                        'height': 30
                    }
                }
            };
        }
    });
    $('.filter-option input[type="checkbox"]').change(function(){
                filters = [];
                map.data.forEach(function(feature) { // remove all
                    map.data.remove(feature);
                });
                // add all
                map.data.addGeoJson(weatherGeoJSON);
                map.data.addGeoJson(eventsGeoJSON);
                map.data.addGeoJson(dengueGeoJSON);
                // selectively remove
                $('input[name="filter"]:checked').each(function(idx, elem){
                    filters.push($(elem).val());
                });
                map.data.forEach(function(feature) {
                    if (filters.indexOf(feature.getProperty('type')) == -1) {
                        map.data.remove(feature);
                    }
                });
    });

    $('.haze-filter-option input[type="checkbox"]').change(function(){
        $('#haze').toggle();
    });
}
$(document).ready(function(){
    $('#refreshAPI').click(function() {
         $.ajax({
            url: 'refreshAPI',
        }).done (function() {
            location.reload();
        })
    });
});