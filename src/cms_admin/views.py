"""
    This module acts like an AdminController
"""
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from utils.models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Singapore, CrisisTransactionLog, Haze
from .tabview import AdminTabViews
from utils.views import render_tab_view, is_operator, is_admin
from utils.districts.districts import DistrictManager, CrisisManager
from utils.dispatchers.pmodispatcher import PMODispatcher
from django.template.defaulttags import register
import json
import requests
from utils.crisiscalculation.calculation import CrisisCalculator
from django.contrib.auth.decorators import login_required

# def healthCheck(request):
#     return HttpResponse('It\'s all good! Admin UI works :)')


def get_transaction_log(request):
    """
        Get the transaction log from the database
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    tabs = AdminTabViews()
    tabs.set_active_tab('log')
    event_type_dict = {}
    return render_tab_view(request, tabs, {
        'eventTransactionLog': EventTransactionLog.objects.all(),
        'crisisLogDatabase': CrisisTransactionLog.objects.all(),
    })


def get_crisis_view(request):
    """
        Set crisis manager as active tab
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    tabs = AdminTabViews()
    tabs.set_active_tab('crisis')
    return render_tab_view(request, tabs, {
    })


@register.filter(name='type')
def get_event_type(log):
    """
        Choose an event type as active tab
    """
    if (TrafficEvent.objects.filter(event=log.event).exists() == True):
        return 'Traffic'
    if (TerroristEvent.objects.filter(event=log.event).exists() == True):
        return 'Terrorist'
    return None


@register.filter(name='address')
def get_address_from_lat_long(latlong):
    """
        Take the location address from given lattitude, longitude
    """
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % (
        latlong.y, latlong.x)
    r = requests.get(url)
    result = r.json()
    address = ""
    if (len(result.get('results')) > 0):
        for x in result.get('results')[0].get('address_components'):
            address += x.get('long_name') + ', '
        return address[:-2]
    else:
        return ""


@register.filter(name='tran')
def get_long_transaction_type(log):
    """
        Display the transaction type
    """
    return log.get_transaction_type_display()


@register.filter(name='adminop')
def get_admin_or_operator(log):
    """
        Choose admin or operator as active tab
    """
    if log.operator is not None:
        return log.operator
    if log.admin is not None:
        return log.admin
    return '-'


def get_districts(request):
    """
        Return the districts data
    """
    return JsonResponse(DistrictManager().return_geo_json(), safe=False)


@login_required
def set_crisis(request):
    """
        Set crisis level
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    CrisisManager().set_crisis_level(
        request.GET.get('district'), request.GET.get('newcrisis'), None)

    return HttpResponse("Success", content_type="text/plain")


def map_events(request):
    """
        Display events on the map
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    tabs = AdminTabViews()
    tabs.set_active_tab('map')
    return render_tab_view(request, tabs, {'haze': Haze.objects.all()})


@login_required
def list_events(request):
    """
        Return a list of events
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    tabs = AdminTabViews()
    tabs.set_active_tab('list')
    return render_tab_view(request, tabs, {
        'trafficevents': TrafficEvent.objects.filter(event__isactive=True),
        'terroristevents': TerroristEvent.objects.filter(event__isactive=True)
    })


@login_required
def delete_event(request):
    """
        Method to delete an event
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    if request.method == 'GET':
        event_id = request.GET.get('eventid')
        event_type = request.GET.get('eventtype')
        if (event_type == 'traffic'):
            t = TrafficEvent.objects.get(id=event_id)
            e = Event.objects.get(id=t.event.id)
            e.delete()
        elif (event_type == 'terrorist'):
            t = TerroristEvent.objects.get(id=event_id)
            print(t.event.id)
            e = Event.objects.get(id=t.event.id)
            e.delete()
        return HttpResponse("Success", content_type="text/plain")


@login_required
def crisis_calculator(request):
    """
        Show suggested crisis
    """
    if not is_admin(request.user):
        return HttpResponseForbidden()
    tabs = AdminTabViews()
    tabs.set_active_tab('calculator')
    crises = CrisisCalculator().check_crisis()
    print(crises)
    return render_tab_view(request, tabs, data={'crises': crises})


@login_required
def report_manager(request):
    tabs = AdminTabViews()
    tabs.set_active_tab('reportmanager')
    return render_tab_view(request, tabs)


def send_report(request):
    PMODispatcher().dispatch(False)
    return JsonResponse({'success': True})
