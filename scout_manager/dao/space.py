from spotseeker_restclient.spotseeker import Spotseeker
from spotseeker_restclient.exceptions import DataFailureException
from scout.dao.space import add_cuisine_names, add_foodtype_names_to_spot, \
    add_payment_names, add_additional_info

def get_spot_by_id(spot_id):
        spot_client = Spotseeker()
        res = spot_client.get_spot_by_id(spot_id)
        return process_extended_info(res)

def process_extended_info(spot):
        spot = add_foodtype_names_to_spot(spot)
        spot = add_cuisine_names(spot)
        spot = add_payment_names(spot)
        spot = add_additional_info(spot)
        spot = sort_hours_by_day(spot)
        for item in spot.extended_info:
            if item.key == "owner":
                spot.owner = item.value
        return spot

def sort_hours_by_day(spot):
    days = ["monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday"]
    hours_objects = []
    for day in days:
        day_hours = \
            [hours for hours in spot.spot_availability if hours.day == day]
        hours_objects.append({"day": day,
                              "hours": day_hours
                              })
    spot.grouped_hours = hours_objects
    return spot


def update_spot(data):
    # handles case where single box is checked doesn't return a list
    if isinstance(data["type"], unicode):
        data["type"] = [data["type"]]
    # formats extended info
    extended_info = {}

    cuisines = data.pop("extended_info:s_cuisine", [])
    for cuisine in cuisines:
        extended_info[cuisine] = True

    foods = data.pop("extended_info:s_food", [])
    for food in foods:
        extended_info[food] = True

    payments = data.pop("extended_info:s_pay", [])
    for payment in payments:
        extended_info[payment] = True

    for key in list(data):
        if "extended_info" in key:
            value = data[key]
            name = key.split(":")[1]
            data.pop(key)
            if value != "None" and len(value) > 0:
                if value == "true":
                    extended_info[name] = True
                else:
                    extended_info[name] = value


    # formats location data
    location_data = {}
    for key in list(data):
        if "location" in key:
            name = key.split(":")[1]
            location_data[name] = data[key]
            data.pop(key)


    data["extended_info"] = extended_info
    data["location"] = location_data


