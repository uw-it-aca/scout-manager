"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from django.test import TestCase

baseUrl = '/manager/spaces/'

class NavigationTests(TestCase):

    ####################Start helper methods####################
    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, "html.parser")
        return soup

    def checkLinkExists(self, soup, reference):
        self.assertElementExists(soup, 'a', href=reference)

    def assertElementExists(self, soup, *args, **kwargs):
        self.assertIsNotNone(soup.find(*args, **kwargs))
    ####################End helper methods#######################

    #Main page to edit space and add space
    def test_mainPage(self):
        page = self.makeSoup(baseUrl)
        self.checkLinkExists(page, baseUrl + 'add/')
        self.checkLinkExists(page, baseUrl +'1/')
        self.checkLinkExists(page, '/detail/1/')

    #Main page to email help
    def test_mainEmail(self):
        page = self.makeSoup('/manager/')
        self.checkLinkExists(page, 'mailto:help@uw.edu')

    #Add page to home
    def test_addPage(self):
        page = self.makeSoup(baseUrl + 'add/')
        self.checkLinkExists(page, '/manager/')
        self.assertElementExists(page, 'input', type='submit', value='Save Changes')
        self.assertElementExists(page, 'input', type='button', value='Cancel')

    #Edit page to home
    def test_editPage(self):
        page = self.makeSoup(baseUrl + '1/')
        self.assertElementExists(page, '/manager/') 