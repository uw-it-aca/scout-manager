# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from io import StringIO
from urllib.parse import urlencode
from django.test import override_settings
from django.core.management import call_command
from scout_manager.management.commands.\
    sync_techloan import Command
from scout_manager.management.commands.\
    techloan.spotseeker import Spots
from scout_manager.management.commands.\
    techloan.techloan import Techloan
from scout_manager.test.techloan import TechloanTestCase
from mock import patch
import os
import copy
import json
import logging
import responses

test_logger = logging.getLogger(__name__)

good_techloan_updater = {
    'server_host': 'https://techloan.uw.edu',
    'oauth_credential': 'dummy',
    'oauth_scope': 'dummy',
    'oauth_user': 'javerage',
}

bad_techloan_updater = good_techloan_updater.copy()
bad_techloan_updater.update({'server_host': 0})

filter = Spots._filter


def remove_images(spots: list) -> list:
    spots_copy = copy.deepcopy(spots)
    for spot in spots_copy:
        for item in spot['items']:
            item['images'] = []
    return spots_copy


def remove_item_extended_info(spots: list, key: str,
                              replacement=None) -> list:
    spots_copy = copy.deepcopy(spots)
    for spot in spots_copy:
        for item in spot['items']:
            if replacement:
                item['extended_info'][key] = replacement
            else:
                item['extended_info'].pop(key)
    return spots_copy


def call_sync(*args, **kwargs):
    out = StringIO()
    err = StringIO()
    call_command(
        'sync_techloan',
        *args,
        stdout=out,
        stderr=err,
        **kwargs,
    )
    return {'out': out.getvalue(), 'err': err.getvalue()}


@override_settings(RESTCLIENTS_SPOTSEEKER_HOST='http://api.techloan.test')
class SyncTechloanTest(TechloanTestCase):
    """
    Tests to make sure that the sync_techloan management command
    works as expected.
    """

    def setUp(self):
        self.equipments = [
            {
                'id': 54321,
                'name': 'Test Equip',
                'description': None,
                'equipment_location_id': 12345,
                'make': 'Test Make',
                'model': 'Test Model',
                'manual_url': None,
                'image_url': 'www.google.com',
                'last_modified': '2021-12-13T11:22:10.717000',
                'check_out_days': 5,
                'stf_funded': False,
                'num_active': 0,
                'reservable': True,
                '_embedded': {
                    'class': {
                        'name': 'Test Class',
                        'category': 'Test Category',
                    },
                    'availability': [{
                        'num_available': 0,
                    }],
                },
            },
            {
                'id': 98765,
                'name': 'Another Equip',
                'description': 'Hi',
                'equipment_location_id': 00000,
                'make': 'Test Make',
                'model': 'Test Model',
                'manual_url': None,
                'image_url': 'www.bing.com',
                'last_modified': '2021-12-13T11:22:10.717000',
                'check_out_days': 50,
                'stf_funded': True,
                'num_active': 40,
                'reservable': False,
                '_embedded': {
                    'class': {
                        'name': 'Test Class',
                        'category': 'Testing Category',
                    },
                    'availability': [{
                        'num_available': 19,
                    }],
                },
            },
        ]

        self.equip_with_img = copy.deepcopy(self.equipments)
        for equip in self.equip_with_img:
            equip['image_url'] = 'http://placehold.jp/150x150.png'

        with open(os.path.join(
                'scout_manager/resources/spotseeker/file/api/v1',
                f'spot?{urlencode(filter)}'), 'r') as f:
            self.mock_spots = json.load(f)

        self.mock_spots2 = copy.deepcopy(self.mock_spots)
        self.mock_spots_no_imgs = remove_images(self.mock_spots)
        self.mock_spots_bad_cte_ids = remove_item_extended_info(
            self.mock_spots, 'cte_type_id', replacement='-1230123'
        )

    @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=bad_techloan_updater)
    def test_bad_techloan_updater(self):
        # assert a logger error is raised
        with self.assertLogs(level='ERROR') as cm:
            # add test info log so test doesn't fail if no logs
            test_logger.info('Starting full sync...')
            call_sync()
            self.assertIn('Settings misconfigured', cm.output[0])

    @responses.activate
    def test_get_techloan_with_requests(self):
        responses.add(
            responses.GET,
            'http://techloan.test/api/v1/equipment',
            status=200,
            body=json.dumps(self.equipments),
        )

        # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
        with patch('scout_manager.management.commands.techloan.techloan'
                   '.Techloan._url', 'http://techloan.test/api/v1/equipment'):
            techloan = Command().get_techloan()
        self.assertIsInstance(techloan, Techloan)
        self.assertEquals(techloan.equipments, self.equipments)

    @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=bad_techloan_updater)
    # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    @patch('scout_manager.management.commands.techloan.spotseeker'
           '.Spots._url', 'http://techloan.test/api/v1/spot')
    def test_get_spots_with_requests(self):
        spots = Command().get_spots()
        self.assertIsInstance(spots, Spots)
        self.assertEquals(len(spots.spots), 2)

        # assert that each spot has a cte_techloan_id in extended_info
        for spot in spots:
            self.assertIn('cte_techloan_id', spot['extended_info'])

    def get_spot_by_id(self, spot_id, spots):
        return [spot for spot in spots if spot['id'] == spot_id][0]

    def get_spot_ids(self, spots):
        return [spot['id'] for spot in spots]

    def get_item_ids(self, spots, spot_ids=None):
        if spot_ids is None:
            return [item['id'] for spot in spots for item in spot['items']]
        else:
            return [item['id'] for spot in spots for item in spot['items']
                    if spot['id'] in spot_ids]

    def get_image_ids(self, spots, item_id):
        return [image['id'] for spot in spots for item in spot['items']
                if (item['id'] == item_id) for image in item['images']]

    @responses.activate
    @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    @patch('scout_manager.management.commands.techloan.techloan'
           '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    @patch('scout_manager.management.commands.techloan.spotseeker'
           '.Spots._url', 'http://techloan.test/api/v1/spot')
    def test_full_sync_techloan_no_imgs(self):

        responses.add(
            responses.GET,
            'http://techloan.test/api/v1/equipment',
            status=200,
            body=json.dumps(self.equipments),
        )

        # assert no errors logged
        with self.assertLogs() as cm:
            # add test info log so test doesn't fail if no logs
            test_logger.info('Starting full sync...')
            call_sync()
            for out in cm.output:
                self.assertNotIn('ERROR', out)

    # @responses.activate
    # @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    # @patch('scout_manager.management.commands.techloan.techloan'
    #        '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    # @patch('scout_manager.management.commands.techloan.spotseeker'
    #        '.Spots._url', 'http://techloan.test/api/v1/spot')
    # def test_sync_add_imgs(self):
    #     responses.add(
    #         responses.GET,
    #         'http://techloan.test/api/v1/equipment',
    #         status=200,
    #         body=json.dumps(self.equip_with_img),
    #     )

    #     responses.add(
    #         responses.GET,
    #         f'http://techloan.test/api/v1/spot/?{urlencode(filter)}',
    #         status=200,
    #         body=json.dumps(self.mock_spots_no_imgs),
    #     )

    #     for id in self.get_spot_ids(self.mock_spots_no_imgs):
    #         responses.add(
    #             responses.PUT,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps('OK'),
    #         )

    #         responses.add(
    #             responses.GET,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps(
    #                 self.get_spot_by_id(id, self.mock_spots_no_imgs)
    #             ),
    #         )

    #         for item_id in self.get_item_ids(self.mock_spots_no_imgs,
    #                                          spot_ids=[id]):
    #             responses.add(
    #                 responses.POST,
    #                 f'http://techloan.test/api/v1/item/{item_id}/image',
    #                 status=201,
    #                 body=json.dumps('OK'),
    #             )

    #     # assert no errors logged
    #     with self.assertLogs() as cm:
    #         # add test info log so test doesn't fail if no logs
    #         test_logger.info('Starting full sync...')
    #         call_sync()
    #         for out in cm.output:
    #             self.assertNotIn('Failed to retrieve image', out)
    #             self.assertNotIn('ERROR', out)

    @responses.activate
    @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    @patch('scout_manager.management.commands.techloan.techloan'
           '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    @patch('scout_manager.management.commands.techloan.spotseeker'
           '.Spots._url', 'http://techloan.test/api/v1/spot')
    def test_sync_replace_imgs(self):
        responses.add(
            responses.GET,
            'http://techloan.test/api/v1/equipment',
            status=200,
            body=json.dumps(self.equip_with_img),
        )

        # assert no errors logged
        with self.assertLogs() as cm:
            # add test info log so test doesn't fail if no logs
            test_logger.info('Starting full sync...')
            call_sync()
            for out in cm.output:
                self.assertNotIn('ERROR', out)

    # @responses.activate
    # @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    # @patch('scout_manager.management.commands.techloan.techloan'
    #        '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    # @patch('scout_manager.management.commands.techloan.spotseeker'
    #        '.Spots._url', 'http://techloan.test/api/v1/spot')
    # def test_sync_bad_cte_id(self):
    #     responses.add(
    #         responses.GET,
    #         'http://techloan.test/api/v1/equipment',
    #         status=200,
    #         body=json.dumps(self.equip_with_img),
    #     )

    #     responses.add(
    #         responses.GET,
    #         f'http://techloan.test/api/v1/spot/?{urlencode(filter)}',
    #         status=200,
    #         body=json.dumps(self.mock_spots_bad_cte_ids),
    #     )

    #     for id in self.get_spot_ids(self.mock_spots_bad_cte_ids):
    #         responses.add(
    #             responses.PUT,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps('OK'),
    #         )

    #         responses.add(
    #             responses.GET,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps(
    #                 self.get_spot_by_id(id, self.mock_spots_bad_cte_ids)
    #             ),
    #         )

    #         for item_id in self.get_item_ids(self.mock_spots, spot_ids=[id]):
    #             for image_id in self.get_image_ids(self.mock_spots, item_id):
    #                 responses.add(
    #                     responses.DELETE,
    #                     'http://techloan.test/api/v1/item/'
    #                     f'{item_id}/image/{image_id}',
    #                     status=200,
    #                     body=json.dumps('OK'),
    #                 )

    #     # assert errors for bad cte logged
    #     with self.assertLogs(level='ERROR') as cm:
    #         call_sync()
    #         for out in cm.output:
    #             if 'ERROR' in out:
    #                 self.assertIn('Can\'t find item id', out)

    # @responses.activate
    # @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    # @patch('scout_manager.management.commands.techloan.techloan'
    #        '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    # @patch('scout_manager.management.commands.techloan.spotseeker'
    #        '.Spots._url', 'http://techloan.test/api/v1/spot')
    # def test_no_sync_for_unchanged_equips(self):
    #     responses.add(
    #         responses.GET,
    #         'http://techloan.test/api/v1/equipment',
    #         status=200,
    #         body=json.dumps(self.equip_with_img),
    #     )

    #     responses.add(
    #         responses.GET,
    #         f'http://techloan.test/api/v1/spot/?{urlencode(filter)}',
    #         status=200,
    #         body=json.dumps(self.mock_spots_bad_cte_ids),
    #     )

    #     for id in self.get_spot_ids(self.mock_spots):
    #         responses.add(
    #             responses.PUT,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps('OK'),
    #         )

    #         responses.add(
    #             responses.GET,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps(self.get_spot_by_id(id, self.mock_spots)),
    #         )

    #         for item_id in self.get_item_ids(self.mock_spots, spot_ids=[id]):
    #             responses.add(
    #                 responses.POST,
    #                 f'http://techloan.test/api/v1/item/{item_id}/image',
    #                 status=201,
    #                 body=json.dumps('OK'),
    #             )

    #             for image_id in self.get_image_ids(self.mock_spots, item_id):
    #                 responses.add(
    #                     responses.DELETE,
    #                     'http://techloan.test/api/v1/item/'
    #                     f'{item_id}/image/{image_id}',
    #                     status=200,
    #                     body=json.dumps('OK'),
    #                 )

    #     with self.assertLogs() as cm:
    #         test_logger.info('Starting full sync...')
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.get_techloan',
    #                    return_value=Techloan(self.equip_with_img)):
    #             techloan = Command.get_techloan()
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.get_spots',
    #                    return_value=Spots(self.mock_spots, None)):
    #             spots = Command.get_spots()
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.sync_techloan_to_spots',
    #                    return_value=spots.sync_with_techloan(techloan)):
    #             Command.sync_techloan_to_spots(techloan, spots)
    #         for out in cm.output:
    #             self.assertNotIn('ERROR', out)

    #     for item_id in self.get_item_ids(self.mock_spots, spot_ids=[id]):
    #         responses.add(
    #             responses.POST,
    #             f'http://techloan.test/api/v1/item/{item_id}/image',
    #             status=500,
    #             body=json.dumps('OK'),
    #         )

    #         for image_id in self.get_image_ids(self.mock_spots, item_id):
    #             responses.add(
    #                 responses.DELETE,
    #                 'http://techloan.test/api/v1/item/'
    #                 f'{item_id}/image/{image_id}',
    #                 status=500,
    #                 body=json.dumps('OK'),
    #             )

    #     with self.assertLogs() as cm:
    #         test_logger.info('Starting full sync...')
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.sync_techloan_to_spots',
    #                    return_value=spots.sync_with_techloan(techloan)):
    #             Command.sync_techloan_to_spots(techloan, spots)
    #         for out in cm.output:
    #             self.assertNotIn('ERROR', out)

    # @responses.activate
    # @override_settings(SPOTSEEKER_TECHLOAN_UPDATER=good_techloan_updater)
    # # cannot use override_settings for SPOTSEEKER_TECHLOAN_URL
    # @patch('scout_manager.management.commands.techloan.techloan'
    #        '.Techloan._url', 'http://techloan.test/api/v1/equipment')
    # @patch('scout_manager.management.commands.techloan.spotseeker'
    #        '.Spots._url', 'http://techloan.test/api/v1/spot')
    # def test_deactivate_spot_items_without_matching_cte_id(self):
    #     responses.add(
    #         responses.GET,
    #         'http://techloan.test/api/v1/equipment',
    #         status=200,
    #         body=json.dumps(self.equip_with_img),
    #     )

    #     responses.add(
    #         responses.GET,
    #         f'http://techloan.test/api/v1/spot/?{urlencode(filter)}',
    #         status=200,
    #         body=json.dumps(self.mock_spots_bad_cte_ids),
    #     )

    #     for id in self.get_spot_ids(self.mock_spots_bad_cte_ids):
    #         responses.add(
    #             responses.PUT,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps('OK'),
    #         )

    #         responses.add(
    #             responses.GET,
    #             f'http://techloan.test/api/v1/spot/{id}',
    #             status=200,
    #             body=json.dumps(
    #                 self.get_spot_by_id(id, self.mock_spots_bad_cte_ids)
    #             ),
    #         )

    #     item_ids = self.get_item_ids(self.mock_spots_bad_cte_ids)
    #     with self.assertLogs() as cm:
    #         test_logger.info('Starting full sync...')
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.get_techloan',
    #                    return_value=Techloan(self.equip_with_img)):
    #             techloan = Command.get_techloan()
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.get_spots',
    #                    return_value=Spots(
    #                       self.mock_spots_bad_cte_ids, None)):
    #             spots = Command.get_spots()
    #         with patch('scout_manager.management.commands.sync_techloan'
    #                    '.Command.sync_techloan_to_spots',
    #                    return_value=spots.sync_with_techloan(techloan)):
    #             Command.sync_techloan_to_spots(techloan, spots)
    #         for out in cm.output:
    #             self.assertNotIn('ERROR', out)
    #         for spot in spots:
    #             for item in spot['items']:
    #                 if 'id' not in item:
    #                     assert 'i_is_active' in item['extended_info']
    #                 elif item['id'] in item_ids:
    #                     assert 'i_is_active' not in item['extended_info']
