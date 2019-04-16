from django.test import TestCase
from django.test import Client
from utils.models import Admin, Operator, Event, EventTransactionLog, TrafficEvent, TerroristEvent, Reporter, CrisisTransactionLog
from utils.dispatchers.socialmediadispatcher import SocialMediaDispatcher
from utils.dispatchers.agencydispatcher import AgencyDispatcher
from utils.pullapis.weather import WeatherAPI
from utils.pullapis.dengue import DengueAPI
from utils.pushapis.fb import FacebookAPI
from utils.pushapis.twitter import TwitterAPI
from utils.pushapis.sms import TwilioAPI
from utils.pushapis.email_api import EmailAPI
from utils.crisiscalculation.calculation import CrisisCalculator, InvalidSeverityException
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
import random

# Create your tests here.
testEvent = {
    'description': 'Test Event',
    'num_casualties': 10,
    'num_injured': 5,
    'location': Point(103.8, 1.36)
}

testReporter = {
    'name': 'Tester',
    'contact_number': '1234',
    'identification': 'S12345K'
}

def createNewEvent():
    usr, created = User.objects.get_or_create(
        username='test', password='testpassword', email='test@test.com')
    usr.save()
    op = Operator.objects.create(user_ptr_id=usr.id, name='Test Operator')
    rep = Reporter.objects.create(**testReporter)
    ev = testEvent
    ev['first_responder'] = rep
    ev = Event.objects.create(**testEvent)
    ev.save()
    ev.operator.add(op)
    evlog = EventTransactionLog.objects.create(
        event=ev, transaction_type='CR', operator=op, reporter=rep)
    return ev, evlog


class EventsTest(TestCase):

    def setUp(self):
        event, log = createNewEvent()
        pass


class AgencyDispatcherTest(TestCase):

    def setUp(self):
        self.event, self.log = createNewEvent()

    def test_agency_message_traffic(self):
        self.traffic_event = TrafficEvent.objects.create(
            event=self.event, num_vehicles=20)
        self.assertEqual(
            AgencyDispatcher(self.log).construct_message(), 'New traffic incident at 1.360000, 103.800000: 10 casualties and 5 injuries.')
        self.traffic_event.delete()

    def test_agency_message_terrorist(self):
        self.terrorist_event = TerroristEvent.objects.create(
            event=self.event, num_hostiles=20, attack_type='BMB')
        self.assertEqual(
            AgencyDispatcher(self.log).construct_message(), 'New terrorist attack incident at 1.360000, 103.800000: 10 casualties and 5 injuries.')

    def test_agency_subscribers_traffic(self):
        self.traffic_event = TrafficEvent.objects.create(
            event=self.event, num_vehicles=20)
        self.assertEqual(
            AgencyDispatcher(self.log).get_agency_subscribers(), ['+6586691325'])
        self.traffic_event.delete()

    def test_agency_subscribers_terrorist(self):
        self.terrorist_event = TerroristEvent.objects.create(
            event=self.event, num_hostiles=20, attack_type='BMB')
        self.assertEqual(AgencyDispatcher(
            self.log).get_agency_subscribers(), ['+6586691325', '+6586691325'])
        self.terrorist_event.delete()


class SocialDispatcherTest(TestCase):

    def setUp(self):
        self.usr, created = User.objects.get_or_create(
            username='test', password='testpassword', email='test@test.com')
        self.adm = Admin.objects.create(
            user_ptr_id=self.usr.id, name='Test Admin')
        self.crisisLog = CrisisTransactionLog.objects.create(
            new_crisis=4, admin=self.adm, district='Bishan')

    def test_social_dispatcher_message(self):
        self.assertEqual(SocialMediaDispatcher(self.crisisLog).construct_message(
        ), 'Crisis level in Bishan has been changed to Level 4. Please take care.')


class PullAPITest(TestCase):

    def setUp(self):
        pass

    def test_pull_weather(self):
        self.assertTrue(WeatherAPI().pull_PSI_update())
        self.assertTrue(WeatherAPI().pull_weather_update())

    def test_pull_dengue(self):
        self.assertTrue(DengueAPI().pull_update())


class PushAPITest(TestCase):

    def setUp(self):
        pass

    def test_fb_update(self):
        randomizeUpdate = random.randint(1, 10000)
        self.assertTrue(
            FacebookAPI().push_update('System Test %d #ignorethis' %
                                      randomizeUpdate))

    def test_twitter_update(self):
        randomizeUpdate = random.randint(1, 10000)
        self.assertTrue(
            TwitterAPI().push_update('System Test %d #ignorethis' %
                                     randomizeUpdate))

    def test_email_update(self):
        self.assertTrue(EmailAPI().push_update(
            'cz3003cmstest@gmail.com', 'System Test', 'System Test #ignorethis'))

    def test_sms_update(self):
        self.assertTrue(
            TwilioAPI().push_update('System Test #ignorethis', '+6586691325'))


class CrisisCalculatorTest(TestCase):

    def setUp(self):
        pass

    def test_serverity_thresholds(self):  # boundary value testing?
        severity_test_values = [0, 99, 100, 150, 300, 500, 750, 1000]
        true_crisis_levels = [0, 0, 1, 2, 3, 4, 5]
        for tv, av in zip(severity_test_values, true_crisis_levels):
            self.assertEqual(CrisisCalculator().get_crisis_level(tv), av)
        with self.assertRaises(InvalidSeverityException):
            CrisisCalculator().get_crisis_level(-1)
