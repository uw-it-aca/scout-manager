# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Tests for the scout-manager buildings DAO
"""
from django.test import TestCase
import scout_manager.dao.buildings
from scout_manager.dao.buildings import get_building_list,\
    get_building_list_by_campus


TEST_BUILDING_LIST = {
    'Sea Building': {
        'campus': 'seattle'
    },
    'Tac Building': {
        'campus': 'tacoma'
    },
    'Bot Building': {
        'campus': 'bothell'
    }
}
# override building list for testing purposes
scout_manager.dao.buildings.BUILDING_LIST = TEST_BUILDING_LIST


class BuildingDaoTest(TestCase):
    def test_get_all_buildings(self):
        buildings = get_building_list()
        self.assertEqual(len(buildings), 3)
        self.assertEqual(buildings, {'Tac Building': 'tacoma', 'Sea Building': 'seattle', 'Bot Building': 'bothell'})

    def test_get_by_campus(self):
        self.assertEqual(len(get_building_list_by_campus('tacoma')), 1)
        self.assertEqual((get_building_list_by_campus('tacoma')),
                         {'Tac Building': 'tacoma'})
        self.assertEqual(len(get_building_list_by_campus('not a campus')), 0)
