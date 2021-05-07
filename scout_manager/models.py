# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class PersonManager(models.Manager):
    def is_provisioned(self, netid):
        return len(Person.objects.filter(netid=netid)) > 0


class MembershipManager(models.Manager):
    def is_member(self, person_id, group_id):
        try:
            person = Person.objects.get(netid=person_id)
            group = Group.objects.get(group_id=group_id)
            memberships = GroupMembership.objects.filter(group=group,
                                                         person=person)
        except ObjectDoesNotExist:
            return False
        return len(memberships) > 0


class Person(models.Model):
    netid = models.CharField(max_length=40, unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = PersonManager()

    def __unicode__(self):
        return "Person: {}".format(self.netid)


class Group(models.Model):
    group_id = models.CharField(max_length=255, unique=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Group: {}".format(self.group_id)


class GroupMembership(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = MembershipManager()

    def __unicode__(self):
        return "GroupMembership: {} - {}".format(self.group, self.person)
