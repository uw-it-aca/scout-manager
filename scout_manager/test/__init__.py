# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.test.utils import override_settings
from uw_spotseeker.dao import Spotseeker_DAO
from os.path import abspath, dirname
import os

DAO = "Mock"
spotseeker_paths = Spotseeker_DAO().service_mock_paths()


@override_settings(RESTCLIENTS_SPOTSEEKER_DAO_CLASS=DAO)
class ScoutTest(TestCase):
    def _get_manager_mock_path(self):
        manager_path = abspath(
            os.path.join(dirname(dirname(__file__)), "resources"))
        paths = spotseeker_paths + [manager_path]
        return paths

    Spotseeker_DAO.service_mock_paths = _get_manager_mock_path
