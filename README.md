Roots
=====

Roots is a community-based site framework for seminar communities.

Motivation
----------

Many educational seminar communities exist, and often each of them provides their own solution for man
Roots is being built with the purpose of being an universal solution.

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
    sudo yum install django
  - With pip enabled:
    pip install django
  - On Windows or other Linux systems(simple manual install):
    https://docs.djangoproject.com/en/dev/topics/install/#installing-an-official-release-manually

* Install django apps that roots depends on

  - Install south (http://south.readthedocs.org/en/latest/installation.html)
  - Install allauth (https://github.com/pennersr/django-allauth)

* Create your own local_settings.py file using local_settings.py.in as a template.
  Follow the instructions in the template file.in

* Create database tables, when prompted, create superuser account
    > python manage.py syncdb

* Run the development webserver
    > python manage.py runserver

* Test settings by logging into admin site with created superuser account
    > http://127.0.0.1/admin

* Have fun and play :)
