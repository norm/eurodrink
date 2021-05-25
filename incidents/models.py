from datetime import date
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
import tweepy

from contests.models import Performance, Score, Show, Participant


class Penalty(models.TextChoices):
    ONE_FINGER = 'one-finger', _('One finger')
    TWO_FINGERS = 'two-fingers', _('Two fingers')
    DOWN = 'down', _('Down your drink')


class BaseIncidentType(models.Model):
    """
    An IncidentType is a specific type of event that can occur during a
    Contest that is flagged as a cause for taking a drink.
    """
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=230)
    tweet = models.CharField(max_length=230, blank=True, null=True)
    penalty = models.CharField(max_length=12, choices=Penalty.choices)

    def tweet_text(self):
        return self.tweet or self.description

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class BaseIncident(models.Model):
    """
    An Incident is an instance of an IncidentType that has happened.
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.should_tweet():
            self.tweet_incident()

    def should_tweet(self):
        return True

    def tweet_incident(self):
        args = [ self.get_incident_text(), ]
        context = self.get_context_hashtag()
        if context:
            args.append(context)
        args.append('#Eurovision')
        args.append('#esc%d' % date.today().year)
        self.send_tweet(' '.join(args))

    def send_tweet(self, text):
        auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
        )
        auth.set_access_token(
            os.environ['ACCESS_TOKEN'],
            os.environ['ACCESS_TOKEN_SECRET'],
        )
        api = tweepy.API(auth)
        api.update_status(text)

    class Meta:
        abstract = True


class PerformanceIncidentType(BaseIncidentType):
    """
    An IncidentType that can only occur during a Performance.
    """
    performances = models.ManyToManyField(
        Performance,
        through='PerformanceIncident',
        blank=True,
    )


class PerformanceIncident(BaseIncident):
    """
    An instance of a PerformanceIncidentType that has occurred
    during a specific Performance.
    """
    type = models.ForeignKey(
        PerformanceIncidentType,
        on_delete=models.CASCADE
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE
    )
    predicted = models.BooleanField(default=False)

    def should_tweet(self):
        return self.predicted == False and self.performance.occurred == False

    def get_incident_text(self):
        if self.type.tweet:
            text = self.type.tweet
        else:
            text ='%s - %s' % (self.type.title, self.type.description)
        return '%s! %s' % (self.type.get_penalty_display(), text)

    def get_context_hashtag(self):
        return '#%s' % self.performance.song.country.hashtag

    def __str__(self):
        predicted=''
        if self.predicted:
            predicted=' (predicted)'
        return '%s%s during %s' % (
            self.type.title,
            predicted,
            self.performance,
        )


class ScoreIncidentType(BaseIncidentType):
    """
    An IncidentType that can only occur during the announcement of
    scores during a Contest.
    """
    participant = models.ManyToManyField(
        Participant,
        through='ScoreIncident',
        blank=True,
    )


class ScoreIncident(BaseIncident):
    """
    An instance of a ScoreIncidentType that has occurred as a specific
    Participant has announced their scores during a Show of a Contest.
    """
    type = models.ForeignKey(
        ScoreIncidentType,
        on_delete=models.CASCADE
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )

    def get_incident_text(self):
        if self.type.tweet:
            text = self.type.tweet
        else:
            text ='%s - %s' % (self.type.title, self.type.description)
        return '%s! %s' % (self.type.get_penalty_display(), text)

    def get_context_hashtag(self):
        return '#%s' % self.participant.country.hashtag

    def __str__(self):
        return '%s by %s' % (self.type, self.participant)


class ShowIncidentType(BaseIncidentType):
    """
    An IncidentType that can occur at any time during a Show of a Contest.
    """
    show = models.ManyToManyField(
        Show,
        through='ShowIncident',
        blank=True,
    )


class ShowIncident(BaseIncident):
    """
    An instance of a ShowIncidentType that has occurred during
    a specific Show of a Contest.
=    """
    type = models.ForeignKey(
        ShowIncidentType,
        on_delete=models.CASCADE
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE
    )

    def get_incident_text(self):
        return '%s! %s' % (
            self.type.get_penalty_display(),
            self.type.description,
        )

    def get_context_hashtag(self):
        return None

    def __str__(self):
        return '%s in %s' % (self.type, self.show)
