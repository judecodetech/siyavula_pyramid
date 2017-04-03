"""
Test all views and functions
"""
import unittest

from pyramid import testing

VALID_URL = 'https://en.wikipedia.org/wiki/Software_development'
INVALID_URL = 'https://docs.python.org/3/reference/simple_stmts.html'


class ViewTests(unittest.TestCase):
    """
    Views tests
    """

    def setUp(self):
        self.config = testing.setUp()

    def test_home(self):
        """
        Test home view
        """
        from .views import WikiViews
        request = testing.DummyRequest()
        wiki_view = WikiViews(request)
        info = wiki_view.home()
        self.assertEqual(info['project'], 'siyavula_pyramid')

    def test_content_valid_url(self):
        """
        Test content view with a valid url
        """
        from .views import WikiViews
        request = testing.DummyRequest()
        # add wiki url to post request
        request.POST = {'wiki_url': VALID_URL}
        # instantiate wiki view class
        wiki_view = WikiViews(request)
        info = wiki_view.content()
        self.assertTrue('toc' in info)

    def test_content_invalid_url(self):
        """
        Test content view with an invalid url
        """
        from .views import WikiViews
        request = testing.DummyRequest()
        request.POST = {'wiki_url': INVALID_URL}
        wiki_view = WikiViews(request)
        info = wiki_view.content()
        self.assertTrue('error_message' in info)


class FunctionalTests(unittest.TestCase):
    """
    Functional tests
    """
    def setUp(self):
        """
        Setup test app
        """
        from siyavula_pyramid import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        """
        Test root url
        """
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pyramid' in res.body)

    def test_content(self):
        """
        Test content url
        """
        res = self.testapp.get('/content', status=404)
        self.assertTrue(b'404 Not Found' in res.body)

    def test_get_toc_invalid(self):
        """
        Test get toc with invalid url
        """
        from .wiki_toc import get_toc
        toc = get_toc(wiki_url=INVALID_URL)
        self.assertTrue('error' in toc)

    def test_get_toc_valid(self):
        """
        Test get toc with valid url
        """
        from .wiki_toc import get_toc
        toc = get_toc(wiki_url=VALID_URL)
        self.assertTrue('1 Methodologies' in toc)

    def test_wiki_toc_isfloat_true(self):
        """
        Test if function isfloat returns
        true if a value is a float
        """
        from .wiki_toc import isfloat
        value = isfloat(value='40.22222')
        self.assertTrue(value is True)

    def test_wiki_toc_isfloat_false(self):
        """
        Test if function isfloat returns
        false if a value is not a float
        """
        from .wiki_toc import isfloat
        value = isfloat(value='test_float')
        self.assertTrue(value is False)
