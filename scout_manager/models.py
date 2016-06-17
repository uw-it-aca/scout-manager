from django.db import models


class Person(models.Model):
    netid = models.CharField(max_length=40)
    added_on = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    group_id = models.CharField(max_length=500)
    added_on = models.DateTimeField(auto_now_add=True)


class GroupMembership(models.Model):
    group = models.ForeignKey('Group')
    person = models.ForeignKey('Person')
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
