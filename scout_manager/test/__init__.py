# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.test.utils import override_settings
from uw_spotseeker.dao import Spotseeker_DAO

DAO = "Mock"


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class ScoutTest(TestCase):
    pass
