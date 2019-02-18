"""
    Module that acts like an Operator Controller
"""
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from utils.views import render_tab_view, is_operator, is_admin
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from utils.models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Reporter, Haze
from utils.dispatchers.agencydispatcher import AgencyDispatcher
from .tabview import OperatorTabViews
from utils.pullapis.dengue import DengueAPI
from utils.pullapis.weather import WeatherAPI

# def healthCheck(request):
#     return HttpResponse('It\'s all good! Operator UI works :)')


def lat_lng_to_point(string_obj):
    """
        Convert a given lattitude, longitude to a Point object
    """
    lat, lng = string_obj.split(',')
    return Point(float(lng), float(lat))


@login_required
def deactivate_event(request):
    """
        Deactivate an event
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
    event_id = request.GET.get('eventid')
    e = Event.objects.get(id=event_id)
    e.isactive = False
    e.save()
    operator = Operator.objects.get(user_ptr_id=request.user.id)
    event_log = EventTransactionLog.objects.create(
        event=e,
        transaction_type='ED',
        operator=operator,
        desc='DEACTIVATE event')
    event_log.save()
    AgencyDispatcher(event_log).dispatch()
    return redirect('/cms_operator/list')


@login_required
def update_event(request):
    """
        Update an event
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        reporter = {}
        event_type = request.POST.get('eventtype')
        event_id = request.POST.get('eventid')
        reporter['identification'] = request.POST.get('identification')
        try:
            reporter = Reporter.objects.get(
                identification=reporter['identification'])
        except Reporter.DoesNotExist:
            reporter['name'] = request.POST.get('name')
            reporter['contact_number'] = request.POST.get('contact')
            reporter = Reporter.objects.create(
                **reporter)
            reporter.save()
        edit_string = []
        if event_type == 'traffic':
            event = TrafficEvent.objects.get(id=event_id)
            if event.num_vehicles != int(request.POST.get('numVehicles')):
                event.num_vehicles = int(request.POST.get('numVehicles'))
                edit_string.append('UPDATE num_vehicles')
        elif event_type == 'terrorist':
            event = TerroristEvent.objects.get(id=event_id)
            if event.num_hostiles != int(request.POST.get('numHostiles')):
                event.num_hostiles = int(request.POST.get('numHostiles'))
                edit_string.append('UPDATE num_hostiles')
        if event.event.num_casualties != int(request.POST.get('numCasualties')):
            event.event.num_casualties = int(request.POST.get('numCasualties'))
            edit_string.append('UPDATE num_casualties')
        if event.event.num_injured != int(request.POST.get('numInjured')):
            event.event.num_injured = int(request.POST.get('numInjured'))
            edit_string.append('UPDATE num_injured')
        if event.event.description != request.POST.get('description'):
            event.event.description = request.POST.get('description')
            edit_string.append('UPDATE description')
        event.event.save()
        event.save()
        operator = Operator.objects.get(user_ptr_id=request.user.id)
        if operator not in event.event.operator.all():
            event.event.operator.add(operator)
        if reporter not in event.event.reporters.all() or reporter != event.event.first_responder:
            event.event.reporters.add(reporter)
        event_log = EventTransactionLog.objects.create(
            event=event.event,
            transaction_type='ED',
            operator=operator,
            reporter=reporter,
            desc=','.join(edit_string))
        event_log.save()
        AgencyDispatcher(event_log).dispatch()  # dispatch to agencies
        return redirect('/operator/list')
    else:
        return HttpResponseBadRequest()


@login_required
def new_event(request):
    """
        Create a new event
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
    if request.method == 'GET':
        tabs = OperatorTabViews()
        tabs.set_active_tab('newevent')
        data = {
            'eventtypes': enumerate(['Traffic Event', 'Terrorist Event'])
        }
        return render_tab_view(request, tabs, data)
    elif request.method == 'POST':
        event_details = {}
        reporter = {}
        event_type = request.POST.get('eventtype')
        reporter['identification'] = request.POST.get('identification')
        try:
            event_details['first_responder'] = Reporter.objects.get(
                identification=reporter['identification'])
        except Reporter.DoesNotExist:
            reporter['name'] = request.POST.get('name')
            reporter['contact_number'] = request.POST.get('contact')
            event_details['first_responder'] = Reporter.objects.create(
                **reporter)
            event_details['first_responder'] .save()

        operator = Operator.objects.get(user_ptr_id=request.user.id)
        event_details['description'] = request.POST.get('description')
        event_details['num_casualties'] = int(request.POST.get('numCasualties'))
        event_details['num_injured'] = int(request.POST.get('numInjured'))
        event_details['location'] = lat_lng_to_point(request.POST.get('location'))
        event = Event.objects.create(**event_details)
        event.save()
        event.operator.add(operator)

        event_log = EventTransactionLog.objects.create(
            event=event, transaction_type='CR', operator=operator)  # add the operator in later
        event_log.save()
        if event_type:
            specific_event_details = {'event': event}
            if event_type == 'traffic':
                specific_event_details['num_vehicles'] = int(
                    request.POST.get('numVehicles'))
                new_event = TrafficEvent.objects.create(**specific_event_details)
            elif event_type == 'terrorist':
                specific_event_details['num_hostiles'] = int(
                    request.POST.get('numHostiles'))
                specific_event_details[
                    'attack_type'] = request.POST.get('attacktype')
                new_event = TerroristEvent.objects.create(**specific_event_details)
            else:
                return HttpResponseBadRequest('nnok')
            new_event.save()
            AgencyDispatcher(event_log).dispatch()
            return redirect('/cms_operator/list')
        return HttpResponseBadRequest('nok')


@login_required
def list_events(request):
    """
        List all the events
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
    tabs = OperatorTabViews()
    tabs.set_active_tab('list')
    return render_tab_view(request, tabs, {
        'trafficevents': TrafficEvent.objects.filter(event__isactive=True),
        'terroristevents': TerroristEvent.objects.filter(event__isactive=True)
    })


# @login_required
def map_events(request):
    """
        Display events on the map
    """
    # if not isOperator(request.user):
    #     return HttpResponseBadRequest()
    tabs = OperatorTabViews()
    tabs.set_active_tab('map')
    return render_tab_view(request, tabs, {'haze': Haze.objects.all()})


def get_event_type(event):
    """
        Get an event type
    """
    if isinstance(event, TrafficEvent):
        return 'traffic'
    elif isinstance(event, TerroristEvent):
        return 'terrorist'


def get_event_update_form(request):
    """
        Update the event in the form
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
    context = {}
    event_id = request.GET.get('eventid')
    context['eventtype'] = request.GET.get('eventtype')
    if context['eventtype'] == 'traffic':
        context['event'] = TrafficEvent.objects.get(id=event_id)
    elif context['eventtype'] == 'terrorist':
        context['event'] = TerroristEvent.objects.get(id=event_id)
    else:
        return HttpResponseBadRequest()
    return render(request, 'operator/updateEventForm.html', context)


def get_events(request):
    """
        Get event list from the database
    """
    if not is_operator(request.user):
        return HttpResponseForbidden()
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


def get_event_type_icon(event_type):
    """
        Get the event type icon
    """
    if event_type == 'traffic':
        return 'caraccident.png'
    elif event_type == 'terrorist':
        return 'terrorist.png'

def get_events_geo_JSON(request):
    """
        Get JSON format of events
    """
    # if not isOperator(request.user):
    #     return HttpResponseBadRequest()
    data = {}
    geojson = {'type': 'FeatureCollection', 'features': []}
    events = getEvents(request)
    geojson['features'] = [{
        'type': 'Feature',
        'geometry': {
                'type': 'Point',
                'coordinates': [event['details'].event.location.x, event['details'].event.location.y]
        },
        'properties': {
            'type': event['type'],
            'icon': getEventTypeIcon(event['type']),
            'event': {
                'name': event['details'].event.first_responder.name,
                'description': event['details'].event.description,
                'operator': event['details'].event.operator.all()[0].name
            }
        }
    } for event in events]
    data['geojson'] = geojson
    return JsonResponse(data, safe=False)


def pull_weather(request):
    """
        Pull weather data from WeatherAPI
    """
    return JsonResponse(WeatherAPI().return_geo_json(), safe=False)

def refresh_API(request):
    """
        Refresh data on the map
    """
    WeatherAPI().pull_weather_update()
    DengueAPI().pull_update()
    WeatherAPI().pull_PSI_update()
    return HttpResponse('ok')
