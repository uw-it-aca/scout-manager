from scout_manager.views.rest_dispatch import RESTDispatch
from django.http import HttpResponse


class Spot(RESTDispatch):
    """
    Handles changes to spots
    """

    def POST(self, request):
        return HttpResponse('it works')
