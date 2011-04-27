import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController, render

log = logging.getLogger(__name__)

class UsersController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/users.mako')
        # or, return a response
        return 'Hello World'
