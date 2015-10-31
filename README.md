Roots
=====

[![Travis build status](https://travis-ci.org/tbabej/roots.svg?branch=master)](https://travis-ci.org/tbabej/roots)
[![Coverage Status](https://coveralls.io/repos/tbabej/roots/badge.svg?branch=master)](https://coveralls.io/r/tbabej/roots?branch=master)
[![Code Health](https://landscape.io/github/tbabej/roots/master/landscape.svg?style=flat)](https://landscape.io/github/tbabej/roots/master)
[![Chat with developers](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/tbabej/roots)

![Roots project](https://raw.githubusercontent.com/tbabej/roots/master/base/static/logo.png  "Roots project")

Roots is a community-based site framework for seminar communities.

Example of live production site is available at: [STROM website](https://seminar.strom.sk/)

Unfortunately, only public parts of the website are available.

Motivation
----------

Many educational seminar communities exist (see [this list for only those in Czech and Slovak republic](http://cs.wikipedia.org/wiki/Koresponden%C4%8Dn%C3%AD_semin%C3%A1%C5%99#P.C5.99ehled_semin.C3.A1.C5.99.C5.AF_v.C4.8Detn.C4.9B_t.C3.A9mat) ), and often each of them provides their own web portal for managing all the work and information that needs to be stored with varying degree of success.

Users, problem statements, solutions, submissions, leaderboards, evaluation, keeping the competitors up to date - all of that requires non-trivial effort to implement in the web interface.

Roots is being built with the purpose of being an universal solution for correspondence seminars communities, while at the same time it keeps flexibility as one of the key requirements.

Technologies
------------

Standing on the shoulders of giants, build on Django.

Install
-------

### Using Vagrant

A quickest platform independent way to try out (or develop) Roots is using
Vagrant.

    $ git clone git://git.github.com/tbabej/roots.git         # clone the repository
    $ cd roots
    $ vagrant up

Vagrant will bring the development machine up, and configure development
enviroment for you. To start your Roots instance, you simply:

    $ vagrant ssh
    $ cd roots
    $ python manage.py runserver 0.0.0.0:8080

Roots instance from within the Vagrant VM will be forwarded
to http://localhost:8080.

It will be initialized with a small set of sample data (competition, season,
series, problemset). The default admin user has username 'admin' and password
'admin'.

### Local setup

Another recommended approach for trying Roots out is to use virtualenv,
since Roots has a lot of version-fixed dependencies:

    $ virtualenv rootsenv
    $ source rootsenv/bin/activate

After that, setup itself is just running few commands:

    $ git clone git://git.github.com/tbabej/roots.git         # clone the repository
    $ cd roots
    $ pip install -r requirements.txt                         # install the dependencies
    $ cp roots/local_settings.py.in roots/local_settings.py   # setup default local settings
    $ cp -r templates_custom.in templates_custom              # setup default custom templates
    $ python manage.py syncdb --noinput                       # setup the database
    $ python manage.py migrate                                # apply the migrations

Now, the Roots should be ready to go. There are two more steps you'd probably want to do:

    $ python manage.py createsuperuser                        # setup admin account
    $ python manage.py runserver

After that, a empty Roots site should run just fine!


Main feature list (non-technical and non-exhaustive)
----------------------------------------------------

* Management of users
  * Both participants and organizers
  * Allows regular registrations and social logins
* Management of correspondence competition
  * Handling of seasons and series of problems
  * Electronic user problem submission
  * Dynamic leaderboards
* Posts and static pages
  * Organizers are allowed to post new information (in blog style), in WYSIWYG editors
  * Support for static pages available
* Sophisticated problem database for organizers
  * Problems sorted into problemset, with various categories, severities, rankings, as well as usage stats available
* Leaflet management
* Camp management (as a reward for best competitors)
* Other events registration management
* Full site LaTex support
* Built-in wiki for organizers

Adoption
--------

I'm happy to help any correspondence seminar which wants to try Roots as a basis for their new site. Any feedback is welcome. Please submit issues, or send me a email (address can be found in the commits).

I'm also looking for help coming from fellow developers, please reach out to me via pull requests for contributions or plain old email for any help you might need.

Attribution
-----------

Roots project logo based on the [green engineering icon](http://thenounproject.com/term/green-engineering/12323/) by The Noun Project, which was relesed under public domain.
