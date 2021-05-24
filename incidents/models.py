from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class PerformanceIncidentType(BaseIncidentType):
    """
    An IncidentType that can only occur during a Performance.
    """
    performances = models.ManyToManyField(
        Performance,
        through='PerformanceIncident',
        blank=True,
    )


class PerformanceIncident(models.Model):
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

    def __str__(self):
        return '%s during %s' % (
            self.type.title,
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


class ScoreIncident(models.Model):
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


class ShowIncident(models.Model):
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

    def __str__(self):
        return '%s in %s' % (self.type, self.show)
