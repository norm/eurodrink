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


## Twitter credentials

In order to tweet, we first need twitter credentials for the app and the user
to tweet as. Add the consumer key and secret obtained from
[Twitter](https://developer.twitter.com/en/apps) to the `.env` file:

    PYTHONUNBUFFERED=True
    CALLBACK_URL=http://localhost:5000/done
    CONSUMER_KEY=XXX
    CONSUMER_SECRET=XXX

Run the auth app, then visit [http://localhost:5000/](http://localhost:5000/):

    honcho start auth

Sign in with the Twitter account you want to use and authorize the app.
Add the two lines provided to the end of your `.env` file:

    ACCESS_TOKEN=XXX
    ACCESS_TOKEN_SECRET=XXX

You can now stop the auth app running.


## Refreshing the data

The database is not to be treated as the canonical source of data, it is just
used for the ease of using django to build pages and to work with twitter
during the contest itself.

    sh update.sh


## Using the admin interface

    honcho start web

To log into the admin interface, visit http://localhost:3876/ with the
username `norm` and password `norm`.

The admin navigation contains a link to the control panel that is used
to tweet the drinking game during the grand final.

## Website publication

    # preview on http://localhost:37465/
    honcho start static
    make static

    # copy when satisifed
    make static
    aws s3 sync site/. s3://eurovisiondrinking.com/.


## Running the drinking game

First, ensure this year's data is in `eurovision_data/`, even in draft. The
performances should have their data entered fully (artists, singers,
languages), and double-checked they are in the correct running order,
as this is relied upon for ease of navigating acts in the control panel.

    sh update.sh
    sh production.sh

The panel will present the first performance and all the possible incidents.
When the performance is over, click "Finished", that performance is marked
as having occurred, and the next will be presented.

Once all performances have finished, the panel will switch to the scoring
round incidents. A list of all participants is presented. As each score is
reported, click the country in question and the possible incidents will be
presented. Once that participant's scores have been announced, click
"Finished" and that participant is marked as having scored.

Once all participants have announced their scores, the panel will announce
that you are done.
