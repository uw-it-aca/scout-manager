from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response
from scout.dao.space import get_spot_list


def list(request):
    # TODO: filter this by spot manager
    # TODO: add support for multiple spot types (Eg items)
    spots = get_spot_list()
    context = {"spots": spots,
               "count": len(spots)}
    return render_to_response(
            'scout_manager/list.html',
            context,
            context_instance=RequestContext(request))


def add(request):
    return render_to_response(
            'scout_manager/add.html',
            context_instance=RequestContext(request))


def item(request):
    return render_to_response(
            'scout_manager/item.html',
            context_instance=RequestContext(request))


def future(request):
    return render_to_response(
            'scout_manager/future.html',
            context_instance=RequestContext(request))


def space(request):
    return render_to_response(
            'scout_manager/space.html',
            context_instance=RequestContext(request))
