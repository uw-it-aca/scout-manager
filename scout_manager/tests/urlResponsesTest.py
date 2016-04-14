"""
A simple test using python for loading urls
"""
import unittest

from django.test import LiveServerTestCase
from django.test import Client

class urlStatusCheck(LiveServerTestCase):

    def setUp(self):
        client = Client()

    ####################Start helper methods####################

    #Method to test clicks
    def clickOnLink(self, link):
        self.driver.find_element_by_partial_link(link).click()

    #Makes driver go to the given URL
    def go_url(self, urlsuffix=''):
        self.driver.get(self.baseurl + urlsuffix)

    #Returns the status code of the given URL
    def urlStatus(self, urlsuffix=''):
        #Issues a GET request
        response = self.client.get(urlsuffix)
        return response.status_code

    #Checks to see if the status code of the given URL matches
    #   the given status code
    def matchUrlStatus(self, code, urlsuffix=''):
        self.assertEqual(self.urlStatus(urlsuffix), code)   

    ####################End helper methods####################

    #Checks to see if the home manager page (/manager/) results in a 200 
    def test_home_exists(self):
        self.matchUrlStatus(200, '/')
    
    #Checks to see if the items pages (/items/) results in a 200
    def test_addPage(self):
        self.matchUrlStatus(200, '/items/')
        self.matchUrlStatus(200, '/items/5555/')
        self.matchUrlStatus(200, '/items/add')


    #Checks to see if the spaces page results in a 200
    def test_publishPage(self):
        self.matchUrlStatus(200, '/spaces/')
        #self.matchUrlStatus(200, '/spaces/x/') Not sure what to put in for x
            #Ask what does r'^spaces/(?P<spot_id>[0-9]{1,5}) means in urls.py
        self.matchUrlStatus(200, '/spaces/add/')

    #Checks to see if the schedule page results in a 200
    #def test_spacePage(self):
    #    self.matchUrlStatus(200, '/schedule/')
            #Ask what does r'^spaces/(?P<spot_id>[0-9]{1,5}) means in urls.py
            
    #Checks to see if entering an invalid URL results in a 404
    def test_badURL(self):
        self.matchUrlStatus(404, '/rando/' )

