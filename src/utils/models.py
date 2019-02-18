from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User

class Weather(gismodels.Model):
    """
        Caches information pulled from weather API
            - weather condition
    """
    area_name = models.CharField(max_length=128, primary_key=True)
    location = gismodels.PointField()
    condition = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name_plural = 'Weather Objects'

class Haze(gismodels.Model):
    """
        Caches information pulled from weather API
            - haze conditions
    """
    region_name = models.CharField(max_length=128, primary_key=True)
    location = gismodels.PointField()
    psi = models.IntegerField(default=0)
    pm_25 = models.IntegerField(default=0)
    pm_10 = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Haze Objects'


class Dengue(models.Model):

    """
        Caches information pulled from dengue API
            - dengue hotspots
    """
    gid = models.AutoField(primary_key=True)
    # locality = models.CharField(max_length=254, blank=True, null=True)
    # case_size = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    # hyperlink = models.CharField(max_length=254, blank=True, null=True)
    # shape_leng = models.DecimalField(
    #     max_digits=1000, decimal_places=1000, blank=True, null=True)
    # shape_area = models.DecimalField(
    #     max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = gismodels.GeometryField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'cms_dengue'
        verbose_name_plural = 'Dengue Objects'


class Operator(User):
    """
        User with operator priviledges
    """
    name = models.CharField(max_length=256, default='')

    class Meta:
        verbose_name = 'Operator'

class Admin(User):
    """
        User with admin priviledges
    """
    name = models.CharField(max_length=256, default='')

    class Meta:
        verbose_name = 'Admin'

class Reporter(models.Model):
    """
        Stores information related to person reporting incident
    """
    name = models.CharField(max_length=128, default='')
    identification = models.CharField(max_length=10, primary_key=True)
    contact_number = models.CharField(max_length=8, blank=True)

class Event(models.Model):

    """
        Event superclass model. Contains:
            - operators who have created/edited it
            - first person to report
            - other people who have reported this incident
            - is the event active?
            - text description of event
            - number of casualties
            - number of injured people
            - location of event
            - what sort of assistance is required (not used now ....)
    """
    AMBULANCE = 'AMB'
    RESCUE = 'RES'
    EVACUATION = 'EVA'
    ASSISTANCE_CHOICES = (
        (AMBULANCE, 'Ambulance'),
        (RESCUE, 'Rescue'),
        (EVACUATION, 'Evacuation')
    )

    operator = models.ManyToManyField(Operator)
    first_responder = models.ForeignKey(
        Reporter, related_name='first_responder', on_delete=models.CASCADE)
    reporters = models.ManyToManyField(
        Reporter, blank=True, related_name='other_responders')
    isactive = models.BooleanField(default=True)
    description = models.TextField(default='')
    num_casualties = models.IntegerField(default=0)
    num_injured = models.IntegerField(default=0)
    date_recorded = models.DateTimeField(auto_now=True)
    location = gismodels.PointField(blank=True)
    assistance_required = models.CharField(
        max_length=3, choices=ASSISTANCE_CHOICES)

class TrafficEvent(models.Model):
    """
        Traffic event subclass
            - Number of vehicles affected by incident
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_vehicles = models.IntegerField(default=0)

class TerroristEvent(models.Model):
    """
        Terrorist event subclass
            - Number of hostiles
            - Type of terrorist attack
    """
    BOMB = 'BMB'
    BIOCHEMICAL = 'BCH'
    HOSTAGE = 'HST'
    TYPE_CHOICES = (
        (BOMB, 'Bomb'),
        (BIOCHEMICAL, 'Biochemical'),
        (HOSTAGE, 'Hostage')
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_hostiles = models.IntegerField(default=0)
    attack_type = models.CharField(max_length=3, choices=TYPE_CHOICES)

class EventTransactionLog(models.Model):
    """
        Stores transaction log of operations on events.
            - Operator who edited/created event (null if not an operator)
            - Admin who edited/created event (null if not an admin)
            - Description of change
                e.g. UPDATE num_casualties
            - Date of transaction (made to be auto now)
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=2, choices=(('ED', 'Edit'), ('CR', 'Create'), ('DL', 'Delete')))
    operator = models.ForeignKey(Operator, blank=True, null=True, on_delete=models.CASCADE)
    reporter = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, blank=True, null=True, on_delete=models.CASCADE)
    desc = models.CharField(max_length=1024, blank=True)
    date_transaction = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event Transaction Log'
        verbose_name_plural = 'Event Transaction Logs'


class Singapore(models.Model):
    """
        Contains GeoSpatial information on Singapore districts
    """
    gid = models.AutoField(primary_key=True)
    id_0 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    iso = models.CharField(max_length=3, blank=True, null=True)
    name_0 = models.CharField(max_length=75, blank=True, null=True)
    id_1 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    name_1 = models.CharField(max_length=75, blank=True, null=True)
    hasc_1 = models.CharField(max_length=15, blank=True, null=True)
    ccn_1 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    cca_1 = models.CharField(max_length=254, blank=True, null=True)
    type_1 = models.CharField(max_length=50, blank=True, null=True)
    engtype_1 = models.CharField(max_length=50, blank=True, null=True)
    nl_name_1 = models.CharField(max_length=50, blank=True, null=True)
    varname_1 = models.CharField(max_length=150, blank=True, null=True)
    geom = gismodels.GeometryField(blank=True, null=True)

    def __str__(self):
        return self.name_0 + ' ' + self.name_1

    class Meta:
        # managed = False
        db_table = 'cms_singapore'
        verbose_name_plural = 'Singapore Objects'


class District(models.Model):
    """
        Contains crisis level information for the Singapore districts
    """
    district = models.CharField(max_length=10, primary_key=True)
    crisis = models.PositiveSmallIntegerField(default=0)
    center = gismodels.PointField(blank=True, null=True)


class CrisisTransactionLog(models.Model):
    """
        Crisis transaction log which records when the crisis level is raised or decreased by an admin
            - new crisis level
            - admin account that made the change
    """
    new_crisis = models.PositiveSmallIntegerField()
    admin = models.ForeignKey(Admin, blank=True, null=True, on_delete=models.CASCADE)
    district = models.CharField(max_length=10)
    date_recorded = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Crisis Transaction Log'
        verbose_name_plural = 'Crisis Transaction Logs'
