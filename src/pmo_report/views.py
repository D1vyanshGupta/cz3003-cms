"""
    Module to generate the report to send to the PMO
"""
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from utils.models import TrafficEvent, TerroristEvent, District
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


def get_traffic_info(request):
    """
        Get traffic information from the database
    """
    traffic_events = TrafficEvent.objects.all()
    response = {}
    num_vehicles = 0
    num_casualties = 0
    num_injuries = 0
    for traffic_event in traffic_events:
        event = traffic_event.event
        num_vehicles += traffic_event.num_vehicles
        num_casualties += event.num_casualties
        num_injuries += event.num_injured
    response['numTraffics'] = len(traffic_events)
    response['numVehicles'] = num_vehicles
    response['numCasualties'] = num_casualties
    response['numInjuries'] = num_injuries

    return JsonResponse(response, safe=False)


def get_terrorist_info(request):
    """
        Get terrorist information from the database
    """
    terrorist_events = TerroristEvent.objects.all()
    response = {}
    num_hostiles = 0
    num_casualties = 0
    num_injuries = 0
    attack_types = ""
    for terrorist_event in terrorist_events:
        event = terrorist_event.event
        num_hostiles += terrorist_event.num_hostiles
        num_casualties += event.num_casualties
        num_injuries += event.num_injured
        attack_types += terrorist_event.attack_type +','

    response['numAttacks'] = len(terrorist_events)
    response['numHostiles'] = num_hostiles
    response['numCasualties'] = num_casualties
    response['numInjuries'] = num_injuries
    response['attackTypes'] = attack_types

    return JsonResponse(response, safe=False)

def get_crisis_info(request):
    """
        Get the crisis information for each region
    """
    districts = Districts.objects.all()
    response = {}
    for d in districts:
        response[d.district] = d.crisis
    return JsonResponse(response, safe=False)


def get_map_image(request):
    """
        Get the image of Google Map
    """
    try:
        print('capturing screenshots')
        browser = webdriver.Firefox()
        browser.get('http://localhost:8000/maps/crisis')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot('cms/static/img/crisis_screenshot.png')
        browser.get('http://localhost:8000/maps/traffic')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot('cms/static/img/traffic_screenshot.png')
        browser.get('http://localhost:8000/maps/terrorist')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot('cms/static/img/terrorist_screenshot.png')
        browser.get('http://localhost:8000/maps/weather')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot('cms/static/img/weather_screenshot.png')
        browser.get('http://localhost:8000/maps/dengue')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot('cms/static/img/dengue_screenshot.png')
        browser.quit()
    finally:
        return HttpResponse('done')
