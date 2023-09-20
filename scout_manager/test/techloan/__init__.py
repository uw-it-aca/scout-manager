# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS='Mock')
class TechloanTestCase(TestCase):
    pass
