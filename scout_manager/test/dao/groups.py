# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Tests for the scout-manager groups DAO
"""
from django.test import TestCase
from django.test.utils import override_settings
from scout_manager.dao import groups as groups_dao
from scout_manager.models import Group, GroupMembership, Person
from uw_gws import GWS

DAO = 'Mock'


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class GroupDaoTest(TestCase):
    """Tests the scout manager groups DAO methods."""

    def test_removed_orphan_people(self):
        # start with a higher id, so we have Person ids not in GroupMembership
        # ids. See SCOUT-728.
        Person.objects.create(id=2, netid="javerage")
        groups_dao.add_group("u_acadev_tester")
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

    def test_is_provisioned_user(self):
        Person.objects.create(id=2, netid="javerage")
        self.assertTrue(groups_dao.is_provisioned_user("javerage"))
        self.assertFalse(groups_dao.is_provisioned_user("javerage1"))
        Person.objects.get(id=2).delete()

    @override_settings(MANAGER_SUPERUSER_GROUP='u_acadev_tester')
    def test_is_superuser(self):
        gws = GWS()
        Person.objects.create(id=2, netid="javerage")
        gws.add_members("u_acadev_tester", ["javerage"])
        self.assertTrue(groups_dao.is_superuser("javerage"))
        self.assertFalse(groups_dao.is_superuser("javerage1"))
        Person.objects.get(id=2).delete()
