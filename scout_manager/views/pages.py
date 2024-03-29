# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.template import RequestContext
from django.shortcuts import render
from scout_manager.dao.item import (
    get_spot_by_item_id as manager_get_spot_by_item_id
)
from scout_manager.dao.space import get_spot_by_id as manager_get_spot_by_id
from scout_manager.dao.space import get_spot_hours_by_day, get_spot_list
from scout_manager.dao.buildings import get_building_list
from scout_manager.dao.groups import is_superuser
from scout_manager.models import GroupMembership
from restclients_core.exceptions import DataFailureException
from scout.dao.image import get_spot_image, get_item_image
from scout.dao.item import get_filtered_items, get_item_count
from scout.dao.space import get_spot_list as get_spots
from scout.views import CAMPUS_LOCATIONS, extract_spots_item_info
from django.http import Http404, HttpResponse
from userservice.user import UserService
from django.conf import settings
from uw_saml.decorators import group_required
import base64


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def home(request):
    netid = UserService().get_user()
    return render(request, "scout_manager/home.html", {"netid": netid})


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def items(request):
    netid = UserService().get_user()
    spots = get_spot_list("tech")
    spots = _filter_spots(spots, netid)
    spots = get_filtered_items(spots, request)
    count = get_item_count(spots)
    if count <= 0:
        spots = []

    context = {
        "spots": spots,
        "count": count,
        "netid": netid,
        "is_superuser": is_superuser(netid),
    }
    return render(request, "scout_manager/items.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def items_add(request):
    netid = UserService().get_user()
    buildings = get_building_list()
    tech_spots = get_spots("tech")
    info = extract_spots_item_info(tech_spots)
    spot = (
        manager_get_spot_by_id(request.GET.get("spot_id"))
        if request.GET.get("spot_id")
        else None
    )
    context = {
        "spot": spot,
        "buildings": buildings,
        "filters": info,
        "is_superuser": is_superuser(netid),
        "netid": netid,
    }
    return render(request, "scout_manager/items_add.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def items_add_batch(request):
    netid = UserService().get_user()
    buildings = get_building_list()
    tech_spots = get_spots("tech")
    info = extract_spots_item_info(tech_spots)
    spot = (
        manager_get_spot_by_id(request.GET.get("spot_id"))
        if request.GET.get("spot_id")
        else None
    )

    context = {
        "spot": spot,
        "buildings": buildings,
        "filters": info,
        "netid": netid,
    }
    return render(request, "scout_manager/items_add_batch.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def items_edit(request, item_id):
    netid = UserService().get_user()
    buildings = get_building_list()
    spot = manager_get_spot_by_item_id(int(item_id))
    tech_spots = get_spots("tech")
    info = extract_spots_item_info(tech_spots)

    context = {
        "spot": spot,
        "buildings": buildings,
        "app_type": "tech",
        "is_superuser": is_superuser(netid),
        "filters": info,
        "netid": netid,
    }
    return render(request, "scout_manager/items_edit.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def schedule(request, spot_id):
    netid = UserService().get_user()
    spot = manager_get_spot_by_id(spot_id)
    context = {"spot": spot, "netid": netid}
    return render(request, "scout_manager/schedule.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def spaces(request):
    netid = UserService().get_user()

    app_type = request.GET.get("app_type", None)
    is_published = request.GET.get("is_published", None)
    if is_published is not None:
        if is_published == "true":
            is_published = True
        elif is_published == "false":
            is_published = False
    spots = get_spot_list(app_type, is_published)
    if netid:
        spots = _filter_spots(spots, netid)
    else:
        return HttpResponse("Unauthorized", status=401)

    context = {
        "spots": spots,
        "count": len(spots),
        "app_type": app_type,
        "netid": netid,
        "is_superuser": is_superuser(netid),
    }
    return render(request, "scout_manager/spaces.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def spaces_add(request):
    netid = UserService().get_user()
    buildings = get_building_list()
    context = {
        "buildings": buildings,
        "spot": {"grouped_hours": get_spot_hours_by_day(None)},
        "campus_locations": CAMPUS_LOCATIONS,
        "netid": netid,
    }
    return render(request, "scout_manager/spaces_add.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def spaces_upload(request):
    netid = UserService().get_user()
    return render(
        request,
        "scout_manager/spaces_upload.html",
        {"netid": netid},
    )


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def spaces_edit(request, spot_id):
    netid = UserService().get_user()

    try:
        spot = manager_get_spot_by_id(spot_id)
    except DataFailureException as e:
        if e.status == 404:
            raise Http404()
        else:
            raise e
    buildings = get_building_list()
    # if no campus buildings, get all
    if len(buildings) < 1:
        buildings = get_building_list()
    context = {
        "spot": spot,
        "buildings": buildings,
        "campus_locations": CAMPUS_LOCATIONS,
        "netid": netid,
    }
    return render(request, "scout_manager/spaces_edit.html", context)


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def image(request, image_id, spot_id):
    width = request.GET.get("width", None)
    try:
        resp, content = get_spot_image(spot_id, image_id, width)
        etag = resp.headers.get("etag", None)
        encoded_content = base64.b64encode(content)
        response = HttpResponse(
            encoded_content, content_type=resp.headers["content-type"]
        )
        response["etag"] = etag
        return response
    except Exception:
        raise Http404()


@group_required(settings.SCOUT_MANAGER_ACCESS_GROUP)
def item_image(request, image_id, item_id):
    width = request.GET.get("width", None)
    try:
        resp, content = get_item_image(item_id, image_id, width)
        etag = resp.headers.get("etag", None)
        encoded_content = base64.b64encode(content)
        response = HttpResponse(
            encoded_content, content_type=resp.headers["content-type"]
        )
        response["etag"] = etag
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
