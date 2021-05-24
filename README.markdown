eurodrink
=========

[@eurovisiondrink](https://twitter.com/eurovisiondrink) is a semi-automated
twitter account for those of us who enjoy drinking during the Eurovision Song
Contest. When certain incidents happen during the broadcast, a tweet is sent
explaining what has just happened and how much you should drink.

To speed up this tweeting, most of it happens from a control panel, so I can
get back to enjoying Eurovision as quickly as possible.

This repo is that control panel, and the source for the website
[http://eurovisiondrinking.com](http://eurovisiondrinking.com).


## Setting up

The control panel is normally used via a virtual environment.

    pip install virtualenvwrapper
    mkvirtualenv eurodrink
    pip install -r requirements.txt

## Refreshing the data

The database is not to be treated as the canonical source of data, it is just
used for the ease of using django to build pages and to work with twitter
during the contest itself.

    sh update.sh

## Using the admin interface

    honcho start web

To log into the admin interface, visit http://localhost:3876/ with the
username `norm` and password `norm`.
