"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from django.test import TestCase
from django.test.utils import override_settings

baseUrl = '/manager/'
studyUrl = baseUrl + 'spaces/'
foodUrl = baseUrl + 'spaces/?app_type=food'
addUrl = baseUrl + 'spaces/add/'

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
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + 'add/'))

    def test_main_page_to_food(self):
        """Assert that main page has a link to a list of food spaces"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + '?app_type=food'))

    """
    This hasn't been implemented yet...
    def test_main_page_to_study(self):
        # Assert that main page has a link to a list of study spaces
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + '?app_type=spaces'))
    """

    def test_food_page_to_space(self):
        """Assert that food page has a link to edit space page"""
        page = self.makeSoup(baseSpaceUrl + "?app_type=food")
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + '1/'))

    def test_food_page_to_study_page(self):
        """Assert that food page has a link to study spaces page"""
        page = self.makeSoup(baseSpaceUrl + "?app_type=food")
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl))

    def test_food_page_to_add(self):
        """Assert that food page has a link to add space page"""
        page = self.makeSoup(baseSpaceUrl + "?app_type=food")
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + 'add/'))

    def test_add_page_to_main(self):
        """Assert that the add page has a link to main page"""
        page = self.makeSoup(baseSpaceUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def test_add_page_to_food_page(self):
        """Assert that the add page has a link to food page"""
        page = self.makeSoup(baseSpaceUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl + "?app_type=food"))

    def test_add_page_to_study_page(self):
        """Assert that the add page has a link to study page"""
        page = self.makeSoup(baseSpaceUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, baseSpaceUrl))

    def test_edit_page_to_main(self):
        """Assert that the edit page has a link to main page"""
        page = self.makeSoup(baseSpaceUrl + '1/')
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def check_footer_links(self, url):
        """Given a URL checks if the Privacy/Terms links are present"""
        page = self.makeSoup(url)
        self.assertTrue(self.checkLinkExists(page, 'http://www.washington.edu/online/privacy/'))
        self.assertTrue(self.checkLinkExists(page, 'http://www.washington.edu/online/terms/'))
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    def test_main_page_footer_links(self):
        """Assert that the main page has footer links"""
        self.check_footer_links(baseUrl)

    def test_add_page_footer_links(self):
        """Assert that the add page has footer links"""
        self.check_footer_links(baseSpaceUrl + 'add/')

    def test_food_page_footer_links(self):
        """Assert that the food page has footer links"""
        self.check_footer_links(baseSpaceUrl + '?app_type=food')

    def test_study_page_footer_links(self):
        """Assert that the space page has footer links"""
        self.check_footer_links(baseSpaceUrl)

    def test_edit_page_footer_links(self):
        """Assert that the edit page has footer links"""
        self.check_footer_links(baseSpaceUrl + '1/')

