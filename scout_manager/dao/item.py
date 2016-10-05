from spotseeker_restclient.spotseeker import Spotseeker
from spotseeker_restclient.exceptions import DataFailureException
from scout_manager.dao.space import process_extended_info


def get_item_by_id(item_id):
    from scout.dao.item import add_item_info

    spot_client = Spotseeker()
    spot = None
    try:
        spots = spot_client.search_spots([
            ('item:id', item_id),
            ('extended_info:app_type', 'tech'),
        ])
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
