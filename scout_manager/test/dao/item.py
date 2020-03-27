from scout_manager.dao.item import _build_item_json, create_item, _get_spot_json
from uw_spotseeker import Spotseeker
from scout_manager.test import ScoutTest
from mock import patch
import datetime
import json


class ItemDaoTest(ScoutTest):
    def setUp(self):
        self.test_item = {
            'id': '',
            'spot_id': '1',
            'name': 'Test Item',
            'category': 'computers',
            'subcategory': 'Laptop Computer',
            'extended_info:i_brand': 'Apple',
            'extneded_info:i_description': 'For testing...',
            'etag': '74d3d61ac442fc076d104b120lf86a5cb82fa3'
        }

    def test_create_single_item(self):
        test_data = {'json': json.dumps(self.test_item)}
        item_json = _build_item_json(test_data)
        item_json.pop('id')
        item_json.pop('spot_id')
        json_data = _get_spot_json('1')
        etag = json_data['etag']
        json_data['items'].append(item_json)
        with patch.object(Spotseeker, 'put_spot') as mock_put:
            create_item(test_data)
            mock_put.assert_called_once_with('1', json.dumps(json_data), etag)

    def test_create_item_batch(self):
        test_list = [self.test_item, self.test_item]
        test_data = {'json': json.dumps(test_list)}
        item_json = _build_item_json({'json': json.dumps(self.test_item)})
        item_json.pop('id')
        item_json.pop('spot_id')
        json_data = _get_spot_json('1')
        etag = test_list[0]['etag']
        json_data['items'].append(item_json)
        json_data['items'].append(item_json)
        with patch.object(Spotseeker, 'put_spot') as mock_put:
            create_item(test_data)
            mock_put.assert_called_once_with('1', json.dumps(json_data), etag)

