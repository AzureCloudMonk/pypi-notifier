PyPI Notifier
=============

http://www.pypi-notifier.org

Watches your ``requirements.txt`` files and notifies you via email when
a project is updated.

Requirements
------------

Python 2.7 is required to run PyPI Notifier. Install the project dependencies
with::

    pip install -r requirements.txt

Configuration
-------------

Copy ``config.example.py`` as ``config.py`` and fill the values.

Running Web Server
------------------

Web server is run with `gevent <http://www.gevent.org/>`_.
There is a script for running the web server::

    ./run_gevent.py

Flask development server can be run with the following command::

    ./manage.py runserver

Running Backgrund Jobs
----------------------

There are 3 jobs that needed to be run periodically::

    ./manage.py update_repos     # Fetches requirements
    ./manage.py update_packages  # Checks latest versions from PyPI
    ./manage.py send_emails      # Notifies users about updates
