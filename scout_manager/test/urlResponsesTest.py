"""
Use a list of URLs and expected status codes to ensure every page
returns the expected code.
"""

from django.test import TestCase

baseUrl = '/manager'

OK = 200
redir = 301
notfound = 404


class urlStatusCheck(TestCase):
    """
    Use a list of URLs and expected status codes to ensure every page
    returns the expected code.
    """

    expected = (
        ('home', '/', OK),
        ('home_redir', '', redir),
        ('items', '/items', OK),
        ('items_slash', '/items/', OK),
        ('item_specific', '/items/5555/', OK),
        ('spaces', '/spaces/', OK),
        ('spaces_add', '/spaces/add/', OK),
        ('spaces_specific', '/spaces/1/', OK),
        ('schedule', '/schedule/1', OK),
        ('bad_url', '/rando/', notfound)
    )

    def urlStatus(self, urlsuffix=''):
        """Return response code of given URL, or 500 if failed"""
        try:
            response = self.client.get(baseUrl + urlsuffix)
            return response.status_code
        except:
            return 500

    def assertUrlStatus(self, code, urlsuffix=''):
        """Assert that baseUrl + urlsuffix returns the given status code"""
        self.assertEqual(self.urlStatus(urlsuffix), code)

    def generateTestFunc(name, path, status):
        """Generate a test func that asserts 'path' returns 'status'."""
        def newfunc(self):
            self.assertUrlStatus(status, path)

        newfunc.__name__ = 'test_' + name

        return newfunc

    for name, path, status in expected:
        newfunc = generateTestFunc(name, path, status)
        vars()[newfunc.__name__] = newfunc
        del newfunc
