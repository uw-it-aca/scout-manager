from scout_manager.test import ScoutTest
from django.test.client import RequestFactory
from scout_manager.views.api import process_form_data
import json

# URL for a mock endpoint
spotUrl = '/manager/api/spot/24/'


class ApiTest(ScoutTest):
    def setUp(self):
        self.factory = RequestFactory()

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
        # Mock the request itself
        request = self.factory.put(spotUrl, mockData)
        request.META = {}
        request.META['CONTENT_TYPE'] = 'multipart/form-data; boundary=' + mockWebKitBoundary
        result = process_form_data(request)
        # Assert that we can properly get the correct json from the request body
        self.assertEqual(result['json'], json.dumps(mockJSON))
