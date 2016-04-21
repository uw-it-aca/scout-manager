from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response
from scout.dao.space import get_spot_list, get_spot_by_id


def home(request):
    return render_to_response(
            'scout_manager/home.html',
            context_instance=RequestContext(request))


def items(request):
    return render_to_response(
            'scout_manager/items.html',
            context_instance=RequestContext(request))


def items_add(request):
    return render_to_response(
            'scout_manager/items_add.html',
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
    spot = get_spot_by_id(spot_id)
    return render_to_response(
            'scout_manager/schedule.html',
            {'spot': spot},
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
    return render_to_response(
            'scout_manager/spaces_add.html',
            context_instance=RequestContext(request))


def spaces_edit(request, spot_id):
    spot = get_spot_by_id(spot_id)
    print spot.spot_types[0].__dict__
    return render_to_response(
            'scout_manager/spaces_edit.html',
            {'spot': spot},
            context_instance=RequestContext(request))
