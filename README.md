Roots
=====

[![Travis build status](https://travis-ci.org/tbabej/roots.svg?branch=master)](https://travis-ci.org/tbabej/roots)
[![Coverage Status](https://coveralls.io/repos/tbabej/roots/badge.svg?branch=master)](https://coveralls.io/r/tbabej/roots?branch=master)
[![Code Health](https://landscape.io/github/tbabej/roots/master/landscape.svg?style=flat)](https://landscape.io/github/tbabej/roots/master)

![Roots project](https://raw.githubusercontent.com/tbabej/roots/master/base/static/logo.png  "Roots project")

Roots is a community-based site framework for seminar communities.

Motivation
----------

Many educational seminar communities exist, and often each of them provides their own solution for managing all the work and information that needs to be stored with varying degree of success.

Roots is being built with the purpose of being an universal solution.


Feature list (non-technical)
---------------------------

 - Sign up and sign in both iusing Gmail and Facebook
   - Also support for ordinary registration
 - Support both for staff and user accounts
   - Support for user groups, permissions
   - User and staff profiles
 - Event and Camp management
   - Support for online signup for events
 - Post publication, LaTeX support in posts
   - Posts are written in MS-Word like environment
 - Leaflet publication
 - Photo gallery management
   - With watermark support
 - Sotisphicated problem database support
   - Rating, comments, generation of problem sets
   - Last event usages, number of usages shown
   - Categories
 - Built-in wiki for staff


Technologies
------------

Built on Django.

Contribute
----------

You are welcome to fork and submit your pull requests. Here's simple guide:

* Clone the roots repository:
    > git clone git://git.github.com/tbabej/roots.git

* Install django
  - On Fedora-based systems:
    sudo yum install python-django
  - With pip enabled:
    sudo pip install django
  - On Windows or other Linux systems(simple manual install):
    https://docs.djangoproject.com/en/dev/topics/install/#installing-an-official-release-manually

* Install django apps that roots depends on. Most of these can be installed using one
  command. However, here we provide links to official documentation, so look it up there.

  - Install south (http://south.readthedocs.org/en/latest/installation.html)
  - Install allauth (https://github.com/pennersr/django-allauth)
  - Install django-extensions (https://github.com/django-extensions/django-extensions)
    For this one you need to have pygraphviz python library installed and working.
    This can be done easily using easy_install pygraphviz.  Make sure you have Graphviz
    installed (www.graphviz.org). On Fedora-based systems: sudo yum install graphviz-devel -y

* Create your own local_settings.py file using local_settings.py.in as a template.
  Follow the instructions in the template file.in

* Create database tables, when prompted, create superuser account
    > python manage.py syncdb

* Run the development webserver
    > python manage.py runserver

* Test settings by logging into admin site with created superuser account
    > http://127.0.0.1/admin

* Have fun and play :)

Coding style
------------

We use relaxed version of the PEP8 standart:
* PEP8 erros E121 - E128 are ignored
* lines can be up to 80 characters long

You can check it using the following command:
> pep8 . --exclude=migrations --ignore=E121,E122,E123,E124,E125,E126,E127,E128 | grep -v '80 > 79'


Requirements
------------

Make sure you have basic packages installed:

    > sudo yum install git gcc -y

For compilation of the python packages, you will also need:

    > sudo yum install python-devel ImageMagick-devel -y

Install the following python packages:
    > pip install django wiki django-mathjax django-debug-toolbar django-photologue django-reversion django-author django-ratings django-extensions django-allauth django-grappelli Wand 


Useful tips
-----------

* Models used by the roots app can be visualized using django-extensions app.

  The following command should provide you with nice diagram:

  > python manage.py graph_models -age -o models.png


Attribution
-----------

Roots project logo based on the green engineering icon (http://thenounproject.com/term/green-engineering/12323/), which was relesed under public domain.
