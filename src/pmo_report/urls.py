from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url('get_traffic_info', get_traffic_info),
    url('get_terrorist_info', get_terrorist_info),
    url('get_map_image', get_map_image),
    url('get_crisis_info', get_crisis_info)
]
