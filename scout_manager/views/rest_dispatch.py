# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import sys
from django.http import HttpResponse


class RESTDispatch:
    """
    Handles passing on the request to the correct view
    method based on the request type.
    """

    def run(self, *args, **named_args):
        request = args[0]

        if "GET" == request.META["REQUEST_METHOD"]:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return invalid_method()
        elif "POST" == request.META["REQUEST_METHOD"]:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return invalid_method()
        elif "PUT" == request.META["REQUEST_METHOD"]:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return invalid_method()
        elif "DELETE" == request.META["REQUEST_METHOD"]:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return invalid_method()

        else:
            return invalid_method()


def _make_response(status_code, reason_phrase):
    response = HttpResponse(reason_phrase)
    response.status_code = status_code
    response.reason_phrase = reason_phrase
    response.write(response.content)
    return response


def data_not_found():
    return _make_response(404, "Data not found")


def invalid_method():
    return _make_response(405, "Method not allowed")
