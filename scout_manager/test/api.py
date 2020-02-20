from scout_manager.test import ScoutTest
from django.test.client import RequestFactory
from scout_manager.views.api import process_form_data
from mock import Mock
from PIL import Image
import json
import io
import os

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

    def testProcessImageData(self):
        mockWebKitBoundary = '----WebKitFormBoundaryz4dBfr609jFDl7b6'
        file_path = os.path.dirname(os.path.abspath(__file__))
        path = "{}/form_data".format(file_path)
        image_path = "{}/test_jpeg.jpg".format(file_path)

        mock_data = open(path, "rb").read()
        test_image = Image.open(image_path)
        mock_request = Mock()
        mock_request.body = mock_data
        mock_meta = {'CONTENT_TYPE': 'multipart/form-data; boundary=' + mockWebKitBoundary}
        mock_request.META = mock_meta

        result = process_form_data(mock_request)
        import pdb; pdb.set_trace()
        result_image = Image.open(io.BytesIO(result["file"].encode('utf-8')))
        self.assertEqual(test_image, result_image)

        result_json = json.loads(result['json'])
        self.assertEqual(result_json['id'], "114")
        self.assertEqual(result_json['name'], "In the Art Building - multiline name to test")
        self.assertEqual(result_json['extended_info:app_type'], "food")
        self.assertEqual(result_json['extended_info:campus'], "seattle")
        self.assertEqual(result_json['extended_info:owner'], "u_acadev_tester")
        self.assertEqual(result_json['extended_info:has_cte_techloan'], "")
        self.assertEqual(result_json['extended_info:cte_techloan_id'], "")
        self.assertEqual(result_json['extended_info:s_description'], "test")
        self.assertEqual(result_json['location:latitude'], "47.65824100")
        self.assertEqual(result_json['location:longitude'], "-122.30664400")
        self.assertEqual(result_json['location:building_name'], "Art Building (ART)")
        self.assertEqual(result_json['etag'], "fcebcc8bd09a011b2d3af333f0f23078ad37f2b3")
