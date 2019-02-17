from django.urls import path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='log')),
    # url(r'^healthCheck/', views.healthCheck),
    path('log', get_transaction_log),
    path('crisis', get_crisis_view),
    path('get_districts', get_districts),
    path('set_crisis', set_crisis),
    path('map', map_events),
    path('list', list_events),
    path('report', report_manager),
    path('delete_event', delete_event),
    path('send_report', send_report),
    path('suggested_crisis', crisis_calculator)
]
