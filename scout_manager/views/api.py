from scout_manager.views.rest_dispatch import RESTDispatch
from scout_manager.dao.space import update_spot
from django.http import HttpResponse
import json

class Spot(RESTDispatch):
    """
    Handles changes to spots
    """

    def POST(self, request):
        return HttpResponse('it works')

    def PUT(self, request, spot_id):
        data = json.loads(request.body)
        update_spot(data)
        return HttpResponse('it works')