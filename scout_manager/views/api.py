# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from scout_manager.views.rest_dispatch import RESTDispatch
from scout_manager.dao.space import (
    update_spot,
    create_spot,
    delete_spot,
    get_spot_by_id,
)
from scout_manager.dao.groups import is_superuser, is_provisioned_user
from scout_manager.dao.item import update_item, create_item, delete_item
from django.http import HttpResponse
from scout_manager.models import Person, GroupMembership
from userservice.user import UserService
from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
import json
import re
import logging

logging.basicConfig()
logger = logging.getLogger("scout_manager")


@method_decorator(group_required(settings.SCOUT_MANAGER_ACCESS_GROUP),
                  name="run")
class Spot(RESTDispatch):
    """
    Handles changes to spots
    """

    def PUT(self, request, spot_id):
        user = UserService().get_user()
        form_data = process_form_data(request)
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        try:
            update_spot(form_data, spot_id)
        except Exception as ex:
            if isinstance(ex, ImproperlyConfigured):
                return _improperly_configured_handler(ex)
            # if spotseeker returns a 401, it's unauthorized
            if ex.status == 401:
                return _unauthorized_handler(ex)
            logger.exception(
                "Error updating spot user: %s spot_id: %s" % (user, spot_id)
            )
            ex.msg = json.loads(ex.msg)
            ex.msg = ex.msg.get("__all__")
            if ex.msg is not None:
                ex.msg = ' '.join(ex.msg)
            else:
                ex.msg = "Form is invalid"
            return HttpResponse(
                str(ex.msg), status=400, content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "it works"}), content_type="application/json"
        )

    def DELETE(self, request, spot_id):
        user = UserService().get_user()
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        etag = request.body
        try:
            delete_spot(spot_id, etag)
        except Exception as ex:
            if isinstance(ex, ImproperlyConfigured):
                return _improperly_configured_handler(ex)
            logger.exception(
                "Error deleting spot user: %s spot_id: %s" % (user, spot_id)
            )
            return HttpResponse(
                str(ex.msg), status=400, content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "it works"}), content_type="application/json"
        )


def process_form_data(request):
    if request.META["CONTENT_TYPE"].startswith("multipart"):
        put, files = request.parse_file_upload(request.META, request)
        request.FILES.update(files)
        put_dict = put.dict()
        if "file" in files:
            put_dict["file"] = files["file"].file
        request.PUT = put_dict
    else:
        put_dict = QueryDict(request.body).dict()
        request.PUT = put_dict

    form_data = request.PUT
    return form_data


def can_edit_spot(spot_id, user):
    """
    Determines if a user can edit the given spot based on them being a member
    of the existing group attached to the spot, also allows 'superusers'
    """
    try:
        group_id = _get_current_spot_group(spot_id)
    except AttributeError:
        group_id = None
    is_spot_editor = GroupMembership.objects.is_member(user, group_id)
    if not is_spot_editor:
        is_spot_editor = is_superuser(user)
    return is_spot_editor


def can_add_spot(member_id):
    """
    Determines if a user can add spots based on them being a member
    of *any* spot group, also allows 'superusers'
    """
    user = UserService().get_user()
    return is_superuser(user) or is_provisioned_user(user)


def _get_current_spot_group(spot_id):
    spot = get_spot_by_id(spot_id)
    return spot.owner


# Return a 500 for ImproperlyConfigured errors to activate the appropriate
# error message on the clientside
def _improperly_configured_handler(ex):
    logger.exception("Improperly configured settings")
    return HttpResponse(
        str(ex.msg), status=500, content_type="application/json"
    )


# Return a 403 (for now) for Unauthorized errors to activate the appropriate
# error message on the clientside
def _unauthorized_handler(ex):
    logger.exception("Unauthorized user")
    return HttpResponse(
        str(ex.msg), status=403, content_type="application/json"
    )


@method_decorator(group_required(settings.SCOUT_MANAGER_ACCESS_GROUP),
                  name="run")
class SpotCreate(RESTDispatch):
    """
    Handles Spot creation, using PUT to deal with django issues
    """

    def PUT(self, request):
        form_data = process_form_data(request)
        try:
            spot_id = create_spot(form_data)
        except Exception as ex:
            if isinstance(ex, ImproperlyConfigured):
                return _improperly_configured_handler(ex)
            # if spotseeker returns a 401, it's unauthorized
            if ex.status == 401:
                return _unauthorized_handler(ex)
            logger.exception("Error creating spot")
            return HttpResponse(
                str(ex.msg), status=400, content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "Created", "id": spot_id}),
            content_type="application/json",
        )


@method_decorator(group_required(settings.SCOUT_MANAGER_ACCESS_GROUP),
                  name="run")
class Item(RESTDispatch):
    """
    Handles changes to items
    """

    def PUT(self, request, item_id):
        user = UserService().get_user()
        form_data = process_form_data(request)
        # quick fix, until can_edit_item is implemented.
        spot_id = json.loads(form_data["json"])["spot_id"]
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        try:
            update_item(form_data, item_id)
        except Exception as ex:
            if isinstance(ex, ImproperlyConfigured):
                return _improperly_configured_handler(ex)
            return HttpResponse(
                str(ex.msg), status=400, content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "it works"}), content_type="application/json"
        )

    def DELETE(self, request, item_id):
        user = UserService().get_user()
        spot_id = request.body
        spot_id = int(spot_id)
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        try:
            delete_item(item_id, spot_id)
        except Exception as ex:
            if isinstance(ex, ImproperlyConfigured):
                return _improperly_configured_handler(ex)
            return HttpResponse(
                str(ex.msg), status=400, content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "it works"}), content_type="application/json"
        )


@method_decorator(group_required(settings.SCOUT_MANAGER_ACCESS_GROUP),
                  name="run")
class ItemCreate(RESTDispatch):
    """
    Handles Item creation, using PUT to deal with django issues
    """

    def PUT(self, request):
        form_data = process_form_data(request)
        # try:
        create_item(form_data)
        # except Exception as ex:
        #     return HttpResponse(json.dumps({'error': str(ex)}), status=400,
        #                         content_type='application/json')
        return HttpResponse(
            json.dumps({"status": "it works"}), content_type="application/json"
        )
