"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from django.test import TestCase

baseUrl = '/manager/spaces/'

class NavigationTests(TestCase):

    ####################Start helper methods####################
    #Parses through the html that we got from '/manager/spaces/'
        #and returns it as something readible
    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, "html.parser")
        return soup

    #Parses through the soup and finds all a tags w/ the href passed in
    def checkLinkExists(self, soup, reference):
        return bool(soup.find('a', href=reference))
    ####################End helper methods#######################

    #Main page to edit space and add space
    def test_mainPage(self):
        page = self.makeSoup(baseUrl)
        #Checks the add page
        self.assertTrue(self.checkLinkExists(page, baseUrl + 'add/'))
        #Checks the edit page of the first link
            #Check very bottom, 1
        self.assertTrue(self.checkLinkExists(page, baseUrl +'1/'))
        #Checks the detail page of the first link
        self.assertTrue(self.checkLinkExists(page, '/detail/1/'))

    #Main page to help email
    def test_mainEmail(self):
        page = self.makeSoup('/manager/')
        #Checks the mailing link
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    #Add page to home
    def test_addPage(self):
        page = self.makeSoup(baseUrl + 'add/')
        self.assertTrue(self.checkLinkExists(page, '/manager/'))

    #Edit page to home
        #Check very bottom, 1
    def test_editPage(self):
        page = self.makeSoup(baseUrl + '1/'))
        self.assertTrue(self.checkLinkExists(page, '/manager/'))
  
"""
Error Readings (ER):
        1.CURRENTLY DOESN'T WORK CAUSE AttributeError, 'Spotseeker' object
            no attribute 'get_building_list'
"""