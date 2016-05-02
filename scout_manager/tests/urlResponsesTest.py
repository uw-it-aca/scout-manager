"""
A simple test using python for loading urls
"""

from django.test import TestCase

baseUrl = '/manager'

class urlStatusCheck(TestCase):

    ####################Start helper methods####################

    #Returns the status code of the given URL
    def urlStatus(self, urlsuffix=''):
        #Issues a GET request
        response = self.client.get(baseUrl + urlsuffix)
        return response.status_code

    #Checks to see if the status code of the given URL matches
    #   the given status code
    def matchUrlStatus(self, code, urlsuffix=''):
        self.assertEqual(self.urlStatus(urlsuffix), code)   

    ####################End helper methods####################

    #Checks to see if the home manager page (/manager/) results in a 200 
    def test_home_exists(self):
        self.matchUrlStatus(200, '/')
    
    #Checks to see if the items pages (/items/) results in a 200
    def test_addPage(self):
        self.matchUrlStatus(200, '/items/')
        self.matchUrlStatus(200, '/items/5555/')


    #Checks to see if the spaces page (/spaces/results in a 200
    def test_publishPage(self):
        self.matchUrlStatus(200, '/spaces/')
        self.matchUrlStatus(200, '/spaces/add/')
<<<<<<< HEAD
        #CURRENTLY DOESN'T WORK CAUSE no attribute 'get_building_list'
        self.matchUrlStatus(200, '/spaces/1/')
=======
        self.matchUrlStatus(200, '/spaces/1/') #This one is causing a problem
>>>>>>> story/admin-01

    #Checks to see if the schedule works
    def test_spacePage(self):
        self.matchUrlStatus(200, '/schedule/1')
            
    #Checks to see if entering an invalid URL results in a 404
    def test_badURL(self):
        self.matchUrlStatus(404, '/rando/' )

