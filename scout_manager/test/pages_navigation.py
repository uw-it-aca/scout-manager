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


def _makeTestFooterFunc(start):
    """Given a URL checks if the Privacy/Terms links are present"""
    def _testFunc(self):
        page = self.makeSoup(urls[start])
        self.assertTrue(self.checkLinkExists(page, 'http://www.washington.edu/online/privacy/'))
        self.assertTrue(self.checkLinkExists(page, 'http://www.washington.edu/online/terms/'))
        self.assertTrue(self.checkLinkExists(page, 'mailto:help@uw.edu'))

    _testFunc.__name__ = 'test_%s_page_footer_links' %(start)
    _testFunc.__doc__ = 'Assert that footer links on the %s page exist' %(start)
    return _testFunc

class NavigationTests(ScoutTest):

    @classmethod
    def setUpClass(cls):
        super(NavigationTests, cls).setUpClass()
        cls.soups = {}

    for start, ends in _testCases.items():
        testFooterFunc = _makeTestFooterFunc(start)
        temp_name = testFooterFunc.__name__
        vars()[temp_name] = testFooterFunc
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

