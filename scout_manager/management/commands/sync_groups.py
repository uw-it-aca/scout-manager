from django.core.management.base import BaseCommand, CommandError
from scout_manager.dao.groups import get_members
from scout_manager.models import Group, Person, GroupMembership

class Command(BaseCommand):

    def handle(self, *args, **options):
        groups_to_update = Group.objects.all()
        for group in groups_to_update:
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

        # Removing orphaned people
        people_ids_in_group = GroupMembership.objects.all()\
            .values_list('id', flat=True)
        distinct_ids = []
        for id in people_ids_in_group:
            if id not in distinct_ids:
                distinct_ids.append(id)
        Person.objects.exclude(id__in=distinct_ids).delete()


