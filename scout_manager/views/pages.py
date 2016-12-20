from django.template import RequestContext
from django.shortcuts import render_to_response
from scout_manager.dao.item import get_item_by_id as manager_get_item_by_id
from scout_manager.dao.space import get_spot_by_id as manager_get_spot_by_id
from scout_manager.dao.space import get_spot_hours_by_day, get_spot_list
from scout_manager.dao.buildings import get_building_list
from scout_manager.dao.groups import is_superuser
from scout_manager.models import GroupMembership
from scout.dao.image import get_spot_image, get_item_image
from scout.dao.item import get_filtered_items, get_item_count
from scout.views import CAMPUS_LOCATIONS
from django.http import Http404, HttpResponse
from userservice.user import UserService
import base64


def home(request):
    netid = UserService().get_user()
    return render_to_response(
            'scout_manager/home.html',
            {"netid": netid},
            context_instance=RequestContext(request))


def items(request):
    netid = UserService().get_user()
    spots = get_spot_list('tech')
    spots = _filter_spots(spots, netid)
    spots = get_filtered_items(spots, request)
    count = get_item_count(spots)
    if count <= 0:
        spots = []

    context = {"spots": spots,
               "count": count,
               "netid": netid,
               "is_superuser": is_superuser(netid)}
    return render_to_response('scout_manager/items.html', context,
                              context_instance=RequestContext(request))


def items_add(request):
    netid = UserService().get_user()
    buildings = get_building_list()
    spots = get_spot_list()
    spot = manager_get_spot_by_id(request.GET.get('spot_id')) \
        if request.GET.get('spot_id') else None
    context = {"spot": spot,
               "spots": spots,
               "buildings": buildings,
               "count": len(spots),
               "netid": netid}
    return render_to_response(
            'scout_manager/items_add.html',
            context,
            context_instance=RequestContext(request))


def items_edit(request, item_id):
    netid = UserService().get_user()
    buildings = get_building_list()
    spots = get_spot_list()
    spot = manager_get_item_by_id(int(item_id))
    context = {"spot": spot,
               "spots": spots,
               "buildings": buildings,
               "app_type": 'tech',
               "netid": netid}
    return render_to_response('scout_manager/items_edit.html', context,
                              context_instance=RequestContext(request))


def schedule(request, spot_id):
    netid = UserService().get_user()
    spot = manager_get_spot_by_id(spot_id)
    context = {"spot": spot,
               "netid": netid}
    return render_to_response(
            'scout_manager/schedule.html',
            context,
            context_instance=RequestContext(request))


def spaces(request):
    netid = UserService().get_user()

    app_type = request.GET.get('app_type', None)
    is_published = request.GET.get('is_published', None)
    if is_published is not None:
        if is_published == "true":
            is_published = True
        elif is_published == "false":
            is_published = False
    spots = get_spot_list(app_type, is_published)
    spots = _filter_spots(spots, netid)

    context = {"spots": spots,
               "count": len(spots),
               "app_type": app_type,
               "netid": netid,
               "is_superuser": is_superuser(netid)}
    return render_to_response(
            'scout_manager/spaces.html',
            context,
            context_instance=RequestContext(request))


def spaces_add(request):
    netid = UserService().get_user()
    buildings = get_building_list()
    context = {"buildings": buildings,
               "spot": {"grouped_hours": get_spot_hours_by_day(None)},
               "campus_locations": CAMPUS_LOCATIONS,
               "netid": netid}
    return render_to_response(
            'scout_manager/spaces_add.html',
            context,
            context_instance=RequestContext(request))


def spaces_upload(request):
    netid = UserService().get_user()
    return render_to_response(
            'scout_manager/spaces_upload.html',
            {"netid": netid},
            context_instance=RequestContext(request))


def spaces_edit(request, spot_id):
    netid = UserService().get_user()
    spot = manager_get_spot_by_id(spot_id)
    buildings = get_building_list()
    # if no campus buildings, get all
    if len(buildings) < 1:
        buildings = get_building_list()
    context = {"spot": spot,
               "buildings": buildings,
               "campus_locations": CAMPUS_LOCATIONS,
               "netid": netid
               }
    return render_to_response(
            'scout_manager/spaces_edit.html',
            context,
            context_instance=RequestContext(request))


def image(request, image_id, spot_id):
    width = request.GET.get('width', None)
    try:
        resp, content = get_spot_image(spot_id, image_id, width)
        etag = resp.get('etag', None)
        encoded_content = base64.b64encode(content)
        response = HttpResponse(encoded_content,
                                content_type=resp['content-type'])
        response['etag'] = etag
        return response
    except Exception:
        raise Http404()


def item_image(request, image_id, item_id):
    width = request.GET.get('width', None)
    try:
        resp, content = get_item_image(item_id, image_id, width)
        etag = resp.get('etag', None)
        encoded_content = base64.b64encode(content)
        response = HttpResponse(encoded_content,
                                content_type=resp['content-type'])
        response['etag'] = etag
        return response
    except Exception:
        raise Http404()


def _filter_spots(spots, netid):
    if is_superuser(netid):
        return spots
    user_groups = GroupMembership.objects.filter(person__netid=netid)
    group_ids = []
    for group in user_groups:
        group_ids.append(group.group.group_id)
    filtered_spots = []
    for spot in spots:
        if hasattr(spot, "owner"):
            if spot.owner in group_ids:
                filtered_spots.append(spot)

    return filtered_spots
