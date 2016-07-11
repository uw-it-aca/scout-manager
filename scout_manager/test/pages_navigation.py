"""
Cases to test navigation from page to page
"""
from bs4 import BeautifulSoup
from scout_manager.test import ScoutTest

baseUrl = '/manager/'

urls = {
    'home': baseUrl,
    'study': baseUrl + 'spaces/',
    'food': baseUrl + 'spaces/?app_type=food',
    'add': baseUrl + 'spaces/add/',
    'edit': baseUrl + 'spaces/1/'
}

_testCases = {
    'home': ('study', 'food', 'add'),
    'food': ('edit', 'study', 'add'),
    'add': ('home', 'food', 'study'),
    'study': ('home', 'food', 'add'),
    'edit': ('home', 'food', 'study'),
}

def _makeTestFunc(start, end):
    """Returns a function that tests the navigation between two pages"""

    def _testFunc(self):
        page = self.makeSoup(urls[start])
        self.assertTrue(self.checkLinkExists(page, urls[end]))

    _testFunc.__name__ = 'test_%s_to_%s' %(start, end)
    _testFunc.__doc__ = 'Assert that %s has a link to %s' %(start, end)
    return _testFunc

class NavigationTests(ScoutTest):

    @classmethod
    def setUpClass(cls):
        super(NavigationTests, cls).setUpClass()
        cls.soups = {}

    for start, ends in _testCases.items():
        for end in ends:
            testFunc = _makeTestFunc(start, end)
            name = testFunc.__name__
            vars()[name] = testFunc

    del start, ends, end, testFunc, name

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

    # Test methods (from one page to another)
    '''
    def test_main_page_to_add(self):
        """Assert that main page has a link to add page"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, addUrl))

    def test_main_page_to_food(self):
        """Assert that main page has a link to a list of food spaces"""
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, foodUrl))

    def test_main_page_to_study(self):
        """ Assert that main page has a link to a list of study spaces """
        page = self.makeSoup(baseUrl)
        self.assertTrue(self.checkLinkExists(page, studyUrl))

    def test_food_page_to_space(self):
        """Assert that food page has a link to edit space page"""
        page = self.makeSoup(foodUrl)
        self.assertTrue(self.checkLinkExists(page, editUrl))

    def test_food_page_to_study_page(self):
        """Assert that food page has a link to study spaces page"""
        page = self.makeSoup(foodUrl)
        self.assertTrue(self.checkLinkExists(page, studyUrl))

    def test_food_page_to_add(self):
        """Assert that food page has a link to add space page"""
        page = self.makeSoup(foodUrl)
        self.assertTrue(self.checkLinkExists(page, addUrl))

    def test_add_page_to_main(self):
        """Assert that the add page has a link to main page"""
        page = self.makeSoup(addUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def test_add_page_to_food_page(self):
        """Assert that the add page has a link to food page"""
        page = self.makeSoup(addUrl)
        self.assertTrue(self.checkLinkExists(page, foodUrl))

    def test_add_page_to_study_page(self):
        """Assert that the add page has a link to study page"""
        page = self.makeSoup(addUrl)
        self.assertTrue(self.checkLinkExists(page, studyUrl))

    def test_study_page_to_main(self):
        """Assert that the add page has a link to main page"""
        page = self.makeSoup(studyUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def test_study_page_to_food_page(self):
        """Assert that the add page has a link to food page"""
        page = self.makeSoup(studyUrl)
        self.assertTrue(self.checkLinkExists(page, foodUrl))

    def test_study_page_to_add_page(self):
        """Assert that the add page has a link to add page"""
        page = self.makeSoup(studyUrl)
        self.assertTrue(self.checkLinkExists(page, addUrl))

    def test_edit_page_to_main(self):
        """Assert that the edit page has a link to main page"""
        page = self.makeSoup(editUrl)
        self.assertTrue(self.checkLinkExists(page, baseUrl))

    def test_edit_page_to_food_page(self):
        """Assert that the edit page has a link to food page"""
        page = self.makeSoup(editUrl)
        self.assertTrue(self.checkLinkExists(page, foodUrl))

    def test_edit_page_to_study_page(self):
        """Assert that the edit page has a link to study page"""
        page = self.makeSoup(editUrl)
        self.assertTrue(self.checkLinkExists(page, studyUrl))

    # Following tests look at the footer links

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
        self.check_footer_links(addUrl)

    def test_food_page_footer_links(self):
        """Assert that the food page has footer links"""
        self.check_footer_links(foodUrl)

    def test_study_page_footer_links(self):
        """Assert that the space page has footer links"""
        self.check_footer_links(studyUrl)

    def test_edit_page_footer_links(self):
        """Assert that the edit page has footer links"""
        self.check_footer_links(editUrl)
        '''

