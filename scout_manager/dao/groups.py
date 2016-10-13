from restclients.gws import GWS
from restclients.exceptions import DataFailureException, InvalidGroupID
from scout_manager.models import Group, Person, GroupMembership


def get_members(group_id):
    gws = GWS()
    members = gws.get_effective_members(group_id)
    return members


def is_member(group_id, member_id):
    gws = GWS()
    try:
        return gws.is_effective_member(group_id, member_id)
    except InvalidGroupID:
        return False


def add_group(group_id):
    group, created = Group.objects.get_or_create(group_id=group_id)
    if created:
        try:
            _update_group(group)
        except DataFailureException:
            # TODO: do something here since a missing group is bad
            pass


def update_groups():
    groups_to_update = Group.objects.all()
    for group in groups_to_update:
        try:
            _update_group(group)
        except DataFailureException:
            # TODO: do something here since a missing group is bad
            pass

    _remove_orphaned_people()


def _remove_orphaned_people():
    people_ids_in_group = GroupMembership.objects.all()\
        .values_list('id', flat=True)
    distinct_ids = []
    for person_id in people_ids_in_group:
        if person_id not in distinct_ids:
            distinct_ids.append(person_id)
    Person.objects.exclude(id__in=distinct_ids).delete()


def _update_group(group):
    # Create person models for newly seen people
    remote_members = get_members(group.group_id)
    remote_people = []
    for member in remote_members:
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
