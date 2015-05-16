from django.db import models
from django.conf import settings

from twitter import OAuth, Twitter

from controlpanel.models import Context


class Account(models.Model):
    username = models.CharField(max_length=15)
    key = models.CharField(max_length=128)
    secret = models.CharField(max_length=128)
    active = models.BooleanField(default=False)

    @classmethod
    def active_account(kls):
        return kls.objects.filter(active=True)[0]

    def recent_tweets(self):
        return self.get_twitter_handle().statuses.user_timeline(screen_name=self.username)

    def tweet_with_context(self, text):
        context = Context.current()
        expanded = text.replace('%context', context.text)
        self.tweet(expanded)

    def tweet(self, text):
        self.get_twitter_handle().statuses.update(status=text)

    def get_twitter_handle(self):
        return Twitter(
            auth=OAuth(
                self.key,
                self.secret,
                settings.TWITTER_TOKEN,
                settings.TWITTER_SECRET
            )
        )

    def __unicode__(self):
        return self.username
