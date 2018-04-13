from restclients.gws import GWS
from restclients.exceptions import DataFailureException, InvalidGroupID
from scout_manager.models import Group, Person, GroupMembership
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
import logging

logging.basicConfig()
logger = logging.getLogger("scout_manager")


def get_members(group_id):
    gws = GWS()
    try:
        members = gws.get_effective_members(group_id)
    except InvalidGroupID:
        return []
    return members


def is_member(group_id, member_id):
    gws = GWS()
    try:
        return gws.is_effective_member(group_id, member_id)
    except InvalidGroupID:
        return False


def is_provisioned_user(member_id):
    user_exists = True
    try:
        Person.objects.get(netid=member_id).exists()
    except ObjectDoesNotExist:
        user_exists = False
    return user_exists


def is_superuser(member_id):
    if settings.MANAGER_SUPERUSER_GROUP:
        is_spot_editor = is_member(settings.MANAGER_SUPERUSER_GROUP, member_id)
        return is_spot_editor
    else:
        raise ImproperlyConfigured("Must define a MANAGER_SUPERUSER_GROUP"
                                   "in the settings")


def add_group(group_id):
    group, created = Group.objects.get_or_create(group_id=group_id)
    if created:
        try:
            _update_group(group)
        except DataFailureException:
            logger.exception("Adding group: %s" % group_id)
            pass


def update_groups():
    groups_to_update = Group.objects.all()
    for group in groups_to_update:
        try:
            _update_group(group)
        except DataFailureException:
            logger.exception("Updating group: %s" % group.group_id)
            pass

    _remove_orphaned_people()


def _remove_orphaned_people():
    for person in Person.objects.all():
        netid = person.netid
        if 0 == len(GroupMembership.objects.filter(person__netid=netid)):
            person.delete()


def _update_group(group):
    # Create person models for newly seen people
    remote_members = get_members(group.group_id)
    remote_people = []
    for member in remote_members:
        if member.member_type == 'uwnetid':
            person, created = Person.objects.get_or_create(netid=member.name)
            remote_people.append(person)

    # Remove local group members who are not in remote group
    group_people_ids = []
    for person in remote_people:
        group_people_ids.append(person.pk)
    people_to_remove = GroupMembership.objects.filter(group=group)\
        .exclude(person__in=group_people_ids)
    people_to_remove.delete()

    # Add new members to group and update timestamps
    for person in remote_people:
        membership, created = GroupMembership\
            .objects.get_or_create(group=group, person=person)
        if not created:
            # update timestamp
            membership.save()
