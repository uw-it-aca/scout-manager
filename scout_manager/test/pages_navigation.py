"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from django.test import TestCase
from django.test.utils import override_settings

baseUrl = '/manager/spaces/'
DAO = "spotseeker_restclient.dao_implementation.spotseeker.File"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class NavigationTests(TestCase):

    ####################Start helper methods####################
    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, "html.parser")
        return soup

    def checkLinkExists(self, soup, reference):
        return bool(soup.find('a', href=reference))
    ####################End helper methods#######################

    #Main page to edit space and add space
    def test_mainPage(self):
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl + 'add/'))
        self.assertTrue(self.checkLinkExists(page, baseUrl +'1/'))

    #Main page to email help
    def test_mainEmail(self):
        page = self.makeSoup('/manager/')
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    #Add page to home
    def test_addPage(self):
        page = self.makeSoup(baseUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, '/manager/'))

    #Edit page to home
    def test_editPage(self):
        page = self.makeSoup(baseUrl + '1/')
        self.assertTrue(self.checkLinkExists(page, '/manager/'))
    #CURRENTLY DOESN'T WORK CAUSE no attribute 'get_building_list'  