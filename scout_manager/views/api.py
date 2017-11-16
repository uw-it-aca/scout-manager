from scout_manager.views.rest_dispatch import RESTDispatch
from scout_manager.dao.space import update_spot, create_spot, delete_spot,\
    get_spot_by_id
from scout_manager.dao.groups import is_superuser, is_provisioned_user
from scout_manager.dao.item import update_item, create_item, delete_item
from django.http import HttpResponse
from scout_manager.models import Person, GroupMembership
from userservice.user import UserService
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
import json
import re
import logging

logging.basicConfig()
logger = logging.getLogger("scout_manager")


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
            if (isinstance(ex, ImproperlyConfigured)):
                return _improperly_configured_handler(ex)
            logger.exception("Error updating spot user: %s spot_id: %s" %
                             (user, spot_id))
            return HttpResponse(str(ex.message), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')

    def DELETE(self, request, spot_id):
        user = UserService().get_user()
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        etag = request.body
        try:
            delete_spot(spot_id, etag)
        except Exception as ex:
            if (isinstance(ex, ImproperlyConfigured)):
                return _improperly_configured_handler(ex)
            logger.exception("Error deleting spot user: %s spot_id: %s" %
                             (user, spot_id))
            return HttpResponse(str(ex.message), status=400,
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
    return (is_superuser(user) or is_provisioned_user(user))


def _get_current_spot_group(spot_id):
    spot = get_spot_by_id(spot_id)
    return spot.owner


# Return a 500 for ImproperlyConfigured errors to activate the appropriate
# error message on the clientside
def _improperly_configured_handler(ex):
    logger.exception("Improperly configured settings")
    return HttpResponse(str(ex.message), status=500,
                        content_type='application/json')


class SpotCreate(RESTDispatch):
    """
    Handles Spot creation, using PUT to deal with django issues
    """

    def PUT(self, request):
        form_data = process_form_data(request)
        try:
            spot_id = create_spot(form_data)
        except Exception as ex:
            if (isinstance(ex, ImproperlyConfigured)):
                return _improperly_configured_handler(ex)
            logger.exception("Error creating spot")
            return HttpResponse(str(ex.message), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'Created',
                                        'id': spot_id}),
                            content_type='application/json')


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
            if (isinstance(ex, ImproperlyConfigured)):
                return _improperly_configured_handler(ex)
            return HttpResponse(str(ex.message), status=400,
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')

    def DELETE(self, request, item_id):
        user = UserService().get_user()
        spot_id = request.body
        if not can_edit_spot(spot_id, user):
            raise PermissionDenied
        try:
            delete_item(item_id, spot_id)
        except Exception as ex:
            if (isinstance(ex, ImproperlyConfigured)):
                return _improperly_configured_handler(ex)
            return HttpResponse(str(ex.message), status=400,
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
        create_item(form_data)
        # except Exception as ex:
        #     return HttpResponse(json.dumps({'error': str(ex)}), status=400,
        #                         content_type='application/json')
        return HttpResponse(json.dumps({'status': 'it works'}),
                            content_type='application/json')
