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
        return spot

def sort_hours_by_day(spot):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    hours_objects = []
    for day in days:
        day_hours = \
            [hours for hours in spot.spot_availability if hours.day == day]
        hours_objects.append({"day": day,
                              "hours": day_hours
                              })
    spot.grouped_hours = hours_objects
    return spot


