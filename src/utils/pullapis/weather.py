"""
    Weather API from NEA
"""

import json
import requests
from datetime import datetime
from xml.etree import ElementTree
from ..models import Weather, Haze
from django.contrib.gis.geos import Point

class WeatherAPI:

    """
            WeatherAPI Class for weather.py
    """

    NOWCAST_URL = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time='

    PSI_URL = 'https://api.data.gov.sg/v1/environment/psi?date_time='

    def pull_update(self):
        """
                Pulls Weather info from NEA:
                Includes
                    - Weather Info
                    - PSI Info
                    - PM2.5 Info
        """
        try:
            w = self.pull_weather_update()
            p = self.pull_PSI_update()
            return w and p
        except:
            return False

    def pull_weather_update(self):
        """
            Pulls Nowcast data
        """

        time_str = str(datetime.now()).split('.')[0].replace(' ', 'T')
        request_url = self.NOWCAST_URL + time_str
        r = requests.get(request_url)

        if (r.status_code == 200):
            json_data = json.loads(r.text)
            area_metadata = json_data['area_metadata']

            area_info = {}
            for area_data in area_metadata:
                area_name = area_data['name']
                lat = area_data['label_location']['latitude']
                long = area_data['label_location']['longitude']
                area_info[area_name] = {'latitude': lat, 'longitude': long}

            forecasts = json_data['items'][0]['forecasts']

            for area_forecast in forecasts:
                area_name = area_forecast['area']
                forecast = area_forecast['forecast']
                area_info[area_name]['forecast'] = forecast

            for area_name, info in area_info.items():
                weather_obj, created = Weather.objects.update_or_create(
                area_name=area_name, location=Point(info['longitude'], info['latitude']))
                weather_obj.condition = info['forecast']
                weather_obj.save()

            return True

        else:
            print(r.status_code)
            return False

    def pull_PSI_update(self):
        """
            Pulls PSI Data
        """

        time_str = str(datetime.now()).split('.')[0].replace(' ', 'T')
        request_url = self.PSI_URL + time_str
        r = requests.get(request_url)

        if (r.status_code == 200):
            json_data = json.loads(r.text)
            region_metadata = json_data['region_metadata']

            region_info = {}
            for region_data in region_metadata:
                region_name = region_data['name']
                lat = region_data['label_location']['latitude']
                long = region_data['label_location']['longitude']
                region_info[region_name] = {'latitude': lat, 'longitude': long}

            readings = json_data['items'][0]['readings']

            pm_10_readings = readings['pm10_sub_index']

            pm_25_readings = readings['pm25_sub_index']

            psi_24_hr_readings = readings['psi_twenty_four_hourly']

            for region_name in region_info:
                region_info[region_name]['pm_10'] = pm_10_readings[region_name]
                region_info[region_name]['pm_25'] = pm_25_readings[region_name]
                region_info[region_name]['psi'] = psi_24_hr_readings[region_name]

            for region_name, info in region_info.items():
                haze_obj, created = Haze.objects.update_or_create(
                    region_name=region_name, location=Point(info['longitude'], info['latitude']))

                haze_obj.psi = info['psi']
                haze_obj.pm_10 = info['pm_10']
                haze_obj.pm_25 = info['pm_25']

                haze_obj.save()

            return True
        else:
            print(r.status_code)
            return False

    def get_nowcast_details(self, long_form):
        """
                returns long form of nowcast
        """
        return {
            'Mist': ('BR', 'haze.png'),
            'Cloudy': ('CL', 'darkcloud.png'),
            'Drizzle': ('DR', 'lightrain.png'),
            'Fair (Day)': ('FA', 'sunny.png'),
            'Fog': ('FG', 'haze.png'),
            'Fair (Night)': ('FN', 'clearnight.png'),
            'Fair & Warm': ('FW', 'hot.png'),
            'Heavy Thundery Showers with Gusty Winds': ('HG', 'thunderstorm.png'),
            'Heavy Rain': ('HR', 'rain.png'),
            'Heavy Showers': ('HS', 'shower.png'),
            'Heavy Thundery Showers': ('HT', 'thunderstorm.png'),
            'Hazy': ('HZ', 'haze.png'),
            'Slightly Hazy': ('LH', 'haze.png'),
            'Light Rain': ('LR', 'lightrain.png'),
            'Light Showers': ('LS', 'lightrain.png'),
            'Overcast': ('OC', 'darkcloud.png'),
            'Partly Cloudy (Day)': ('PC', 'partialsun.png'),
            'Partly Cloudy (Night)': ('PN', 'partialnight.png'),
            'Passing Showers': ('PS', 'shower.png'),
            'Moderate Rain': ('RA', 'rain.png'),
            'Showers': ('SH', 'shower.png'),
            'Strong Winds, Showers': ('SK', 'shower.png'),
            'Snow': ('SN', 'snow.png'),
            'Strong Winds, Rain': ('SR', 'rain.png'),
            'Snow Showers': ('SS', 'snow.png'),
            'Sunny': ('SU', 'sunny.png'),
            'Strong Winds': ('SW', 'superwindy.png'),
            'Thundery Showers': ('TL', 'thunderstorm.png'),
            'Windy, Cloudy': ('WC', 'windy.png'),
            'Windy': ('WD', 'windy.png'),
            'Windy, Fair': ('WF', 'windy.png'),
            'Windy, Rain': ('WR', 'rain.png'),
            'Windy, Showers': ('Ws' 'shower.png')
        }[long_form]

    def return_geo_json(self):
        """
                returns GeoJson Data to be added into map
        """
        weather = Weather.objects.all()
        geojson = {'type': 'FeatureCollection', 'features': []}
        for w in weather:
            short_form, icon = self.get_nowcast_details(w.condition)
            geojson['features'].append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [w.location.x, w.location.y]
                },
                'properties': {
                    'type': 'weather',
                    'name': w.area_name,
                    'condition_short': short_form,
                    'condition_long': w.condition,
                    'icon': icon
                }
            })
        return geojson
