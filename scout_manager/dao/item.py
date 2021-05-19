# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_spotseeker.dao import Spotseeker_DAO
from uw_spotseeker import Spotseeker
from restclients_core.exceptions import DataFailureException
from scout_manager.dao.space import process_extended_info
import json


def delete_item(item_id, spot_id):
    spot_client = Spotseeker()
    json_data = _get_spot_json(spot_id)
    etag = json_data["etag"]
    for item in json_data["items"]:
        if item["id"] == int(item_id):
            json_data["items"].remove(item)
    spot_client.put_spot(spot_id, json.dumps(json_data), etag)


def get_item_by_id(item_id):
    from scout.dao.item import add_item_info

    spot_client = Spotseeker()
    spot = None
    try:
        spots = spot_client.search_spots(
            [
                ("item:id", item_id),
                ("extended_info:app_type", "tech"),
            ]
        )
        if spots:
            spot = process_extended_info(spots[0])
            spot = add_item_info(spot)
            spot = _filter_spot_items(item_id, spot)
    except DataFailureException:
        pass
        # TODO: consider logging on failure

    return spot


def _filter_spot_items(item_id, spot):
    for item in spot.items:
        if item.item_id == item_id:
            spot.item = item
    return spot


def create_item(form_data):
    req_data = json.loads(form_data["json"])
    if isinstance(req_data, list):
        spot_id = req_data[0]["spot_id"]
        spot_client = Spotseeker()
        spot_data = _get_spot_json(spot_id)
        etag = req_data[0]["etag"]
        for item in req_data:
            item_json = _build_item_json({"json": json.dumps(item)})
            item_json.pop("id")
            item_json.pop("spot_id")
            spot_data["items"].append(item_json)
        spot_client.put_spot(spot_id, json.dumps(spot_data), etag)
    else:
        item_json = _build_item_json(form_data)
        try:
            # TODO: figure out if this is even needed any longer.
            spot_id = item_json.pop("new_spot_id")
        except KeyError:
            spot_id = item_json["spot_id"]
        item_json.pop("id")
        item_json.pop("spot_id")

        spot_client = Spotseeker()
        json_data = _get_spot_json(spot_id)
        etag = json_data["etag"]
        json_data["items"].append(item_json)
        spot_client.put_spot(spot_id, json.dumps(json_data), etag)


def _get_spot_json(spot_id):
    url = "/api/v1/spot/%s" % spot_id
    dao = Spotseeker_DAO()
    resp = dao.getURL(url, {})

    if resp.status != 200:
        raise DataFailureException(url, resp.status, resp.data)
    return json.loads(resp.data)


def update_item(form_data, item_id, image=None):
    item_json = _build_item_json(form_data)
    spot_id = item_json.pop("spot_id")
    # new_spot_id = item_json.pop('new_spot_id')

    # Can we make item move work while preserving item id?
    # if not new_spot_id == spot_id:
    #     delete_item(item_id, spot_id)
    #     create_item(form_data)
    #     return

    spot_client = Spotseeker()
    json_data = _get_spot_json(spot_id)
    etag = json_data["etag"]
    for i, item in enumerate(json_data["items"]):
        if item["id"] == int(item_id):
            json_data["items"][i] = item_json
    spot_client.put_spot(spot_id, json.dumps(json_data), etag)

    if "removed_images" in item_json:
        for image in item_json["removed_images"]:
            spot_client.delete_item_image(item_id, image["id"], image["etag"])

    if form_data["file"] is not None and form_data["file"] != "undefined":
        spot_client.post_item_image(item_id, form_data["file"])


def _build_item_json(form_data):
    json_data = json.loads(form_data["json"])

    if len(json_data["id"]):
        json_data["id"] = int(json_data["id"])

    extended_info = {}

    for key in list(json_data):
        if key.startswith("extended_info"):
            value = json_data[key]
            name = key.split(":", 1)[1]
            json_data.pop(key)
            if value != "None" and len(value) > 0:
                extended_info[name] = value

    json_data["extended_info"] = extended_info
    return json_data


"""
Core data
"""
# item.name
# item.category
# item.subcategory

"""
Core data... space location id
"""
# location/related space ?

"""
Images
"""
# photo/image model?

"""
Extended info... item information
"""
# i_is_active
# i_is_stf

# i_description
# i_quantity
# i_model
# i_brand
# i_website
# i_manual_url

"""
Extended info... checkout and reservation
"""
# i_checkout_period
# i_reserve_url
# i_reservation_notes

"""
Extended info... access restrictions (deprecated)
"""
# i_has_access_restriction ("true")
# i_access_notes

# i_access_limit_uwnetid ("true")
# i_access_limit_role ("true")
# i_access_limit_school ("true")
# i_access_limit_department ("true")

# i_access_role_students ("true")
# i_access_role_staff ("true")
# i_access_role_faculty ("true")

"""
Extended info... admin information
"""
# i_owner (group)
