from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response
from scout.dao.space import get_spot_list, get_spot_by_id
from scout_manager.dao.space import get_spot_by_id as manager_get_spot_by_id
from spotseeker_restclient.spotseeker import Spotseeker


def home(request):
    return render_to_response(
            'scout_manager/home.html',
            context_instance=RequestContext(request))


def items(request):
    return render_to_response(
            'scout_manager/items.html',
            context_instance=RequestContext(request))


def items_add(request):
    spots = get_spot_list()
    context = {"spots": spots,
               "count": len(spots)}
    return render_to_response(
            'scout_manager/items_add.html',
            context,
            context_instance=RequestContext(request))


def items_edit(request, item_id):
    spots = get_spot_list()
    context = {"spots": spots,
               "count": len(spots)}
    return render_to_response(
            'scout_manager/items_edit.html',
            context,
            context_instance=RequestContext(request))


def schedule(request, spot_id):
    spot = manager_get_spot_by_id(spot_id)
    context = {"spot": spot}
    return render_to_response(
            'scout_manager/schedule.html',
            context,
            context_instance=RequestContext(request))


def spaces(request):
    # TODO: filter this by spot manager
    # TODO: add support for multiple spot types (Eg items)
    spots = get_spot_list()
    context = {"spots": spots,
               "count": len(spots)}
    return render_to_response(
            'scout_manager/spaces.html',
            context,
            context_instance=RequestContext(request))


def spaces_add(request):
    spot_client = Spotseeker()
    # building search only returns study buildings by default
    buildings = spot_client.get_building_list()
    buildings += spot_client.get_building_list("food")
    context = {"buildings": buildings}
    return render_to_response(
            'scout_manager/spaces_add.html',
            context,
            context_instance=RequestContext(request))


def spaces_edit(request, spot_id):
    spot = manager_get_spot_by_id(spot_id)
    spot_client = Spotseeker()
    # building search only returns study buildings by default
    buildings = spot_client.get_building_list()
    buildings += spot_client.get_building_list("food")
    context = {"spot": spot,
               "buildings": buildings,
               }
    return render_to_response(
            'scout_manager/spaces_edit.html',
            context,
            context_instance=RequestContext(request))
