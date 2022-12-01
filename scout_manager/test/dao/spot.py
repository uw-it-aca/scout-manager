# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Tests for the scout-manager spot DAO
"""
from django.http import HttpResponse

from scout_manager.dao.space import (
    create_spot,
    get_spot_by_id,
    get_spot_hours_by_day,
    _process_checkbox_array,
    get_spot_list,
    _get_spot_id_from_url,
    _build_spot_json,
    update_spot,
)
from scout_manager.views.api import Spot
from uw_spotseeker import Spotseeker
from scout_manager.test import ScoutTest
from django.test.utils import override_settings
import datetime
import json
from mock import patch
from restclients_core.exceptions import DataFailureException

DAO = "Mock"


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class SpotDaoTest(ScoutTest):
    def test_make_hours_no_spot(self):
        spot_hours = get_spot_hours_by_day(None)
        self.assertEqual(len(spot_hours), 7)
        self.assertIsNone(spot_hours[0]["hours"])
        self.assertEqual(spot_hours[0]["day"], "monday")

    def test_make_hours_with_spot(self):
        sc = Spotseeker()
        spot = sc.get_spot_by_id(1)

        spot_hours = get_spot_hours_by_day(spot)
        self.assertEqual(len(spot_hours), 7)

        monday_hours = spot_hours[0]["hours"]
        self.assertEqual(len(monday_hours), 2)

        monday_start = datetime.time(hour=10, minute=30, second=00)
        monday_end = datetime.time(hour=14, minute=30, second=00)
        self.assertEqual(monday_hours[0].start_time, monday_start)
        self.assertEqual(monday_hours[0].end_time, monday_end)

    def test_process_checkbox(self):
        ee_string = "s_cuisine_indian"
        ee_list = ["s_cuisine_indian", "s_cuisine_asian"]

        self.assertIsInstance(_process_checkbox_array(ee_string), list)
        self.assertIsInstance(_process_checkbox_array(ee_list), list)

    def test_get_spot_list(self):
        self.assertEqual(len(get_spot_list(app_type="food")), 3)
        self.assertEqual(len(get_spot_list(app_type="study")), 1)
        self.assertEqual(len(get_spot_list(app_type="nonexistant")), 0)
        self.assertEqual(len(get_spot_list()), 3)

    def test_get_id(self):
        url = "http://spotseeker-test-app1.cac.washington.edu/api/v1/spot/5213"
        self.assertEqual(_get_spot_id_from_url(url), "5213")

    # TODO: find a way to get put_spot to be called
    def test_create_spot(self):
        form_data = {
            "json": '{"name": "Test Spot", "capacity": 19,\
                 "location:latitude": 50, "location:longitude": -30,\
                      "extended_info:app_type": "tech"}',
            "file": None,
        }
        try:
            create_spot(form_data)
        except DataFailureException as e:
            self.assertTrue("Error fetching /api/v1/spot." in str(e))

    def test_update_spot(self):
        form_data = {"file": None, "json": '{"capacity": "19"}'}
        json_data = _build_spot_json(form_data)
        with patch.object(Spotseeker, "put_spot") as mock_put:
            # this doesn't actually change the capacity to 19 but calls put_spot
            update_spot(form_data, "1")
            etag = get_spot_by_id(1).etag
            mock_put.assert_called_once_with("1", json.dumps(json_data), etag)

    @patch("scout_manager.test.dao.spot.update_spot")
    def test_error_messages(self, mock_update):
        form_data = {
            "file": None,
            "json": '{"extended_info:location_description": "12345"}',
        }
        mock_update.side_effect = DataFailureException(
            "/api/v1/spot/1", 400, b'{"__all__": ["Error message tested"]}'
        )

        def error_msg_helper(spot_id):
            try:
                update_spot(form_data, spot_id)
            except Exception as ex:
                ex.msg = json.loads(ex.msg.decode("utf-8"))
                print(type(ex.msg))
                ex.msg = ex.msg.get("__all__", "Form is invalid")
                print(type(ex.msg))
                ex.msg = " ".join(ex.msg)
                print(type(ex.msg))
                return HttpResponse(
                    str(ex.msg), status=400, content_type="application/json"
                )
            return HttpResponse(
                json.dumps({"status": "it works"}),
                content_type="application/json",
            )

        with patch.object(
            Spot, "PUT", wraps=mock_update, side_effect=error_msg_helper
        ) as mock_put:
            ret = mock_put("1")
            self.assertEqual(ret.status_code, 400)
            self.assertEqual(
                ret.content.decode("utf-8"), str("Error message tested")
            )


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class BuildSpotJsonTest(ScoutTest):
    """Unit tests for the _build_spot_json function"""

    def test_simple_json(self):
        """Bare minimum plus handling of generic (not special case) keys"""
        # Foo should remain untouched, while type is required
        json_data = {"foo": "bar", "type": "baz"}
        out = _build_spot_json(wrap_json(json_data))
        expected = {
            "type": ["baz"],
            "foo": "bar",
            "extended_info": {},
            "location": {},
        }
        self.assertEqual(out, expected)

    def test_extended_info_json(self):
        """
        Test that _build_spot_json correctly handles parameters specified
        as both a list or single item
        """
        cuisines = ["s_cuisine_one", "s_cuisine_two"]
        foods = ["s_food_tofu", "s_food_pizza"]
        payment = "s_pay_cash"
        json_data = {
            "extended_info:s_cuisine": cuisines,
            "extended_info:s_food": foods,
            "extended_info:s_pay": payment,
            "extended_info:test": "bar",
            "type": "foo",
        }
        out = _build_spot_json(wrap_json(json_data))
        # Cuisine/food/payment types should end up in their own keys
        # rather than a list
        expected = {
            "type": ["foo"],
            "extended_info": {
                "s_cuisine_one": "true",
                "s_cuisine_two": "true",
                "s_food_tofu": "true",
                "s_food_pizza": "true",
                "s_pay_cash": "true",
                "test": "bar",
            },
            "location": {},
        }
        self.assertEqual(out, expected)

    def test_extended_info_json_labstats_5(self):
        """
        Test that _build_spot_json correctly handles labstats 5 information
        """
        labstats = "has_labstats"
        labstats_id = "47"
        json_data = {
            "labstats": labstats,
            "extended_info:labstats_id": labstats_id,
        }
        out = _build_spot_json(wrap_json(json_data))
        # Cuisine/food/payment types should end up in their own keys
        # rather than a list
        expected = {
            "extended_info": {"has_labstats": "true", "labstats_id": "47"},
            "location": {},
        }
        self.assertEqual(out, expected)

    def test_extended_info_json_labstats_cloud(self):
        """
        Test that _build_spot_json correctly handles labstats cloud information
        """

        labstats = "has_online_labstats"
        labstats_customer_id = "17aa57b6-0528-11e8-ba89-0ed5f89f718b"
        labstats_label = "example_label"
        labstats_page_id = "47"
        json_data = {
            "labstats": labstats,
            "extended_info:labstats_customer_id": labstats_customer_id,
            "extended_info:labstats_label": labstats_label,
            "extended_info:labstats_page_id": labstats_page_id,
        }
        out = _build_spot_json(wrap_json(json_data))
        # Cuisine/food/payment types should end up in their own keys
        # rather than a list
        expected = {
            "extended_info": {
                "has_online_labstats": "true",
                "labstats_customer_id": labstats_customer_id,
                "labstats_label": labstats_label,
                "labstats_page_id": labstats_page_id,
            },
            "location": {},
        }
        self.assertEqual(out, expected)

    def test_location_json(self):
        """Test location parsing"""
        json_data = {
            "location:longitude": "24",
            "location:latitude": "34",
            "location:other": "67",
            "type": "foo",
        }
        out = _build_spot_json(wrap_json(json_data))
        expected = {
            "type": ["foo"],
            "extended_info": {},
            "location": {"longitude": "24", "latitude": "34", "other": "67"},
        }
        self.assertEqual(out, expected)

    def test_no_type(self):
        json_data = {
            "extended_info:test": "bar",
        }
        try:
            _build_spot_json(wrap_json(json_data))
        except KeyError:
            self.fail("_build_spot_json raised a KeyError with no type set")


def wrap_json(jsdata):
    """Prepare json for use in _build_spot_json"""
    return {"json": json.dumps(jsdata)}
