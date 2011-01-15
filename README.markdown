Prerequisites
=============

Fickileaks requires [Pylons][1] and [Elixir][2]. On a Debian-based system you can get all of these by issuing the following command as root:

    apt-get install python-pylons python-elixir


Installation and Setup
======================

    paster setup-app development.ini
    paster serve --reload development.ini

Caution: Always set “debug = false” in configuration files for production sites and make sure your users do to.


[1]: http://pylonshq.com/

[2]: http://elixir.ematia.de/trac/wiki
