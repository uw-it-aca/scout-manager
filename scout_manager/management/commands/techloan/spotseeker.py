# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import datetime
import os
import urllib.request as req
from schema import Schema
from urllib.parse import urlencode
from typing import Iterator
from .techloan import Techloan
from .utils import clean_html
from restclients_core.exceptions import DataFailureException
from uw_spotseeker import Spotseeker
from uw_spotseeker.dao import Spotseeker_DAO

logger = logging.getLogger(__name__)


def sync_equipment_to_item(equipment, item):
    if equipment["name"]:
        item["name"] = equipment["name"][:50]

    item["category"] = equipment["_embedded"]["class"]["category"]
    item["subcategory"] = equipment["_embedded"]["class"]["name"]

    if equipment["description"]:
        item["extended_info"]["i_description"] = clean_html(
            equipment["description"][:350])
    item["extended_info"]["i_brand"] = equipment["make"]
    item["extended_info"]["i_model"] = equipment["model"]
    if equipment["manual_url"]:
        item["extended_info"]["i_manual_url"] = equipment["manual_url"]
    if equipment["image_url"]:
        item["extended_info"]["i_image_url"] = equipment["image_url"]

    item["extended_info"]["i_checkout_period"] = equipment["check_out_days"]
    if equipment["stf_funded"]:
        item["extended_info"]["i_is_stf"] = "true"
    else:
        item["extended_info"].pop("i_is_stf", None)
    item["extended_info"]["i_quantity"] = \
        equipment["_embedded"]["availability"][0]["num_available"]

    if equipment["reservable"]:
        item["extended_info"]["i_reservation_required"] = "true"
    else:
        item["extended_info"].pop("i_reservation_required", None)
    item["extended_info"]["i_access_limit_role"] = "true"
    item["extended_info"]["i_access_role_students"] = "true"

    item['extended_info']['i_recent_changes'] = \
        item['extended_info'].get('i_last_modified') != \
        equipment['last_modified']
    # if last_modified is None, set it to now
    item['extended_info']['i_last_modified'] = \
        equipment['last_modified'] or datetime.datetime.now().isoformat()


class Spot(dict):
    _scheme = Schema({
        'id': int,
        'name': str,
        'etag': str,
        'extended_info': {
            'cte_techloan_id': str,
        },
    }, ignore_extra_keys=True)

    def __init__(self, spot):
        self._scheme.validate(spot)

        # Allow the class to be accessed like a dict
        super(Spot, self).__init__(spot)
        self.__dict__ = spot

    def deactive_all_items(self):
        for item in self["items"]:
            item["extended_info"].pop("i_is_active", None)

    def item_with_equipment_id(self, equipment_id):
        for item in self['items']:
            if ('cte_type_id' in item['extended_info'] and
                    int(item['extended_info']['cte_type_id']) == equipment_id):
                return item
        return None

    def raw(self):
        return self.__dict__

    def validate(self) -> bool:
        try:
            self._scheme.validate(self.__dict__)
            return True
        except Exception as ex:
            return False


class Spots:
    _url = '{}/api/v1/spot'
    _filter = {'extended_info:app_type': 'tech',
               'extended_info:has_cte_techloan': 'true',
               'limit': '0'}

    def __init__(self, spots_json_arr, config):
        self._config = config
        self.spots = []
        for spot in spots_json_arr:
            try:
                self.spots.append(Spot(spot))
            except Exception as ex:
                logger.warning("Bad data retrieved from spotseeker " +
                               str(ex) + " from " + json.dumps(spot))

    def __iter__(self) -> Iterator[Spot]:
        return self.spots.__iter__()

    def sync_with_techloan(self, techloan: Techloan):
        logger.info("Sync with techloan")
        for spot in self.spots:
            spot.deactive_all_items()
            equipments = techloan.equipments_for_spot(spot)

            for equipment in equipments:
                item = spot.item_with_equipment_id(equipment['id'])

                if item is None:
                    item = {
                        'name': "%s %s (%d day)" % (
                            equipment['make'],
                            equipment['model'],
                            equipment['check_out_days']
                        ),
                        'category': '',
                        'subcategory': '',
                        'extended_info': {
                            'cte_type_id': equipment["id"],
                        },
                    }
                    item["name"] = item["name"][:50]
                    spot["items"].append(item)

                item["extended_info"]["i_is_active"] = "true"
                sync_equipment_to_item(equipment, item)

    def _get_item_id_by_cte_id(self, items: list, cte_type_id: str) -> int:
        if cte_type_id != 'None':
            for item in items:
                if item['extended_info'].get('cte_type_id') == cte_type_id:
                    return item['id']
        return None

    def _item_image_exists(self, item_id, items: list) -> bool:
        for item in items:
            if item['id'] == item_id:
                return len(item['images']) > 0
        return False

    def _item_has_image(self, item_id, image_url, items: list) -> bool:
        for item in items:
            if item['id'] == item_id and \
                    item['extended_info'].get('i_image_url') == image_url:
                return True
            elif item['id'] == item_id:
                return False
        return False

    def _get_image_id(self, items: list, item_id) -> int:
        for item in items:
            if item['id'] == item_id:
                return item['images'][0]['id']

    def _download_image(self, image_url, cte_type_id) -> str:
        logger.info("Downloading image: " + image_url)

        try:
            opener = req.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            req.install_opener(opener)
            file_name, _ = req.urlretrieve(image_url)
            return file_name
        except Exception as ex:
            logger.warning(f'Failed to download image {image_url}'
                           f' for equipment {cte_type_id}: {str(ex)}')
            return None

    def upload_data(self):
        url = self._url.format(self._config['server_host'])
        item_url = url[:url.rindex('/')] + '/item'
        failures = []

        for spot in self.spots:
            if not spot.validate():
                logger.error(f"Malformed space id : {spot['id']}")
                continue

            logger.info('Updating spot ' + str(spot['id']))

            spot_json = json.dumps(spot.raw())
            try:
                resp, _ = Spotseeker().put_spot(spot['id'], spot_json,
                                                spot['etag'])
            except DataFailureException as ex:
                failures.append({
                    'name': spot['name'],
                    'location': f"PUT {'/api/v1/spot/' + str(spot['id'])}",
                    'reason': resp.status,
                })
                continue

            spotseeker = Spotseeker()
            items_content = spotseeker.get_spot_by_id_json(spot['id'])['items']

            # post item images
            logger.info(f"Uploading images for spot {spot['id']}")
            for item in spot.items:
                item_name = item['name']
                image_url = item['extended_info'].get('i_image_url')
                cte_type_id = item['extended_info'].get('cte_type_id')
                recent_changes = item['extended_info'].get('i_recent_changes')

                item_id = self._get_item_id_by_cte_id(
                    items_content, str(cte_type_id)
                )
                if item_id is None:
                    logger.error(f"Can't find item id for {item_name}")
                    continue

                image_exists = self._item_image_exists(item_id, items_content)
                has_image = image_exists and \
                    self._item_has_image(item_id, image_url, items_content)
                # if same image already exists, skip
                if has_image:
                    continue

                # if different image exists, delete it
                if image_exists:
                    # find image id
                    image_id = self._get_image_id(items_content, item_id)
                    old_image_url = f"{item_url}/{item_id}/image/{image_id}"

                    # delete old image
                    logger.info('Deleting old image ' + old_image_url)

                    spotseeker.delete_item_image(
                        item_id, image_id, spot['etag'])

                image = self._download_image(image_url, cte_type_id) \
                    if image_url and (recent_changes or not image_exists) \
                    else None
                if image is None:
                    continue

                # make url by replacing the 'spot/' with 'item/...'
                full_url = f"{item_url}/{item_id}/image"

                # read image
                with open(image, "rb") as f:
                    image_bytes = f.read()

                # post new image
                logger.info('Uploading image ' + full_url)
                _ = spotseeker.post_item_image(item_id, image_bytes)

        if len(failures) != 0:
            errors = {}

            for failure in failures:
                if isinstance(failure['reason'], list):
                    errors.update({failure['location']: []})
                    for reason in failure['reason']:
                        errors[failure['location']].append(reason)
                else:
                    errors.update({failure['location']: failure['reason']})

            logger.warning(
                f"Errors putting to the server: \n{json.dumps(errors)}")

    @classmethod
    def from_spotseeker_server(cls, config) -> 'Spots':
        logger.info("Get spots from spotseeker_server")

        # search spots with techloan filter
        spots_json = Spotseeker().get_filtered_spots_json(cls._filter)

        return cls(spots_json, config)
