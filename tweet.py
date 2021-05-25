#!/usr/bin/env python
#
# To use, save this as tweet.py, then:
#
# mkvirtualenv twitterauth
# pip install flask tweepy
# CONSUMER_KEY=XXX \
#    CONSUMER_SECRET=XXX \
#    CALLBACK_URL=http://localhost:5000/done \
#    FLASK_APP=tweet flask run

from flask import Flask, request
import os
import tweepy

app = Flask(__name__)

@app.route('/')
def send_for_auth():
    try:
        auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
            os.environ['CALLBACK_URL']
        )
        redirect_url = auth.get_authorization_url()
        return '<p><a href="%s">Auth on twitter</a></p>' % redirect_url
    except:
        return(
            '<p>Needs <code>CONSUMER_KEY</code>, '
              '<code>CONSUMER_SECRET</code>, '
              'and <code>CALLBACK_URL</code> environment values.'
            '</p>'
        )

@app.route('/done')
def got_auth():
    auth = tweepy.OAuthHandler(
        os.environ['CONSUMER_KEY'],
        os.environ['CONSUMER_SECRET'],
        os.environ['CALLBACK_URL']
    )

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    auth.request_token = {
        'oauth_token': oauth_token,
        'oauth_token_secret': oauth_verifier,
    }
    (access_token, access_token_secret) = auth.get_access_token(oauth_verifier)

    api = tweepy.API(auth)
    last_tweet = api.user_timeline()[0]
    return(
        '<p>Authenticated. Last tweet:</p>'
        '<blockquote>%s</blockquote>'
        '<p>Save these values:</p>'
        '<blockquote><pre>'
            'ACCESS_TOKEN=%s\n'
            'ACCESS_TOKEN_SECRET=%s\n'
        '</pre></blockquote>' % (
            last_tweet.text,
            access_token,
            access_token_secret
        )
    )
