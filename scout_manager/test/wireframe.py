# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Tests the content of all pages to make sure everything that needs
to be there is there.
"""

from bs4 import BeautifulSoup
from django.test import TestCase
from django.test.utils import override_settings
from uw_spotseeker import Spotseeker

baseUrl = "/manager/spaces/"
DAO = Spotseeker().get_implementation()


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class ContentTest(TestCase):

    #  Start helper methods
    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, "html.parser")
        return soup

    def checkLinkExists(self, soup, reference):
        return bool(soup.find("a", href=reference))
    #  End helper methods

    def test_homePage(self):
        page = self.makeSoup(baseUrl)
        spaces = page.findAll("li")
        for space in spaces:
            childCount = space.findAll("div")
            # print len(childCount)
            # self.assertEqual(childCount.len() == 13)

        # for space in spaces:
        #    linkCheck = link.get('href')
        #    if (linkCheck == reference):
        #        return True
        #    else
        #        return False
        # sef.assertGreater(len(), 0)
        # checkId = bs.select('#page_discover')
        # self.assertGreater(len(checkId), 0)
