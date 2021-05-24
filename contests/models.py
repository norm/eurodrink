from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """
    A language that a Song can be performed in, usually an officially
    recognised national language of a participating Country.
    """
    id = models.CharField(primary_key=True, max_length=64)

    def __str__(self):
        return self.id


class Country(models.Model):
    """
    A country that participates in Eurovision.
    """
    id = models.CharField(primary_key=True, max_length=64)
    english = models.CharField(max_length=128, blank=False, null=False)
    hashtag = models.CharField(max_length=3, blank=False, null=False)
    neighbours = models.ManyToManyField("self", blank=True)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.english

    class Meta:
        ordering = ['english']


class Contest(models.Model):
    """
    A whole Eurovision Song Contest event.
    """
    year = models.IntegerField(primary_key=True)
    host = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s" % self.year


class Singer(models.Model):
    """
    An individual singer that is, or is part of, an Artist.
    """
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=128, blank=False, null=False)
    known_as = models.CharField(max_length=128)
    born = models.DateField(null=True, blank=True)
    died = models.DateField(null=True, blank=True)
    citizenship = models.ManyToManyField(Country)

    def __str__(self):
        return self.known_as or self.name


class Artist(models.Model):
    """
    One or more Singers (and any other musicians/performers) that
    are credited as performing a Song in a Show.
    """
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=128, blank=False, null=False)
    singer = models.ManyToManyField(Singer)

    def __str__(self):
        return self.name


class Song(models.Model):
    """
    A song, as performed by an Artist, that represents a Country in a
    Contest.
    """
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=128, blank=False, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return u"%s by %s (from %s)" % (self.title, self.artist, self.contest)


class Participant(models.Model):
    """
    A Country taking part in a Contest.
    """
    class Meta:
        unique_together = ['country', 'contest']

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    def __str__(self):
        return '%s in %s' % (self.country, self.contest)


class Show(models.Model):
    """
    An individual live show in a Contest.
    """
    class Type(models.TextChoices):
        FINAL = 'final', _('Grand Final')
        FIRST_SEMI = 'first-semi', _('First Semi-Final')
        SECOND_SEMI = 'second-semi', _('Second Semi-Final')

    id = models.CharField(primary_key=True, max_length=64)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    type = models.CharField(max_length=16, choices=Type.choices)

    def __str__(self):
        return u"%s %s" % (self.Type(self.type).label, self.contest)


class Performance(models.Model):
    """
    A Song, performed in a Show.
    """
    class Meta:
        unique_together = ['song', 'show']

    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    @property
    def score(self):
        return self.score_set.aggregate(
                models.Sum('points')
            )['points__sum'] or 0

    def __str__(self):
        return u"%s (%s, %s #%s) in %s" % (
            self.song.title,
            self.song.artist,
            self.song.country,
            self.song.country.hashtag,
            self.show,
        )


class Score(models.Model):
    """
    A number of points awarded by a Country to a Performance,
    either by a jury or a televote.
    """
    class Meta:
        unique_together = ['country', 'performance', 'source']

    class AwardedBy(models.TextChoices):
        JURY = 'jury', _('Jury')
        TELEVOTE = 'televote', _('Televote')

    points = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    source = models.CharField(max_length=16, choices=AwardedBy.choices)

    def __str__(self):
        return "%d %s points from %s for %s" % (
            self.points,
            self.AwardedBy(self.source).label,
            self.country,
            self.performance,
        )
