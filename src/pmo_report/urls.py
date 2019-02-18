from django.urls import path
from .views import *

urlpatterns = [
    path('get_traffic_info', get_traffic_info),
    path('get_terrorist_info', get_terrorist_info),
    path('get_map_image', get_map_image),
    path('get_crisis_info', get_crisis_info)
]
