from django.test import TestCase
from django.test.utils import override_settings

DAO = "spotseeker_restclient.dao_implementation.spotseeker.File"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class ScoutTest(TestCase):
    pass
