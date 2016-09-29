from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from scout_manager.dao.space import get_spot_by_id as manager_get_spot_by_id
from scout_manager.dao.space import get_spot_hours_by_day, get_spot_list
from scout_manager.dao.buildings import get_building_list, \
    get_building_list_by_campus
from scout.dao.image import get_image
from scout.dao.item import get_item_by_id, get_filtered_items, \
    get_item_count, add_item_info
from django.http import Http404, HttpResponse
import base64


def home(request):
    return render_to_response(
            'scout_manager/home.html',
            context_instance=RequestContext(request))


def items(request):
    spots = get_spot_list('tech')
    spots = get_filtered_items(spots, request)
    count = get_item_count(spots)
    if count <= 0:
        spots = []

    context = {"spots": spots,
               "count": count}
    return render_to_response('scout_manager/items.html', context,
                              context_instance=RequestContext(request))


def items_add(request):
    buildings = get_building_list()
    spots = get_spot_list()
    context = {"spots": spots,
               "buildings": buildings,
               "count": len(spots)}
    return render_to_response(
            'scout_manager/items_add.html',
            context,
            context_instance=RequestContext(request))


def items_edit(request, item_id):
    buildings = get_building_list()
    spots = get_spot_list()
    spot = get_item_by_id(int(item_id))
    context = {"spot": spot,
               "spots": spots,
               "buildings": buildings,
               "app_type": 'tech'}
    return render_to_response('scout_manager/items_edit.html', context,
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
    app_type = request.GET.get('app_type', None)
    is_published = request.GET.get('is_published', None)
    if is_published is not None:
        if is_published == "true":
            is_published = True
        elif is_published == "false":
            is_published = False
    spots = get_spot_list(app_type, is_published)
    context = {"spots": spots,
               "count": len(spots),
               "app_type": app_type}
    return render_to_response(
            'scout_manager/spaces.html',
            context,
            context_instance=RequestContext(request))


def spaces_add(request):
    buildings = get_building_list()
    context = {"buildings": buildings,
               "spot": {"grouped_hours": get_spot_hours_by_day(None)}}
    return render_to_response(
            'scout_manager/spaces_add.html',
            context,
            context_instance=RequestContext(request))


def spaces_upload(request):
    return render_to_response(
            'scout_manager/spaces_upload.html',
            context_instance=RequestContext(request))


def spaces_edit(request, spot_id):
    spot = manager_get_spot_by_id(spot_id)
    buildings = get_building_list_by_campus(spot.campus)
    # if no campus buildings, get all
    if len(buildings) < 1:
        buildings = get_building_list()
    context = {"spot": spot,
               "buildings": buildings,
               }
    return render_to_response(
            'scout_manager/spaces_edit.html',
            context,
            context_instance=RequestContext(request))


def image(request, image_id, spot_id):
    width = request.GET.get('width', None)
    try:
        resp, content = get_image(spot_id, image_id, width)
        etag = resp.get('etag', None)
        encoded_content = base64.b64encode(content)
        response = HttpResponse(encoded_content,
                                content_type=resp['content-type'])
        response['etag'] = etag
        return response
    except Exception:
        raise Http404()
