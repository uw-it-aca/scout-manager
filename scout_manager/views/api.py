from scout_manager.views.rest_dispatch import RESTDispatch
from scout_manager.dao.space import update_spot
from django.http import HttpResponse
import json
import re


class Spot(RESTDispatch):
    """
    Handles changes to spots
    """

    def POST(self, request):
        return HttpResponse('it works')

    def PUT(self, request, spot_id):
        data = json.loads(request.body)
        try:
            update_spot(data, spot_id)
        except Exception as ex:
            return HttpResponse(json.dumps({'error': str(ex)}), status=400)
        return HttpResponse(json.dumps({'status': 'it works'}))


def process_form_data(request):
    form_data = {}
    content_type = request.META['CONTENT_TYPE']
    for param in content_type.split(";"):
        if "boundary" in param:
            boundary = param.replace("boundary=", "").strip()
            # add two dashes, for some reason
            boundary = "--" + boundary
    blocks = request.body.split(boundary)
    for block in blocks:
        for line in block.splitlines():
            if "Content-Disposition" in line:
                match = re.findall(r'name=\"(.*)\"', line)
                block_name = match[0]
            elif len(line) > 0 and line != "--":
                form_data[block_name] = line
    return form_data
