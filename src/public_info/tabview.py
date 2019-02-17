"""
    View module for admin
"""
from utils.tabview import TabView, TabViews, MapView


class PublicMapView(MapView):
    """
        View for admin to see the map
    """
    url = 'public/map'
    template = 'common/map.html'


class PublicTabViews(TabViews):
    """
        Tab view to switch between different views for admin
    """
    def __init__(self):
        self.tabs = [PublicMapView()]
