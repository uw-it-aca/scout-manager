"""
Use a list of URLs and expected status codes to ensure every page
returns the expected code.
"""

from django.test import TestCase

baseUrl = '/manager'

OK = 200
redir = 301
notfound = 404

_testCases = (
    ('Home', '/', OK),
    ('Home redir', '', redir),
    ('Items', '/items', redir),
    ('Items slash', '/items/', OK),
    ('Item specific', '/items/5555/', OK),
    ('Spaces', '/spaces/', OK),
    ('Spaces add', '/spaces/add/', OK),
    ('Spaces specific', '/spaces/1/', OK),
    ('Schedule', '/schedule/1', OK),
    ('Bad url', '/rando/', notfound)
)


def _makeTestFunc(name, path, status=OK, issue=None):
    """Returns a function that tests given URL using assertUrlStatus"""

    def _testFunc(self):
        self.assertUrlStatus(status, path)

    # Makes a test function, with the page passed as the name.
    _testFunc.__name__ = 'test_page_' + name.replace(' ', '_').lower()

    # Makes a help comment about the url status
    doc = 'Assert "%s" results in a %s' % (path, status)

    # Connects the help comment with an issue number in JIRA
    if issue is not None:
        doc += ' (%s)' % issue
    _testFunc.__doc__ = doc

    return _testFunc


class urlStatusCheck(TestCase):
    """Use a list of URLs and expected status codes to ensure every
        page returns the expected code."""
    
    def _clientUrlStatus(self, urlsuffix=''):
        """Return response code of given URL, or 500 if failed"""
        response = self.client.get(baseUrl + urlsuffix)
        return response.status_code

    def assertUrlStatus(self, code, urlsuffix=''):
        """Compares that baseUrl + urlsuffix returns the given status code"""
        self.assertEqual(self._clientUrlStatus(urlsuffix), code)

    # Runs all test cases
    for case in _testCases:
        # Takes all the arguments and make test functions
        _testFunc = _makeTestFunc(*case)
        # Sets the names for the test functions
        name = _testFunc.__name__
        vars()[name] = _testFunc
    
    # Deletes variables so they don't leak into help documentation
    del case, name, _testFunc
