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

    # Helper methods

    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, 'html.parser')
        return soup

    def checkLinkExists(self, soup, reference):
        return bool(soup.find('a', href=reference))

    # Test methods

    def test_main_page_to_add(self):
        """Assert that main page has a link to add page"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl + 'add/'))

    def test_main_page_to_space(self):
        """Assert that main page has a link to a space page"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl + '1/'))

    def test_mainEmail(self):
        """Assert that the main page has a "help" email link"""
        page = self.makeSoup('/manager/')
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    def test_addPage(self):
        """Assert that the add page has a link to main page"""
        page = self.makeSoup(baseUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, '/manager/'))

    def test_editPage(self):
        """Assert that the edit page has a link to main page"""
        page = self.makeSoup(baseUrl + '1/')
        self.assertTrue(self.checkLinkExists(page, '/manager/'))
