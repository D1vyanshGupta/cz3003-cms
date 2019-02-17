"""
    Module that display Views
"""
class TabView:
    """
        A tab view
    """
    tab_id = ''
    url = ''
    is_active = False
    tab_title = ''
    template = ''
    icon = ''

class MapView(TabView):
    """
        A map view
    """
    tab_id = 'map'
    icon = 'map'
    url = 'map'
    title = 'Map'

class ListView(TabView):
    """
        A list view
    """
    tab_id = 'list'
    icon = 'list'
    url = 'list'
    title = 'List'

class TabViews:
    """
        Wrapper class to encapsulate tab views.
    """

    def __init__(self):
        """
            Initiate class with the required TabView classes in self.tabs
        """
        self.tabs = []

    def set_active_tab(self, tab_id):
        """
            Takes a tab_id and sets the active tab to the one with matching tab_id
        """
        for tab in self.tabs:
            if tab_id == tab.tab_id:
                tab.is_active = True
            else:
                tab.is_active = False

    def get_active_tab(self):
        """
            Return the active tab
        """
        for tab in self.tabs:
            if tab.is_active:
                return tab
