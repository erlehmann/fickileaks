from fickileaks.tests import *

class TestRelationviewController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='relationview', action='index'))
        # Test response...
