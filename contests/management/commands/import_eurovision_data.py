from datetime import date
from django.core.management.base import BaseCommand
import toml

from contests.models import (
    Language,
    Country,
    Contest,
    Singer,
    Artist,
    Song,
    Participant,
    Show,
    Performance,
    Score,
)


class Command(BaseCommand):
    help = 'Import from eurovision_data/ files'

    def handle(self, *args, **options):
        self.load_countries('eurovision_data/countries.toml')
        self.load_contests('eurovision_data/contests.toml')

        for contest in Contest.objects.all():
            self.load_singers('eurovision_data/singers/%s.toml' % contest.year)
            self.load_artists('eurovision_data/artists/%s.toml' % contest.year)
            self.load_songs('eurovision_data/songs/%s.toml' % contest.year, contest)
            self.load_shows('eurovision_data/shows/%s.toml' % contest.year, contest)

        for show in Show.objects.all():
            self.load_scores(
                'eurovision_data/scores/%s-%s.toml' % (
                    show.contest.year,
                    show.type,
                ),
                show,
            )

    def load_countries(self, data):
        countries = toml.load(data)
        for country in countries:
            langs = []
            for language in countries[country]['language']:
                lang, _ = Language.objects.get_or_create(id=language)
                langs.append(lang)
            del countries[country]['language']
            obj, _ = Country.objects.update_or_create(
                id=country,
                **countries[country],
            )
            for lang in langs:
                obj.languages.add(lang)

    def load_contests(self, data):
        contests = toml.load(data)
        for contest in contests:
            Contest.objects.update_or_create(
                year=contest,
                host=Country.objects.get(id=contests[contest]['host']),
            )

    def load_singers(self, data):
        singers = toml.load(data)
        for singer in singers:
            citizenships = singers[singer].pop('citizenship')
            obj, _ = Singer.objects.update_or_create(
                id=singer,
                **singers[singer],
            )
            for country in citizenships:
                obj.citizenship.add(Country.objects.get(id=country))

    def load_artists(self, data):
        artists = toml.load(data)
        for artist in artists:
            singers = artists[artist].pop('singer')
            obj, _ = Artist.objects.update_or_create(
                id=artist,
                **artists[artist],
            )
            for singer in singers:
                obj.singer.add(Singer.objects.get(id=singer))

    def load_songs(self, data, contest):
        songs = toml.load(data)
        for song in songs:
            langs = []
            country = Country.objects.get(id=songs[song]['country'])
            for language in songs[song]['language']:
                lang, _ = Language.objects.get_or_create(id=language)
                langs.append(lang)
            obj, _ = Song.objects.update_or_create(
                id=song,
                title=songs[song]['title'],
                artist=Artist.objects.get(id=songs[song]['artist']),
                country=country,
                contest=contest,
            )
            for lang in langs:
                obj.languages.add(lang)

            # a Participant is a Country in a Contest, which has a 1:1
            # relationship with a Song, so we create that here too
            Participant.objects.get_or_create(
                country=country,
                contest=contest,
            )

    def load_shows(self, data, contest):
        shows = toml.load(data)
        for show in shows:
            show_obj, _ = Show.objects.update_or_create(
                id=show,
                contest=contest,
                type=shows[show]['type'],
                date=shows[show]['date'],
            )
            for performance in shows[show]['performances']:
                perf_obj, _ = Performance.objects.update_or_create(
                    song=Song.objects.get(id=performance),
                    show=show_obj,
                )

    def load_scores(self, data, show):
        scores = toml.load(data)
        for country_id in scores:
            country = Country.objects.get(id=country_id)
            for score in scores[country_id]:
                performance = Performance.objects.filter(
                    show=show,
                    song=Song.objects.get(id=score['song']),
                )[0]
                Score.objects.update_or_create(
                    performance=performance,
                    country=country,
                    points=score['points'],
                    source=score['source'],
                )