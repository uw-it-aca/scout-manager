# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from uw_spotseeker.dao import Spotseeker_DAO

DAO = "Mock"


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class ScoutTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="javerage")
        self.user.save()

        self.client.force_login(user=self.user)
        session = self.client.session
        session["samlUserdata"] = {
            "isMemberOf": [settings.SCOUT_MANAGER_ACCESS_GROUP]
        }
        session.save()
