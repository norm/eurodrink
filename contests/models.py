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
