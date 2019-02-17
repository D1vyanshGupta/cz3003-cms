from django.urls import path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
	path('', RedirectView.as_view(url='map')),
    # url(r'^healthCheck/', views.healthCheck),
    path('map', map_events)
]
