# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Use a list of URLs and expected status codes to ensure every page
returns the expected code.
"""

from django.conf import settings
from django.contrib.auth.models import User
from scout_manager.test import ScoutTest

baseUrl = "/manager"

OK = 200
redir = 301
notfound = 404

_testCases = (
    # ('Home', '/', OK, 'SCOUT-122'),
    # ('Home redir', '', redir, 'SCOUT-129'),
    ("Items", "/items/", OK, "SCOUT-122"),
    ("Items redir", "/items", redir, "SCOUT-129"),
    ("Items add", "/items/add/", OK, "SCOUT-122"),
    ("Items add redir", "/items/add", redir, "SCOUT-129"),
    ("Item specific", "/items/5555/", OK, "SCOUT-122"),
    ("Spaces", "/spaces/", OK, "SCOUT-122"),
    ("Spaces redir", "/spaces", redir, "SCOUT-122"),
    ("Spaces add", "/spaces/add/", OK, "SCOUT-122"),
    ("Spaces add redir", "/spaces/add", redir, "SCOUT-129"),
    ("Spaces specific", "/spaces/2/", OK, "SCOUT-122"),
    ("Spaces specific nonexistant", "/spaces/0/", notfound),
    ("Spaces specific redir", "/spaces/5070", redir, "SCOUT-129"),
    ("Bad url", "/rando/", notfound),
)


def _makeTestFunc(name, path, status=OK, issue=None):
    """Returns a function that tests given URL using assertUrlStatus"""

    def _testFunc(self):
        self.assertUrlStatus(status, path)

    # Makes a test function, with the page passed as the name.
    _testFunc.__name__ = "test_page_" + name.replace(" ", "_").lower()

    # Makes a help comment about the url status
    doc = 'Assert "%s" results in a %s' % (path, status)

    # Connects the help comment with an issue number in JIRA
    if issue is not None:
        doc += " (%s)" % issue
    _testFunc.__doc__ = doc

    return _testFunc


class urlStatusCheck(ScoutTest):
    """Use a list of URLs and expected status codes to ensure every
    page returns the expected code."""

    def setUp(self):
        self.user = User.objects.create(username="javerage")
        self.user.save()

        self.client.force_login(user=self.user)
        session = self.client.session
        session["samlUserdata"] = {
            "isMemberOf": [settings.SCOUT_MANAGER_ACCESS_GROUP]
        }
        session.save()

    def tearDown(self):
        self.user.delete()

    def _clientUrlStatus(self, urlsuffix=""):
        """Return response code of given URL, or 500 if failed"""
        response = self.client.get(baseUrl + urlsuffix, REMOTE_USER="javerage")
        return response.status_code

    def assertUrlStatus(self, code, urlsuffix=""):
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
