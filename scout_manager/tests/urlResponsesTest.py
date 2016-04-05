"""
A simple test using python for loading urls
"""

import sys
import unittest
import copy

from django.test import LiveServerTestCase
from django.test import Client
from django.conf import settings

class urlStatusCheck(LiveServerTestCase):

    def setUp(self):
        self.client = Client()

    ####################Start helper methods####################

    #Method to test clicks
    def clickOnLink(self, link):
        self.driver.find_element_by_partial_link(link).click()

    #Makes driver go to the given URL
    def go_url(self, urlsuffix=''):
        self.driver.get(self.baseurl + urlsuffix)

    #Returns the status code of the given URL
    def urlStatus(self, urlsuffix=''):
        statCode = self.client.get(urlsuffix)
        return statCode.status_code

    #Checks to see if the status code of the given URL matches
    #   the given status code
    def matchUrlStatus(self, code, urlsuffix=''):
        self.assertEqual(self.urlStatus(urlsuffix), code)   

    ####################End helper methods####################

    #Checks to see if the home page results in a 200 
    def test_home_exists(self):
        self.matchUrlStatus(200, '/')
    
    #Checks to see if the add page results in a 200
    def test_addPage(self):
        self.matchUrlStatus(200, '/add/')

    #Checks to see if the item page results in a 200
    def test_itemPage(self):
        self.matchUrlStatus(200, '/item/')

    #Checks to see if the publish page results in a 200
    def test_publishPage(self):
        self.matchUrlStatus(200, '/publish/')

    #Checks to see if the space page results in a 200
    def test_spacePage(self):
        self.matchUrlStatus(200, '/space/')

    #Checks to see if entering an invalid URL results in a 404
    def test_badURL(self):
        self.matchUrlStatus(404, '/rando/' )

