from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin as djangoadmin
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

from .views import *

urlpatterns = [
    path('login_view', login_view, name='login_view'),
    # url('login', TemplateView.as_view(template_name='login.html')),
    # url('^logout', views.logout_view),
    path('index', TemplateView.as_view(template_name='index.html'), name='index'),
    path('report/', TemplateView.as_view(template_name='report.html'), name='report'),
    path('get_weather_info', get_weather_info),
    path('get_dengue_info', get_dengue_info),
    path('refreshAPI', refreshAPI),
    path('get_district_info', get_district_info),
    path('get_events_geo_JSON', get_events_geo_JSON),
    path('maps/weather', TemplateView.as_view(template_name='maps/weather.html'), name='weather_map'),
    path('maps/dengue', TemplateView.as_view(template_name='maps/dengue.html'), name='dengue_map'),
    path('maps/terrorist', TemplateView.as_view(template_name='maps/terrorist.html'), name='terrorist_map'),
    path('maps/traffic', TemplateView.as_view(template_name='maps/traffic.html'), name='traffic_map'),
    path('maps/crisis', TemplateView.as_view(template_name='maps/crisis.html'), name='crisis_map'),
    path('', RedirectView.as_view(url='public'), name='public')
    ]
