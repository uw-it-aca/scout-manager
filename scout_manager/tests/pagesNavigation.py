"""
Cases to test navigation from page to page
"""
import unittest
import urllib2

from bs4 import BeautifulSoup
from django.test import LiveServerTestCase
from django.test import Client

class NavigationTests(LiveServerTestCase):
    client = Client()

####################Start helper methods####################
    def makeSoup(self, link):
        webResponse = urllib2.urlopen(link).read()
        soup = BeautifulSoup(webResponse)
        return soup;

    def checkLinkExists(self, soup, reference):
        for link in soup.find_all('a'):
            linkCheck = link.get('href')
            if (linkCheck == reference):
                return True 
            else
                return False
            
####################End helper methods#######################

    #Main page to edit space and add space
    def test_mainPage(self):
        page = self.makeSoup('/')
        linkFound1 = self.checkLinkExists(page, '/manager/space/')
        self.assertTrue(linkFound1)
        linkFound2 = self.checkLinkExists(page, '/scout/space/')
        self.assertTrue(linkFound1)

    #Edit Space to main page
    def test_editPage(self):
        page = self.makeSoup('/')
        linkFound1 = self.checkLinkExists(page, '/manager/')
        self.assertTrue(linkFound1)
        linkFound2 = self.checkLinkExists(page, '/')
        self.assertTrue(linkFound1)

    #Add Space to main page and edit page
    #def test_addPage(self):