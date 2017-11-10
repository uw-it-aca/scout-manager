from scout_manager.test import ScoutTest
from django.test.client import RequestFactory
from scout_manager.views.api import Spot, SpotCreate, Item, process_form_data
from django.core.exceptions import ImproperlyConfigured
from spotseeker_restclient.exceptions import DataFailureException
import logging
from mock import patch
import json

spotCreateUrl = '/manager/api/spot/'
spotUrl = '/manager/api/spot/24/'


class ApiTest(ScoutTest):
    def setUp(self):
        # Disable logging during these tests
        logging.disable(logging.CRITICAL)
        self.spot = Spot()
        self.item = Item()
        self.spotCreate = SpotCreate()
        self.factory = RequestFactory()

    def tearDown(self):
        # Enable the logger for future use
        logging.disable(logging.NOTSET)

    # CREATE SPOT

    @patch('scout_manager.views.api.create_spot', return_value=False)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotCreate(self, mockProcessData, mockCreateSpot):
        request = self.factory.put(spotCreateUrl, {})
        result = self.spotCreate.PUT(request)
        # Assert that the create_spot method was called
        self.assertTrue(mockProcessData.called)
        self.assertTrue(mockCreateSpot.called)
        self.assertEqual(result.status_code, 200)

    @patch('scout_manager.views.api.create_spot', return_value=False)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotCreateConfigFailure(self, mockProcessData, mockCreateSpot):
        mockCreateSpot.side_effect = ImproperlyConfigured()
        request = self.factory.put(spotCreateUrl, {})
        result = self.spotCreate.PUT(request)
        # Assert that ImproperlyConfigured will result in a 500
        self.assertEqual(result.status_code, 500)

    @patch('scout_manager.views.api.create_spot', return_value=False)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotCreateDataFailure(self, mockProcessData, mockCreateSpot):
        mockCreateSpot.side_effect = DataFailureException("a", "b", "c")
        request = self.factory.put(spotCreateUrl, {})
        result = self.spotCreate.PUT(request)
        # Assert that a DataFailureException will result in a 400
        self.assertEqual(result.status_code, 400)

    # UPDATE SPOT

    @patch('scout_manager.views.api.update_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotUpdate(self, mockProcessData, mockUserService, mockEdit, mockUpdateSpot):
        request = self.factory.put(spotUrl, {})
        result = self.spot.PUT(request, '24')
        # Assert that the create_spot method was called
        self.assertTrue(mockProcessData.called)
        self.assertTrue(mockUpdateSpot.called)
        self.assertEqual(result.status_code, 200)

    @patch('scout_manager.views.api.update_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotUpdateConfigFailure(self, mockProcessData,
                                    mockUserService, mockEdit, mockUpdateSpot):
        mockUpdateSpot.side_effect = ImproperlyConfigured()
        request = self.factory.put(spotUrl, {})
        result = self.spot.PUT(request, '24')
        # Assert that the ImproperlyConfigured will result in a 500
        self.assertEqual(result.status_code, 500)

    @patch('scout_manager.views.api.update_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    @patch('scout_manager.views.api.process_form_data', return_value=False)
    def testSpotUpdateDataFailure(self, mockProcessData, mockUserService, mockEdit, mockUpdateSpot):
        mockUpdateSpot.side_effect = DataFailureException("a", "b", "c")
        request = self.factory.put(spotUrl, {})
        result = self.spot.PUT(request, '24')
        # Assert that a DataFailureException will result in a 400
        self.assertEqual(result.status_code, 400)

    # SPOT DELETE

    @patch('scout_manager.views.api.delete_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testSpotDelete(self, mockEdit, mockUserService, mockDeleteSpot):
        request = self.factory.put(spotUrl, {})
        result = self.spot.DELETE(request, '24')
        # Assert that the create_spot method was called
        self.assertTrue(mockDeleteSpot.called)
        self.assertEqual(result.status_code, 200)

    @patch('scout_manager.views.api.delete_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testSpotDeleteConfigFailure(self, mockEdit, mockUserService, mockDeleteSpot):
        mockDeleteSpot.side_effect = ImproperlyConfigured()
        request = self.factory.put(spotUrl, {})
        result = self.spot.DELETE(request, '24')
        # Assert that the ImproperlyConfigured will result in a 500
        self.assertEqual(result.status_code, 500)

    @patch('scout_manager.views.api.delete_spot', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testSpotDeleteDataFailure(self, mockEdit, mockUserService, mockDeleteSpot):
        mockDeleteSpot.side_effect = DataFailureException("a", "b", "c")
        request = self.factory.put(spotUrl, {})
        result = self.spot.DELETE(request, '24')
        # Assert that a DataFailureException will result in a 400
        self.assertEqual(result.status_code, 400)

    # ITEM DELETE

    @patch('scout_manager.views.api.delete_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testItemDelete(self, mockEdit, mockUserService, mockDeleteItem):
        request = self.factory.put(spotUrl, {})
        result = self.item.DELETE(request, '24')
        # Assert that the create_spot method was called
        self.assertTrue(mockDeleteItem.called)
        mockDeleteItem.assert_called_with('24', '{}')
        self.assertEqual(result.status_code, 200)

    @patch('scout_manager.views.api.delete_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testSpotDeleteConfigFailure(self, mockEdit, mockUserService, mockDeleteItem):
        mockDeleteItem.side_effect = ImproperlyConfigured()
        request = self.factory.put(spotUrl, {})
        result = self.item.DELETE(request, '24')
        # Assert that the ImproperlyConfigured will result in a 500
        self.assertEqual(result.status_code, 500)

    @patch('scout_manager.views.api.delete_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testItemDeleteDataFailure(self, mockEdit, mockUserService, mockDeleteItem):
        mockDeleteItem.side_effect = DataFailureException("a", "b", "c")
        request = self.factory.put(spotUrl, {})
        result = self.item.DELETE(request, '24')
        # Assert that a DataFailureException will result in a 400
        self.assertEqual(result.status_code, 400)

    # ITEM UPDATE
    @patch('scout_manager.views.api.process_form_data', return_value={"json": '{"spot_id": "1"}'})
    @patch('scout_manager.views.api.update_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testItemUpdate(self, mockEdit, mockUserService, mockUpdateItem, mockProcess):
        request = self.factory.put(spotUrl, {})
        result = self.item.PUT(request, '24')
        # Assert that the create_spot method was called
        self.assertTrue(mockUpdateItem.called)
        self.assertEqual(result.status_code, 200)

    @patch('scout_manager.views.api.process_form_data', return_value={"json": '{"spot_id": "1"}'})
    @patch('scout_manager.views.api.update_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testSpotUpdateConfigFailure(self, mockEdit, mockUserService, mockUpdateItem, mockProcess):
        mockUpdateItem.side_effect = ImproperlyConfigured()
        request = self.factory.put(spotUrl, {})
        result = self.item.PUT(request, '24')
        # Assert that the ImproperlyConfigured will result in a 500
        self.assertEqual(result.status_code, 500)

    @patch('scout_manager.views.api.process_form_data', return_value={"json": '{"spot_id": "1"}'})
    @patch('scout_manager.views.api.update_item', return_value=False)
    @patch('scout_manager.views.api.UserService')
    @patch('scout_manager.views.api.can_edit_spot', return_value=True)
    def testItemUpdateDataFailure(self, mockEdit, mockUserService, mockUpdateItem, mockProcess):
        mockUpdateItem.side_effect = DataFailureException("a", "b", "c")
        request = self.factory.put(spotUrl, {})
        result = self.item.PUT(request, '24')
        # Assert that a DataFailureException will result in a 400
        self.assertEqual(result.status_code, 400)

    # PROCESS FORM DATA

    def testProcessFormData(self):
        mockWebKitBoundary = '----WebKitFormBoundary1234'
        mockJSON = {
                    "csrfmiddlewaretoken": "1",
                    "name": "Kevin",
                    "id": "",
                    "etg": "",
                    "extended_info:has_cte_techloan": "",
                    "extended_info:cte_techloan_id": "",
                    "extended_info:app_type": "food",
                    "extended_info:is_hidden": "true",
                    "extended_info:owner": "Test",
                    "extended_info:campus": "seattle",
                    "location:latitude": "1",
                    "location:longitude": "1",
                    "available_hours": {}
                   }
        # Mocking the body of the request
        mockData = ('--' + mockWebKitBoundary +
                    '\nContent-Disposition: form-data; name="json"\n\n' +
                    json.dumps(mockJSON) + '\n--' + mockWebKitBoundary + '--\n')
        request = self.factory.put(spotUrl, mockData)
        request.META = {}
        request.META['CONTENT_TYPE'] = 'multipart/form-data; boundary=' + mockWebKitBoundary
        result = process_form_data(request)
        self.assertEqual(result['json'], json.dumps(mockJSON))
