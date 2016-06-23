"""
Tests for the scout-manager spot DAO
"""
from django.test import TestCase
from django.test.utils import override_settings
from scout_manager.dao.space import get_spot_hours_by_day, _process_checkbox_array
from spotseeker_restclient.spotseeker import Spotseeker
import datetime

DAO = "spotseeker_restclient.dao_implementation.spotseeker.File"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class SpotDaoTest(TestCase):

    def test_make_hours_no_spot(self):
        spot_hours = get_spot_hours_by_day(None)
        self.assertEqual(len(spot_hours), 7)
        self.assertIsNone(spot_hours[0]['hours'])
        self.assertEqual(spot_hours[0]['day'], "monday")

    def test_make_hours_with_spot(self):
        sc = Spotseeker()
        spot = sc.get_spot_by_id(1)

        spot_hours = get_spot_hours_by_day(spot)
        self.assertEqual(len(spot_hours), 7)

        monday_hours = spot_hours[0]['hours']
        self.assertEqual(len(monday_hours), 2)

        monday_start = datetime.time(hour=10, minute=30, second=00)
        monday_end = datetime.time(hour=14, minute=30, second=00)
        self.assertEqual(monday_hours[0].start_time, monday_start)
        self.assertEqual(monday_hours[0].end_time, monday_end)

    def test_process_checkbox(self):
        ee_string = 's_cuisine_indian'
        ee_list = ['s_cuisine_indian', 's_cuisine_asian']

        self.assertEqual(type(_process_checkbox_array(ee_string)), list)
        self.assertEqual(type(_process_checkbox_array(ee_list)), list)
