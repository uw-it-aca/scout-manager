"""
A simple functional headless UI test with pyvirtualdisplay and selenium
"""

import os
import sys

from selenium import webdriver
from django.test import LiveServerTestCase
from django.conf import settings

USERNAME = getattr(settings, 'SAUCE_USERNAME', False)
ACCESS_KEY = getattr(settings, 'SAUCE_ACCESS_KEY', False)

from sauceclient import SauceClient
sauce_client = SauceClient(USERNAME, ACCESS_KEY)

class PageFlowTest(LiveServerTestCase):

    baseurl = 'http://localhost:8001/'

    def setUp(self):

        self.desired_cap = {
            'platform': "Mac OS X 10.9",
            'browserName': "chrome",
            'version': "31",
            'tags': ["Pageflow", "Royce"] 
        }

        self.driver = webdriver.Remote(
            command_executor='http://'+USERNAME+':'+ACCESS_KEY+'@ondemand.saucelabs.com:80/wd/hub',
            desired_capabilities=self.desired_cap)

        self.driver.implicitly_wait(10)

    #Method to test clicks
    def clickOnLink(self, link):
        self.driver.find_element_by_partial_link(link).click()

    # Sees if the manager app is reachable by URL
    # tests to see if filter url is navigable
    def test_URL(self):

        sauce_client.jobs.update_job(self.driver.session_id, name="Pageflow: URL")

        #Goes to http://localhost:8001/manager/, which is homepage
        self.driver.get(se.fbaseurl + 'manager/')
        test = self.driver.find_element_by_class_name('intro_text')
        self.assertEqual(test.text,"This is the app home. It has your list of spaces and items that you manage.")

        #Should redirect to http://localhost:8001/manager
        #If not, should be a problem
        self.driver.get(self.baseurl + 'manager')
        test = self.driver.find_element_by_class_name('intro_text')
        self.assertEqual(test.text,"This is the app home. It has your list of spaces and items that you manage.")


    # See if you can flow from homepage of Space List to Edit Space
    def test_homepage_to_add(self):

        sauce_client.jobs.update_job(self.driver.session_id, name="Pageflow: Space List to Add Item")

        #Goes to manager homepage and clicks on "Add New Space"
        self.driver.get(self.baseurl + 'manager/')
        self.clickOnLink("/manager/add/")

    # See if you can flow from homepage of Space List to Edit Space
    def test_homepage_to_add(self):

        sauce_client.jobs.update_job(self.driver.session_id, name="Pageflow: Space List to Edit Space")

        #Goes to manager homepage and clicks on "Add New Space"
        self.driver.get(self.baseurl + 'manager/')
        self.clickOnLink("/manager/add/space")



    def tearDown(self):
        print("https://saucelabs.com/jobs/%s \n" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce_client.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce_client.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()
 

//////////////


    #New test cases to be written
        # User able to see home page when entering in <url:port> (url for FoodScout) to the web browser.
        # User can use 'ALL FOOD' to search for a place to eat on campus
        # User can use 'DISCOVER' to view places to eat on campus
        # User can use 'FILTER' to search for a place to eat on campus
        # User can navigate to the Space Details page for specific spots via the "DISCOVER" page
        # Get directions to a selected food establishment
        # Search for space by pins on map under "ALL FOOD"

    #This tests, I'm not sure.. But it was initally there when Char passed it on to Royce
    #def test_sauce(self):
    #   print("hello")
    #   self.driver.get('http://curry.aca.uw.edu:8001/filter/')
    #   test = self.driver.find_element_by_id('test')
    #   self.assertEqual(test.text,"Hello World!")

    #The old test cases archieved. These were here before Char gave them to Royce
        # User can browse all spaces on campus for a place to eat without knowing anything about the space - https://jira.cac.washington.edu/browse/SCOUT-1
        # User can search for a place to eat on campus by entering the name of the place as a search filter - https://jira.cac.washington.edu/browse/SCOUT-2
        # User can find a place to eat on campus by viewing pins on a map which represent spots that meet the criteria of "open now" and are either near the
            #user's current location or are centered around a central point on campus. https://jira.cac.washington.edu/browse/SCOUT-4
        # User can find a place to eat by searching for places that are 'open specific hours' https://jira.cac.washington.edu/browse/SCOUT-5
        # User can bring up a list of the most popular places to eat by clicking on a link in the app https://jira.cac.washington.edu/browse/SCOUT-6
        # User can bring up a list of the places that serve coffee based on their current location by clicking a link https://jira.cac.washington.edu/browse/SCOUT-7
        # User can bring up a list of places that serve breakfast by clicking a link in the app
