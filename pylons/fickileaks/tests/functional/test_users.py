from fickileaks.tests import *

class TestUsersController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='users', action='index'))
        # Test response...
