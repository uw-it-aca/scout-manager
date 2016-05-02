#!/usr/bin/python
"""
Tests the content of all pages to make sure everything that needs
to be there is there.
"""
import re
from bs4 import BeautifulSoup
from django.test import TestCase

baseUrl = '/manager/spaces/'

class ContentTest(TestCase):
    
    ####################Start helper methods####################

    def makeSoup(self, link):
        webResponse = self.client.get(link)
        soup = BeautifulSoup(webResponse.content, "html.parser")
        return soup

    def checkLinkExists(self, soup, reference):
        return bool(soup.find('a', href=reference))

    ####################End helper methods#######################
    def test_homePage(self):
        page = self.makeSoup(baseUrl)
        spaces = page.findAll('li')
        for space in spaces:
            checkEdit = space.find('a', href=re.compile('^/manager/spaces/[0-9]*/$'))
            text = space.text
            self.assertIsNotNone(checkEdit)
            requiredStrings = [
                'Name:', 
                'Image:',
                'Campus:'
            ]
            for s in requiredStrings:
                self.assertIn(s, text)


        

        #for space in spaces:
        #    linkCheck = link.get('href')
        #    if (linkCheck == reference):
        #        return True 
        #    else
        #        return False
        #sef.assertGreater(len(), 0)
        #checkId = bs.select('#page_discover')
        #self.assertGreater(len(checkId), 0)
        