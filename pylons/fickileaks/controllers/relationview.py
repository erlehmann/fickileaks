import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController

log = logging.getLogger(__name__)

class RelationviewController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/relationview.mako')
        # or, return a response
        return 'Hello World'
