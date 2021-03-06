"""
Tests for the scout-manager groups DAO
"""
from django.test import TestCase
from scout_manager.dao import groups as groups_dao
from scout_manager.models import Group, GroupMembership, Person


class GroupDaoTest(TestCase):
    """ Tests the scout manager groups DAO methods.
    """

    def test_removed_orphan_people(self):
        # start with a higher id, so we have Person ids not in GroupMembership
        # ids. See SCOUT-728.
        Person.objects.create(id=2, netid='javerage')
        groups_dao.add_group('u_acadev_tester')
        before = []
        for person in Person.objects.all():
            before.append(person)

        # group membership did not change
        groups_dao._remove_orphaned_people()
        after = []
        for person in Person.objects.all():
            after.append(person)
        
        # Check that 'extra' was removed, but 'tbohn' was not.
        self.assertEqual(len(after), len(before))
        for person in before:
            self.assertIn(person, after)
