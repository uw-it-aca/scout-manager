"""
Tests for the scout-manager spot DAO
"""
from scout_manager.dao.space import get_spot_hours_by_day, \
    _process_checkbox_array, get_spot_list, _get_spot_id_from_url, \
    _build_spot_json
from spotseeker_restclient.spotseeker import Spotseeker
from scout_manager.test import ScoutTest
import datetime
import json


class SpotDaoTest(ScoutTest):

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

        self.assertIsInstance(_process_checkbox_array(ee_string), list)
        self.assertIsInstance(_process_checkbox_array(ee_list), list)

    def test_get_spot_list(self):
        self.assertEqual(len(get_spot_list(app_type='food')), 3)
        self.assertEqual(len(get_spot_list(app_type='study')), 1)
        self.assertEqual(len(get_spot_list(app_type='nonexistant')), 0)
        self.assertEqual(len(get_spot_list()), 3)

    def test_get_id(self):
        url = "http://spotseeker-test-app1.cac.washington.edu/api/v1/spot/5213"
        self.assertEqual(_get_spot_id_from_url(url), '5213')


class BuildSpotJsonTest(ScoutTest):
    '''Unit tests for the _build_spot_json function'''

    def test_simple_json(self):
        '''Bare minimum plus handling of generic (not special case) keys'''
        # Foo should remain untouched, while type is required
        json_data = {'foo': 'bar', 'type': 'baz'}
        out = _build_spot_json(wrap_json(json_data))
        expected = {
            'type': ['baz'],
            'foo': 'bar',
            'extended_info': {},
            'location': {}
        }
        self.assertEqual(out, expected)

    def test_extended_foods_json(self):
        '''Test extended info handling'''
        cuisines = ['one', 'two']
        json_data = {
            'extended_info:s_cuisine': cuisines,
            'type': 'foo'
        }
        out = _build_spot_json(wrap_json(json_data))
        # Cuisines should not be in their own keys in the EI rather than
        # being inside of the ei:s_cuisine key
        ei = out['extended_info']
        for cuisine in cuisines:
            self.assertEqual(ei[cuisine], 'true')


def wrap_json(jsdata):
    '''Prepare json for use in _build_spot_json'''
    return {'json': json.dumps(jsdata)}
