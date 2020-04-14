from django.test import TestCase
from django.test.utils import override_settings
from uw_spotseeker.dao import Spotseeker_DAO

DAO = "Mock"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class ScoutTest(TestCase):
    pass
