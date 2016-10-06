from scout_manager.views.rest_dispatch import RESTDispatch
from scout_manager.dao.space import update_spot, create_spot, delete_spot
from scout_manager.dao.item import delete_item
from django.http import HttpResponse
import json
import re


class Spot(RESTDispatch):
    """
    Handles changes to spots
    """

    def PUT(self, request, spot_id):
        form_data = process_form_data(request)
        try:
            update_spot(form_data, spot_id)
        except Exception as ex:
            return HttpResponse(json.dumps({'error': str(ex)}), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')

    def DELETE(self, request, spot_id):
        etag = request.body
        try:
            delete_spot(spot_id, etag)
        except Exception as ex:
            return HttpResponse(json.dumps({'error': str(ex)}), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')


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
        block_data = ''
        file_start_idx = None
        for index, line in enumerate(block.splitlines()):
            if "Content-Disposition" in line:
                match = re.findall(r'name=\"(.*?)\"', line)
                block_name = match[0]
            elif len(line) > 0 and line != "--" and "Content-Type" not in line:
                if file_start_idx is None:
                    file_start_idx = index
                block_data += line
        if len(block_data) > 0:
            if block_name == "file":
                file_block = block.splitlines(True)[file_start_idx:]
                file_data = ''.join(file_block)
                form_data[block_name] = file_data.strip()
            else:
                form_data[block_name] = block_data
    return form_data


class SpotCreate(RESTDispatch):
    """
    Handles Spot creation, using PUT to deal with django issues
    """

    def PUT(self, request):
        form_data = process_form_data(request)
        # try:
        create_spot(form_data)
        # except Exception as ex:
        #     return HttpResponse(json.dumps({'error': str(ex)}), status=400,
        #                         content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')


class Item(RESTDispatch):
    """
    Handles changes to items
    """

    def PUT(self, request, item_id):
        form_data = process_form_data(request)
        try:
            pass
            # update_item(form_data, item_id)
        except Exception as ex:
            return HttpResponse(json.dumps({'error': str(ex)}), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')

    def DELETE(self, request, item_id):
        spot_id = request.body
        try:
            delete_item(item_id, spot_id)
        except Exception as ex:
            return HttpResponse(json.dumps({'error': str(ex)}), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')


class ItemCreate(RESTDispatch):
    """
    Handles Item creation, using PUT to deal with django issues
    """

    def PUT(self, request):
        form_data = process_form_data(request)
        # try:
        # create_item(form_data)
        # except Exception as ex:
        #     return HttpResponse(json.dumps({'error': str(ex)}), status=400,
        #                         content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')
