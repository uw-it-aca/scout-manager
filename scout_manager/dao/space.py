from spotseeker_restclient.spotseeker import Spotseeker
from spotseeker_restclient.exceptions import DataFailureException
from scout.dao.space import add_cuisine_names, add_foodtype_names_to_spot, \
    add_payment_names, add_additional_info, add_study_info
import json
import re


def get_spot_list(app_type=None, groups=[]):
    spot_client = Spotseeker()
    res = []
    filters = []
    filters.append(('limit', 0))
    try:
        if app_type:
            filters.append(('extended_info:app_type', app_type))
        for group in groups:
            filters.append(('extended_info:group', group))
        spots = spot_client.search_spots(filters)
        for spot in spots:
            spot = process_extended_info(spot)
            if spot is not None:
                res.append(spot)
    except DataFailureException:
        # TODO: consider logging on failure
        pass

    return res


def get_spot_by_id(spot_id):
    spot_client = Spotseeker()
    res = spot_client.get_spot_by_id(spot_id)
    return process_extended_info(res)


def process_extended_info(spot):
    spot = add_foodtype_names_to_spot(spot)
    spot = add_cuisine_names(spot)
    spot = add_payment_names(spot)
    spot = add_additional_info(spot)
    spot = add_study_info(spot)
    spot.grouped_hours = get_spot_hours_by_day(spot)
    for item in spot.extended_info:
        if item.key == "owner":
            spot.owner = item.value
        if item.key == "app_type":
            spot.app_type = item.value
        if item.key == "is_hidden":
            spot.is_hidden = item.value
    return spot


def get_spot_hours_by_day(spot):
    days = ["monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday"]
    hours_objects = []
    for day in days:
        try:
            day_hours = \
                [hours for hours in spot.spot_availability if hours.day == day]
        except AttributeError:
            day_hours = None
        hours_objects.append({"day": day,
                              "hours": day_hours
                              })
    return hours_objects


def create_spot(form_data):
    json_data = _build_spot_json(form_data)
    spot_client = Spotseeker()
    resp = spot_client.post_spot(json.dumps(json_data))
    spot_id = _get_spot_id_from_url(resp['location'])

    if form_data['file'] is not None and form_data['file'] != "undefined":
        spot_client.post_image(spot_id, form_data['file'])


def _get_spot_id_from_url(spot_url):
    match = re.match('.*?([0-9]+)$', spot_url)
    return match.group(1)


def update_spot(form_data, spot_id, image=None):
    json_data = _build_spot_json(form_data)
    spot_client = Spotseeker()
    # this is really hacky, but the etag seems to keep getting reset
    # between a GET and PUT
    spot = get_spot_by_id(spot_id)
    etag = spot.etag
    spot_client.put_spot(spot_id, json.dumps(json_data), etag)

    if 'removed_images' in json_data:
        for image in json_data['removed_images']:
            spot_client.delete_image(spot_id, image['id'], image['etag'])

    if form_data['file'] is not None and form_data['file'] != "undefined":
        spot_client.post_image(spot_id, form_data['file'])


def _build_spot_json(form_data):
    json_data = json.loads(form_data['json'])

    # handles case where single box is checked doesn't return a list
    if isinstance(json_data["type"], basestring):
        json_data["type"] = [json_data["type"]]
    # formats extended info
    extended_info = {}

    cuisines = json_data.pop("extended_info:s_cuisine", [])
    cuisines = _process_checkbox_array(cuisines)
    for cuisine in cuisines:
        extended_info[cuisine] = True

    foods = json_data.pop("extended_info:s_food", [])
    foods = _process_checkbox_array(foods)
    for food in foods:
        extended_info[food] = True

    payments = json_data.pop("extended_info:s_pay", [])
    payments = _process_checkbox_array(payments)
    for payment in payments:
        extended_info[payment] = True

    for key in list(json_data):
        if "extended_info" in key:
            value = json_data[key]
            name = key.split(":")[1]
            json_data.pop(key)
            if value != "None" and len(value) > 0:
                if value == "true":
                    extended_info[name] = True
                if value == "on":
                    # if a checkbox is checked, set to true
                    extended_info[name] = True
                else:
                    extended_info[name] = value

    # formats location data
    location_data = {}
    for key in list(json_data):
        if "location" in key:
            name = key.split(":")[1]
            location_data[name] = json_data[key]
            json_data.pop(key)

    try:
        phone = json_data.pop("phone")
        extended_info["s_phone"] = phone
    except KeyError:
        pass

    json_data["extended_info"] = extended_info
    json_data["location"] = location_data
    return json_data


def _process_checkbox_array(data):
    if isinstance(data, list):
        return data
    else:
        return [data]
