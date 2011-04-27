import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify, rest

from fickileaks.lib.base import BaseController, render
from fickileaks.model import User

from string import ascii_letters, digits

log = logging.getLogger(__name__)

class UsersController(BaseController):

    # Only GET method is allowed here.
    @rest.restrict('GET')
    @jsonify
    def autocomplete(self):
        # Ensure term parameter is passed.
        if 'term' not in request.params:
            abort(400, 'Request did not contain term parameter.')

        term = request.params['term']

        # Ensure term parameter is in ASCII.
        try:
            term.decode('ascii')
        except UnicodeEncodeError:
            abort(400, 'Term parameter must only contain ASCII characters.')

        # Ensure term parameter only contains email legal characters.
        legalchars = list(ascii_letters) + list(digits) + \
            list("!#$%&'*+-/=?^_`{|}~.@")
        illegalchars = set(term) - set(legalchars)
        if illegalchars:
            abort(400, 'Characters not legal in email address: %s' % ''.join(illegalchars))

        # This uses ilike() to avoid capitalization issues.
        users = User.query.filter(User.email.ilike('%' + term + '%')).all()
        return [u.email for u in users]
