"""
Cases to test navigation from page to page
"""
import unittest
import urllib2

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test import Client

baseUrl = '/manager/'

class NavigationTests(LiveServerTestCase):

####################Start helper methods####################
    def makeSoup(self, link):
        webResponse = self.client.get(reverse('home'))
        soup = BeautifulSoup(webResponse.content, "html5lib")
        return soup

    def checkLinkExists(self, soup, reference):
        print soup
        print reverse('home')
        print reverse('spaces_add')
        for a in soup.findAll('a', href=reference):
            return True
        return False

            
####################End helper methods#######################

    #Main page to edit space and add space
    def test_mainPage(self):
        page = self.makeSoup(baseUrl)
        linkFound1 = self.checkLinkExists(page, reverse('spaces_add'))
        self.assertTrue(linkFound1)
        #linkFound2 = self.checkLinkExists(page, '/items/5555/')
        #self.assertTrue(linkFound3)
        #linkFound3 = self.checkLinkExists(page, '/')
        #self.assertTrue(linkFound3)
    
    """
    #Edit Space to main page
    def test_editPage(self):
        page = self.makeSoup(baseUrl)
        linkFound1 = self.checkLinkExists(page, '/manager/')
        self.assertTrue(linkFound1)
        linkFound2 = self.checkLinkExists(page, '/')
        self.assertTrue(linkFound1)

    #Add Space to main page and edit page
    #def test_addPage(self):
    """