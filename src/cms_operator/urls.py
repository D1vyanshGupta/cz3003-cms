from django.urls import path
from django.views.generic import RedirectView
from .views import *


urlpatterns = [
	path('', RedirectView.as_view(url='new')),
    # url(r'^healthCheck/', views.healthCheck),
    path('new', new_event),
    path('list', list_events),
    path('map', map_events),
    path('update_event', update_event),
    path('deactivate_event', deactivate_event),
	path('activate_event', activate_event),
    path('get_event_update_form', get_event_update_form),
]
