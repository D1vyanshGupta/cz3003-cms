
"""
    A general controller
"""
from django.contrib.auth import authenticate, login as dologin, logout

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

from .districts.districts import DistrictManager

from .models import Operator, Admin
from .models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Reporter, Haze
from .pullapis.weather import WeatherAPI
from .pullapis.dengue import DengueAPI

import os
from .tabview import TabViews


def is_user_type(user, usercls):
    """
        Check if user is of usercls type
    """
    try:
        u = usercls.objects.get(user_ptr=user.id)
        return True
    except:
        return False


def is_operator(user):
    """
        Check if user is operator
    """
    return is_user_type(user, Operator)


def is_admin(user):
    """
        Check if user is admin
    """
    return is_user_type(user, Admin)


# def healthCheck(request):
#     return HttpResponse('It\'s all good!')


def get_user_type(request):
    """
        Get user type if authenticated. If not, user is public.
    """
    if request.user.is_authenticated:
        if is_admin(request.user):
            return 'Admin'
        elif is_operator(request.user):
            return 'Operator'
    else:
        return 'Public'


def render_tab_view(request, tabs, data={}):
    """
        Wrapper method for rendering tab view
    """
    active_tab = tabs.get_active_tab()
    if active_tab:
        return render(request, active_tab.template,
                      {'title': active_tab.title,
                       'data': data,
                       'usertype': get_user_type(request),
                       'tabs': tabs.tabs})
    else:
        return HttpResponse('ERROR')


# def register_operator(request, username, email, password):
#     """
#         Method to create Operator
#     """
#     if not is_operator(Operator.objects.all(), username):
#         new_operator = Operator.objects.create_user(username, email, password)
#         new_operator.save()
#         return HttpResponse("Operator created!")
#     return HttpResponse("Operator existed!")


def login_view(request):
    """
        View function to process login
    """
    user = request.user
    if user is not None:
        # login as an operator
        if is_operator(user):
            return redirect('/cms_operator/map')

        # login as an admin
        elif is_admin(user):
            return redirect('/cms_admin/map')
        else:
            return HttpResponse("Disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


# def logout_view(request):
#     """
#         Process log out action and redirect to login page
#     """
#     logout(request)
#     return redirect('/login')


def get_weather_info(request):
    """
        Method to make API call to get GeoJSON Weather data for Google Map. Includes
            - Weather
            - Haze info
    """
    return JsonResponse(WeatherAPI().return_geo_json(), safe=False)


def get_dengue_info(request):
    """
        Method to make API call to get GeoJSON Dengue data. Includes
            - Dengue hotzones
    """
    return JsonResponse(DengueAPI().return_geo_json(), safe=False)

def get_district_info(request):
    """
        Return the districts data
    """
    return JsonResponse(DistrictManager().return_geo_json(), safe=False)

def refreshAPI(request):
    """
        Refresh the information on the map
    """
    WeatherAPI().pull_weather_update()
    DengueAPI().pull_update()
    WeatherAPI().pull_PSI_update()
    return HttpResponse('ok')


def get_events_geo_JSON(request):
    """
        Get geo JSON format of events
    """
    data = {}
    geojson = {'type': 'FeatureCollection', 'features': []}
    events = get_events(request)
    geojson['features'] = [{
        'type': 'Feature',
        'geometry': {
                'type': 'Point',
                'coordinates': [event['details'].event.location.x, event['details'].event.location.y]
        },
        'properties': {
            'type': event['type'],
            'icon': get_event_type_icon(event['type']),
            'event': {
                'name': event['details'].event.first_responder.name,
                'description': event['details'].event.description,
                'operator': event['details'].event.operator.all()[0].name
            }
        }
    } for event in events]
    data['geojson'] = geojson
    return JsonResponse(data, safe=False)


def get_events(request):
    """
        Get an event list from the database
    """
    events_list = []
    events_list.extend(TrafficEvent.objects.filter(event__isactive=True))
    events_list.extend(TerroristEvent.objects.filter(event__isactive=True))
    events_list = [{
        'type': get_event_type(e),
        'details': e
    }
        for e in sorted(events_list, key=lambda x: x.event.date_recorded, reverse=True)
    ]
    return events_list


def get_event_type_icon(eventtype):
    """
        Get an event type icon
    """
    if eventtype == 'traffic':
        return 'caraccident.png'
    elif eventtype == 'terrorist':
        return 'terrorist.png'


def get_event_type(event):
    """
        Get an event type
    """
    if isinstance(event, TrafficEvent):
        return 'traffic'
    elif isinstance(event, TerroristEvent):
        return 'terrorist'
