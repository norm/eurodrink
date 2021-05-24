from django.core.management.base import BaseCommand
import toml

from contests.models import (
    Language,
    Country,
    Contest,
    Singer,
    Artist,
)


class Command(BaseCommand):
    help = 'Import from eurovision_data/ files'

    def handle(self, *args, **options):
        self.load_countries('eurovision_data/countries.toml')
        self.load_contests('eurovision_data/contests.toml')

        for contest in Contest.objects.all():
            self.load_singers('eurovision_data/singers/%s.toml' % contest.year)
            self.load_artists('eurovision_data/artists/%s.toml' % contest.year)

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
