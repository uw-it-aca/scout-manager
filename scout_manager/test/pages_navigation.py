"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from django.test import TestCase
from django.test.utils import override_settings

baseUrl = '/manager/'
baseSpacesUrl = baseUrl + 'spaces/'
DAO = "spotseeker_restclient.dao_implementation.spotseeker.File"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class NavigationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(NavigationTests, cls).setUpClass()
        cls.soups = {}

    # Helper methods

    def makeSoup(self, link):
        if link in self.soups:
            return self.soups[link]
        else:
            webResponse = self.client.get(link)
            soup = BeautifulSoup(webResponse.content, 'html.parser')
            self.soups[link] = soup
            return soup

    def checkLinkExists(self, soup, reference):
        return bool(soup.find('a', href=reference))

    # Test methods

    def test_main_page_to_add(self):
        """Assert that main page has a link to add page"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseSpacesUrl + 'add/'))

    def test_main_page_to_food(self):
        """Assert that main page has a link to a list of food spaces"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseSpacesUrl + '?app_type=food'))

    """
    This hasn't been implemented yet...
    def test_main_page_to_study(self):
        # Assert that main page has a link to a list of study spaces
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseSpacesUrl + '?app_type=spaces'))
    """

    def test_food_page_to_space(self):
        """Assert that food page has a link to edit space page"""
        page = self.makeSoup(baseSpacesUrl + "?app_type=food")
        self.assertTrue(self.checkLinkExists(page, baseSpacesUrl + '1/'))

    def test_main_page_to_email(self):
        """Assert that the main page has a "help" email link"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    def test_add_page_to_main(self):
        """Assert that the add page has a link to main page"""
        page = self.makeSoup(baseSpacesUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def test_edit_page_to_main(self):
        """Assert that the edit page has a link to main page"""
        page = self.makeSoup(baseSpacesUrl + '1/')
        self.assertTrue(self.checkLinkExists(page, baseUrl))

