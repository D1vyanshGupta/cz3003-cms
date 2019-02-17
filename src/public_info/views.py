"""
    This module acts like an PublicController
"""
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from utils.models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Singapore, CrisisTransactionLog, Haze
from .tabview import PublicTabViews
from utils.views import render_tab_view, is_operator, is_admin
from utils.districts.districts import DistrictManager, CrisisManager
from django.template.defaulttags import register
import json, requests
from django.contrib.auth.decorators import login_required

def map_events(request):
    """
        Display events on the map
    """
    # if not isOperator(request.user):
    #     return HttpResponseBadRequest()
    tabs = PublicTabViews()
    tabs.set_active_tab('map')
    return render_tab_view(request, tabs, {'haze': Haze.objects.all()})
