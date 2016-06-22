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


class Group(models.Model):
    group_id = models.CharField(max_length=500, unique=True)
    added_on = models.DateTimeField(auto_now_add=True)


class GroupMembership(models.Model):
    group = models.ForeignKey('Group')
    person = models.ForeignKey('Person')
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = MembershipManager()
