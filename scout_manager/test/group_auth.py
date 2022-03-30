# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.test.utils import override_settings
from scout_manager.models import GroupMembership, Group, Person
from scout_manager.dao.groups import update_groups, add_group
from uw_spotseeker.dao import Spotseeker_DAO
from uw_gws.dao import GWS_DAO


SS_DAO = "Mock"
GWS_DAO = "Mock"


@override_settings(
    SPOTSEEKER_DAO_CLASS=SS_DAO, RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO
)
class GroupAuthTest(TestCase):
    test_group = "u_acadev_tester"
    test_user = "javerage"

    def setUp(self):
        add_group(self.test_group)
        update_groups()

    def test_group_sync(self):
        group = Group.objects.get(group_id=self.test_group)
        self.assertEqual(group.group_id, self.test_group)
        javerage = Person.objects.get(netid=self.test_user)
        membership = GroupMembership.objects.filter(
            person=javerage, group_id=group
        )
        self.assertEqual(len(membership), 1)

    def test_is_provisioned(self):
        is_provisioned = Person.objects.is_provisioned(self.test_user)
        self.assertTrue(is_provisioned)
        not_provisioned = Person.objects.is_provisioned("notauser")
        self.assertFalse(not_provisioned)

    def test_is_member(self):
        is_member = GroupMembership.objects.is_member(
            self.test_user, self.test_group
        )
        self.assertTrue(is_member)
        not_user = GroupMembership.objects.is_member(
            "notauser", self.test_group
        )
        self.assertFalse(not_user)

        not_group = GroupMembership.objects.is_member(
            self.test_user, "u_notagroup"
        )
        self.assertFalse(not_group)

        Person.objects.create(netid="notingroup")
        not_member = GroupMembership.objects.is_member(
            "notingroup", self.test_group
        )
        self.assertFalse(not_member)
