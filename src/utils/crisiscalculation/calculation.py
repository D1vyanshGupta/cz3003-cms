"""
    Module that performs crisis calculation
"""
from ..models import TrafficEvent, TerroristEvent, Singapore, District
from ..dispatchers.pmodispatcher import PMODispatcher


class InvalidSeverityException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Invalid severity value: ' + repr(self.value)


class CrisisCalculator:

    """
        Module to perform crisis calculation automatically
    """
    SEVERITY_THRESHOLD_BINS = [100, 150, 300, 500, 750]

    def event_severity_calculator(self, event):
        """
            Event severity calculator
        """
        severity = 20 * event.event.num_casualties + \
            10 * event.event.num_injured
        if isinstance(event, TrafficEvent):
            severity += 8 * event.num_vehicles
        elif isinstance(event, TerroristEvent):
            severity += 20 * event.num_hostiles
        else:
            return 0.0
        return severity

    def get_crisis_level(self, severity):
        """
            Return the crisis level
                - 0 <= severity < 1
        """
        if severity < 0:
            raise InvalidSeverityException(severity)
        for i in range(len(self.SEVERITY_THRESHOLD_BINS)):
            if severity < self.SEVERITY_THRESHOLD_BINS[i]:
                return i
        return 5

    def get_events(self, geom):
        """
            Get events from the database
        """
        events = []
        events.extend(TrafficEvent.objects.filter(event__location__within=geom))
        events.extend(
            TerroristEvent.objects.filter(event__location__within=geom))
        return events

    def check_crisis(self):
        """
            Check the crisis in different regions in the map
        """
        singapore = Singapore.objects.all()
        new_crises = {}
        crises = {}
        for singapore_obj in singapore:
            total_severity = sum([self.event_severity_calculator(event)
                                  for event in self.get_events(singapore_obj.geom)])
            print(singapore_obj.name_1, total_severity)
            crisis_level = self.get_crisis_level(total_severity)
            district = Districts.objects.get(district=singapore_obj.name_1)
            crises[district.district] = crisis_level
            if district.crisis >= crisis_level:
                continue
            else:
                new_crises[district.district] = crisis_level
                # district.crisis = crisis_level
        PMODispatcher().emergency_dispatch(new_crises)
        return crises
